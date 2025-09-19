#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import multiprocessing
import time
from typing import List, Dict, Any, Optional
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass

from .device_manager import DeviceConfig
from .device_logger import DeviceLoggerWriter


@dataclass
class ExecutionResult:
    """执行结果数据类"""
    device_name: str
    success: bool
    return_code: int
    error_message: Optional[str] = None
    execution_time: float = 0.0


class ExecutionEngine:
    """执行引擎基类"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.results: List[ExecutionResult] = []
    
    def execute_devices(self, devices: List[DeviceConfig], execution_config: Dict[str, Any]) -> List[ExecutionResult]:
        """执行设备测试（子类实现）"""
        raise NotImplementedError


class ParallelExecutor(ExecutionEngine):
    """并行执行器"""
    
    def __init__(self, project_root: Path):
        super().__init__(project_root)
    
    def execute_devices(self, devices: List[DeviceConfig], execution_config: Dict[str, Any]) -> List[ExecutionResult]:
        """并行执行设备测试"""
        max_concurrent = execution_config.get('max_concurrent', len(devices))
        
        print(f"🚀 启动并行执行模式，最大并发数: {max_concurrent}")
        print("=" * 60)
        
        start_time = time.time()
        
        with ProcessPoolExecutor(max_workers=max_concurrent) as executor:
            # 提交所有任务
            future_to_device = {
                executor.submit(self._execute_single_device, device): device 
                for device in devices
            }
            
            # 收集结果
            for future in as_completed(future_to_device):
                device = future_to_device[future]
                try:
                    result = future.result()
                    self.results.append(result)
                    
                    status = "✅ 成功" if result.success else "❌ 失败"
                    print(f"{status} {device.name} - 耗时: {result.execution_time:.2f}秒")
                    
                except Exception as e:
                    error_result = ExecutionResult(
                        device_name=device.name,
                        success=False,
                        return_code=1,
                        error_message=str(e),
                        execution_time=0.0
                    )
                    self.results.append(error_result)
                    print(f"❌ 异常 {device.name} - 错误: {e}")
        
        total_time = time.time() - start_time
        print("=" * 60)
        print(f"⏱️  并行执行完成，总耗时: {total_time:.2f}秒")
        
        return self.results
    
    def _execute_single_device(self, device: DeviceConfig) -> ExecutionResult:
        """执行单个设备测试"""
        start_time = time.time()
        
        try:
            # 创建设备日志写入器
            device_logger = DeviceLoggerWriter(
                device_name=device.name,
                device_id=device.device_id,
                device_type=device.device_type,
                ws_port=device.ws_port,
                project_root=self.project_root
            )
            
            # 构建执行命令
            cmd = self._build_device_command(device)
            
            # 设置环境变量，让脚本能够获取日志文件路径
            import os
            env = os.environ.copy()
            env['DEVICE_LOG_FILE'] = str(device_logger.log_file_path)
            
            # 执行命令，将输出重定向到设备日志文件
            result = subprocess.run(
                cmd, 
                cwd=self.project_root,
                stdout=device_logger.file,
                stderr=device_logger.file,
                text=True,
                timeout=3600,  # 1小时超时
                env=env
            )
            
            # 关闭设备日志文件
            device_logger.close()
            
            execution_time = time.time() - start_time
            
            return ExecutionResult(
                device_name=device.name,
                success=result.returncode == 0,
                return_code=result.returncode,
                error_message=None,  # 错误信息已经写入日志文件
                execution_time=execution_time
            )
            
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            return ExecutionResult(
                device_name=device.name,
                success=False,
                return_code=1,
                error_message="执行超时",
                execution_time=execution_time
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return ExecutionResult(
                device_name=device.name,
                success=False,
                return_code=1,
                error_message=str(e),
                execution_time=execution_time
            )
    
    def _build_device_command(self, device: DeviceConfig) -> List[str]:
        """构建设备执行命令"""
        # 获取脚本模块名（去掉.py扩展名）
        script_module = device.script_file.replace('.py', '')
        
        # 使用模块方式执行命令
        cmd = [sys.executable, '-m', f'scripts.{script_module}']
        
        # 添加设备参数
        cmd.extend(['--mobile'])
        cmd.extend(['--device-id', device.device_id])
        cmd.extend(['--device-type', device.device_type])
        cmd.extend(['--ws-port', str(device.ws_port)])
        
        # 添加测试范围参数
        if device.max_chapter:
            cmd.extend(['--max-chapter', str(device.max_chapter)])
        
        if device.skip_chapters:
            cmd.extend(['--skip-chapters', ','.join(map(str, device.skip_chapters))])
        
        return cmd


class SequentialExecutor(ExecutionEngine):
    """串行执行器"""
    
    def __init__(self, project_root: Path):
        super().__init__(project_root)
    
    def execute_devices(self, devices: List[DeviceConfig], execution_config: Dict[str, Any]) -> List[ExecutionResult]:
        """串行执行设备测试"""
        print("🚀 启动串行执行模式")
        print("=" * 60)
        
        start_time = time.time()
        
        for i, device in enumerate(devices, 1):
            print(f"📱 执行设备 {i}/{len(devices)}: {device.name}")
            
            result = self._execute_single_device(device)
            self.results.append(result)
            
            status = "✅ 成功" if result.success else "❌ 失败"
            print(f"{status} {device.name} - 耗时: {result.execution_time:.2f}秒")
            
            if i < len(devices):
                print("-" * 40)
        
        total_time = time.time() - start_time
        print("=" * 60)
        print(f"⏱️  串行执行完成，总耗时: {total_time:.2f}秒")
        
        return self.results
    
    def _execute_single_device(self, device: DeviceConfig) -> ExecutionResult:
        """执行单个设备测试"""
        start_time = time.time()
        
        try:
            # 创建设备日志写入器
            device_logger = DeviceLoggerWriter(
                device_name=device.name,
                device_id=device.device_id,
                device_type=device.device_type,
                ws_port=device.ws_port,
                project_root=self.project_root
            )
            
            # 构建执行命令
            cmd = self._build_device_command(device)
            
            print(f"🔧 执行命令: {' '.join(cmd)}")
            
            # 执行命令，将输出重定向到设备日志文件
            result = subprocess.run(
                cmd, 
                cwd=self.project_root,
                stdout=device_logger.file,
                stderr=device_logger.file,
                text=True,
                check=False
            )
            
            # 关闭设备日志文件
            device_logger.close()
            
            execution_time = time.time() - start_time
            
            return ExecutionResult(
                device_name=device.name,
                success=result.returncode == 0,
                return_code=result.returncode,
                error_message=None,
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return ExecutionResult(
                device_name=device.name,
                success=False,
                return_code=1,
                error_message=str(e),
                execution_time=execution_time
            )
    
    def _build_device_command(self, device: DeviceConfig) -> List[str]:
        """构建设备执行命令"""
        # 获取脚本模块名（去掉.py扩展名）
        script_module = device.script_file.replace('.py', '')
        
        # 使用模块方式执行命令
        cmd = [sys.executable, '-m', f'scripts.{script_module}']
        
        # 添加设备参数
        cmd.extend(['--mobile'])
        cmd.extend(['--device-id', device.device_id])
        cmd.extend(['--device-type', device.device_type])
        cmd.extend(['--ws-port', str(device.ws_port)])
        
        # 添加测试范围参数
        if device.max_chapter:
            cmd.extend(['--max-chapter', str(device.max_chapter)])
        
        if device.skip_chapters:
            cmd.extend(['--skip-chapters', ','.join(map(str, device.skip_chapters))])
        
        return cmd


class ExecutionEngineFactory:
    """执行引擎工厂"""
    
    @staticmethod
    def create_executor(execution_mode: str, project_root: Path) -> ExecutionEngine:
        """创建执行器"""
        if execution_mode == "parallel":
            return ParallelExecutor(project_root)
        elif execution_mode == "sequential":
            return SequentialExecutor(project_root)
        else:
            raise ValueError(f"不支持的执行模式: {execution_mode}")
