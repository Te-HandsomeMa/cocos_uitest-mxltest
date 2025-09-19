#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from .report_generator import TestReportGenerator


class DeviceLoggerWriter:
    """设备专用日志写入器"""
    
    def __init__(self, device_name: str, device_id: str, device_type: str, ws_port: int, project_root: Path):
        self.device_name = device_name
        self.device_id = device_id
        self.device_type = device_type
        self.ws_port = ws_port
        self.project_root = project_root
        
        # 生成设备专用日志文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"device_{device_type}_{device_id.replace(':', '_').replace('.', '_')}_{ws_port}_{timestamp}.log"
        self.log_file_path = project_root / "logs" / log_filename
        
        # 确保日志目录存在
        self.log_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 打开日志文件
        self.file = open(self.log_file_path, "a", encoding="utf-8", errors="replace")
        self.report_generated = False
        
        # 写入设备信息头部
        self._write_device_header()
    
    def __getattr__(self, name):
        """代理其他属性到文件对象"""
        return getattr(self.file, name)
    
    def _write_device_header(self):
        """写入设备信息头部"""
        header = f"""
{'='*80}
设备信息:
├── 设备名称: {self.device_name}
├── 设备ID: {self.device_id}
├── 设备类型: {self.device_type}
├── WebSocket端口: {self.ws_port}
├── 日志文件: {self.log_file_path}
└── 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*80}

"""
        self.file.write(header)
        self.file.flush()
    
    def write(self, message: str):
        """写入日志消息"""
        # 添加设备标识前缀
        device_prefix = f"[DEVICE:{self.device_type}_{self.device_id}] "
        prefixed_message = device_prefix + message
        
        # 写入文件
        self.file.write(prefixed_message)
        self.file.flush()
        
        # 检测测试结束，自动生成报告
        if "测试结束" in message and not self.report_generated:
            self._generate_test_report()
    
    def flush(self):
        """刷新缓冲区"""
        self.file.flush()
    
    def close(self):
        """关闭日志文件"""
        # 写入结束信息
        end_info = f"""
{'='*80}
测试结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*80}
"""
        self.file.write(end_info)
        
        # 先关闭文件，确保所有内容都已写入
        self.file.close()
        
        # 在文件关闭后生成报告，确保时间信息完整
        if not self.report_generated:
            self._generate_test_report()
    
    def _generate_test_report(self):
        """生成测试报告"""
        try:
            # 确保reports目录存在
            reports_dir = self.project_root / "reports"
            reports_dir.mkdir(exist_ok=True)
            
            # 生成报告
            generator = TestReportGenerator(str(self.log_file_path), str(reports_dir))
            report_path = generator.generate_report()
            
            # 获取报告摘要
            summary = generator.get_report_summary()
            
            if summary['success']:
                stats = summary['summary']
                report_message = f"""
                
==================== 设备 {self.device_name} 测试报告生成完成 ====================
📄 HTML报告已生成: {report_path}
💡 请在浏览器中打开查看详细报告

========================================================
"""
            else:
                report_message = f"""
                
==================== 设备 {self.device_name} 报告生成失败 ====================
❌ 生成报告时出现错误: {summary['error']}
📄 日志文件位置: {self.log_file_path}

====================================================
"""
            
            # 只打印到控制台，不再写入已关闭的文件
            print(report_message)
            
            self.report_generated = True
            
        except Exception as e:
            error_message = f"""
            
==================== 设备 {self.device_name} 报告生成异常 ====================
❌ 生成报告时出现异常: {str(e)}
📄 日志文件位置: {self.log_file_path}

====================================================
"""
            # 只打印到控制台
            print(error_message)
            self.report_generated = True
    
    def get_log_file_path(self) -> str:
        """获取日志文件路径"""
        return str(self.log_file_path)


class DeviceLoggerManager:
    """设备日志管理器"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.loggers: dict = {}
    
    def create_logger(self, device_name: str, device_id: str, device_type: str, ws_port: int) -> DeviceLoggerWriter:
        """创建设备日志器"""
        logger = DeviceLoggerWriter(device_name, device_id, device_type, ws_port, self.project_root)
        self.loggers[device_name] = logger
        return logger
    
    def get_logger(self, device_name: str) -> Optional[DeviceLoggerWriter]:
        """获取设备日志器"""
        return self.loggers.get(device_name)
    
    def close_all_loggers(self):
        """关闭所有日志器"""
        for logger in self.loggers.values():
            logger.close()
    
    def get_all_log_files(self) -> list:
        """获取所有日志文件路径"""
        return [logger.get_log_file_path() for logger in self.loggers.values()]
