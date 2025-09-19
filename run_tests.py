#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import os
import sys
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

from common.device_manager import DeviceManager, DeviceConfig
from common.execution_engine import ExecutionEngineFactory, ExecutionResult

class TestRunner:
    def __init__(self, config_file='test_config.yaml'):
        """初始化测试运行器"""
        self.config_file = config_file
        self.config = None
        self.project_root = Path(__file__).parent
        self.device_manager = DeviceManager(self.project_root)
        self.is_multi_device = False
        self.load_config()
        
    def load_config(self):
        """加载YAML配置文件"""
        config_path = self.project_root / self.config_file
        
        if not config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_path}")
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            print(f"成功加载配置文件: {config_path}")
            
            # 检测是否为多设备配置
            self.is_multi_device = 'devices' in self.config
            
        except yaml.YAMLError as e:
            raise ValueError(f"YAML配置文件格式错误: {e}")
        except Exception as e:
            raise ValueError(f"读取配置文件失败: {e}")
    
    def validate_config(self):
        """验证配置文件的完整性"""
        if not self.config:
            raise ValueError("配置文件未加载")
        
        if self.is_multi_device:
            return self._validate_multi_device_config()
        else:
            return self._validate_single_device_config()
    
    def _validate_multi_device_config(self):
        """验证多设备配置"""
        # 检查必需字段
        if 'devices' not in self.config:
            raise ValueError("多设备配置缺少 'devices' 字段")
        
        if 'execution' not in self.config:
            raise ValueError("多设备配置缺少 'execution' 字段")
        
        # 解析和验证设备配置
        devices = self.device_manager.parse_devices(self.config)
        self.device_manager.validate_devices()
        
        # 验证执行配置
        execution_config = self.config['execution']
        if 'mode' not in execution_config:
            raise ValueError("execution.mode 字段缺失")
        
        mode = execution_config['mode']
        if mode not in ['parallel', 'sequential']:
            raise ValueError(f"不支持的执行模式: {mode}")
        
        print("多设备配置文件验证通过")
        return True
    
    def _validate_single_device_config(self):
        """验证单设备配置（向后兼容）"""
        # 检查必需字段
        required_fields = ['environment', 'test_scope', 'execution']
        for field in required_fields:
            if field not in self.config:
                raise ValueError(f"配置文件缺少必需字段: {field}")
        
        # 验证环境配置
        env = self.config['environment']
        if 'is_mobile' not in env:
            raise ValueError("environment.is_mobile 字段缺失")
        
        if 'device_type' not in env:
            raise ValueError("environment.device_type 字段缺失")
        
        # 验证移动端配置
        if env['is_mobile']:
            if not env.get('device_id'):
                raise ValueError("移动端运行需要提供 device_id")
            
            device_type = env['device_type']
            if device_type not in ['android', 'ios']:
                raise ValueError(f"不支持的设备类型: {device_type}")
        
        # 验证执行配置
        exec_config = self.config['execution']
        if 'script_file' not in exec_config:
            raise ValueError("execution.script_file 字段缺失")
        
        script_path = self.project_root / 'scripts' / exec_config['script_file']
        if not script_path.exists():
            raise FileNotFoundError(f"脚本文件不存在: {script_path}")
        
        print("单设备配置文件验证通过")
        return True
    
    def setup_logging(self):
        """设置日志配置"""
        if 'logging' not in self.config:
            return
        
        log_config = self.config['logging']
        
        # 生成日志文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_config.get('log_file', 'logs/run_{timestamp}.log').format(timestamp=timestamp)
        log_path = self.project_root / log_file
        
        # 确保日志目录存在
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"日志文件: {log_path}")
        return str(log_path)
    
    def build_command(self):
        """构建执行命令"""
        exec_config = self.config['execution']
        script_file = exec_config['script_file']
        
        # 获取脚本模块名（去掉.py扩展名）
        script_module = script_file.replace('.py', '')
        
        # 使用模块方式执行命令
        cmd = [sys.executable, '-m', f'scripts.{script_module}']
        
        # 添加环境参数
        env = self.config['environment']
        if env['is_mobile']:
            cmd.extend(['--mobile'])
            if env.get('device_id'):
                cmd.extend(['--device-id', env['device_id']])
            # 添加设备类型参数
            if env.get('device_type'):
                cmd.extend(['--device-type', env['device_type']])
        
        # 添加测试范围参数
        test_scope = self.config['test_scope']
        if test_scope.get('max_chapter'):
            cmd.extend(['--max-chapter', str(test_scope['max_chapter'])])
        
        if test_scope.get('skip_chapters'):
            cmd.extend(['--skip-chapters', ','.join(map(str, test_scope['skip_chapters']))])
        
        if test_scope.get('specific_chapters'):
            cmd.extend(['--specific-chapters', ','.join(map(str, test_scope['specific_chapters']))])
        
        # 添加服务器配置
        if 'server' in self.config:
            server_config = self.config['server']
            if server_config.get('ws_port'):
                cmd.extend(['--ws-port', str(server_config['ws_port'])])
        
        # 添加其他脚本参数
        if exec_config.get('script_args'):
            cmd.extend(exec_config['script_args'])
        
        return cmd
    
    def execute_script(self):
        """执行测试脚本"""
        cmd = self.build_command()
        
        print(f"🚀 执行命令: {' '.join(cmd)}")
        print("=" * 60)
        
        try:
            # 执行脚本
            result = subprocess.run(cmd, cwd=self.project_root, check=True)
            print("=" * 60)
            print("✅测试执行完成")
            return result.returncode
        except subprocess.CalledProcessError as e:
            print("=" * 60)
            print(f"❌测试执行失败: {e}")
            return e.returncode
        except Exception as e:
            print("=" * 60)
            print(f"执行过程中发生错误: {e}")
            return 1
    
    def run(self):
        """运行测试"""
        try:
            print("开始加载配置...")
            self.load_config()
            
            print("验证配置...")
            self.validate_config()
            
            if self.is_multi_device:
                print("开始执行多设备测试...")
                return self.execute_multi_device()
            else:
                print("设置日志...")
                self.setup_logging()
                
                print("开始执行单设备测试...")
                return self.execute_script()
            
        except Exception as e:
            print(f"运行失败: {e}")
            return 1
    
    def execute_multi_device(self):
        """执行多设备测试"""
        try:
            # 获取设备列表
            devices = self.device_manager.get_devices()
            
            # 分配端口资源
            self.device_manager.allocate_ports()
            
            # 检查设备状态
            device_status = self.device_manager.check_device_status()
            
            # 显示设备信息
            print(self.device_manager.get_device_info())
            print()
            
            # 显示设备状态
            print("📱 设备状态检查:")
            for device in devices:
                status = "✅ 可用" if device_status.get(device.name, False) else "❌ 不可用"
                print(f"├── {device.name}: {status}")
            print()
            
            # 获取执行配置
            execution_config = self.config['execution']
            execution_mode = execution_config['mode']
            
            print(f"⚙️  执行模式: {'并行执行' if execution_mode == 'parallel' else '串行执行'}")
            if execution_mode == 'parallel':
                max_concurrent = execution_config.get('max_concurrent', len(devices))
                print(f"   最大并发数: {max_concurrent}")
            print(f"⏱️  开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print()
            
            # 创建执行引擎
            executor = ExecutionEngineFactory.create_executor(execution_mode, self.project_root)
            
            # 执行测试
            results = executor.execute_devices(devices, execution_config)
            
            # 显示执行结果
            self._display_execution_results(results)
            
            # 生成测试报告
            self._generate_multi_device_reports(devices)
            
            # 返回结果（如果有任何设备失败，返回1）
            return 0 if all(result.success for result in results) else 1
            
        except Exception as e:
            print(f"多设备执行失败: {e}")
            return 1
    
    def _display_execution_results(self, results: List[ExecutionResult]):
        """显示执行结果"""
        print("=" * 60)
        print("📊 执行结果汇总:")
        print()
        
        success_count = 0
        total_time = 0.0
        
        for result in results:
            status = "✅ 成功" if result.success else "❌ 失败"
            print(f"├── {result.device_name}: {status} - 耗时: {result.execution_time:.2f}秒")
            
            if result.success:
                success_count += 1
            else:
                if result.error_message:
                    print(f"│   └── 错误: {result.error_message}")
            
            total_time += result.execution_time
        
        print()
        print(f"📈 统计信息:")
        print(f"├── 总设备数: {len(results)}")
        print(f"├── 成功设备数: {success_count}")
        print(f"├── 失败设备数: {len(results) - success_count}")
        print(f"├── 成功率: {success_count/len(results)*100:.1f}%")
        print(f"└── 总耗时: {total_time:.2f}秒")
        print()
        
        if success_count == len(results):
            print("🎉 所有设备测试完成！")
        else:
            print("⚠️  部分设备测试失败，请检查日志文件")
    
    def _generate_multi_device_reports(self, devices: List[DeviceConfig]):
        """为多设备测试生成报告"""
        try:
            from common.report_generator import TestReportGenerator
            
            print("\n📄 生成测试报告...")
            
            # 为每个设备生成报告
            for device in devices:
                try:
                    # 查找设备对应的日志文件
                    device_log_files = self._find_device_log_files(device)
                    
                    if not device_log_files:
                        print(f"⚠️  未找到设备 {device.name} 的日志文件")
                        continue
                    
                    # 使用最新的日志文件生成报告
                    latest_log_file = max(device_log_files, key=lambda x: x.stat().st_mtime)
                    
                    # 生成报告
                    report_generator = TestReportGenerator(
                        log_file_path=str(latest_log_file),
                        config_file_path=str(self.project_root / self.config_file),
                        output_dir=str(self.project_root / "reports")
                    )
                    
                    report_path = report_generator.generate_report()
                    print(f"✅ 设备 {device.name} 报告已生成: {report_path}")
                    
                except Exception as e:
                    print(f"❌ 设备 {device.name} 报告生成失败: {e}")
            
            print("📊 所有设备报告生成完成！")
            
        except Exception as e:
            print(f"❌ 报告生成失败: {e}")
    
    def _find_device_log_files(self, device: DeviceConfig) -> List[Path]:
        """查找设备对应的日志文件"""
        logs_dir = self.project_root / "logs"
        if not logs_dir.exists():
            return []
        
        # 查找设备日志文件（格式：device_{device_type}_{device_id}_{ws_port}_{timestamp}.log）
        device_id_clean = device.device_id.replace(':', '_').replace('.', '_')
        pattern = f"device_{device.device_type}_{device_id_clean}_{device.ws_port}_*.log"
        
        import glob
        log_files = []
        for log_file in glob.glob(str(logs_dir / pattern)):
            log_files.append(Path(log_file))
        
        return log_files

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='基于YAML配置的测试执行器')
    parser.add_argument('-c', '--config', default='test_config.yaml', 
                       help='配置文件路径 (默认: test_config.yaml)')
    parser.add_argument('--validate-only', action='store_true',
                       help='仅验证配置文件，不执行测试')
    
    args = parser.parse_args()
    
    runner = TestRunner(args.config)
    
    if args.validate_only:
        try:
            runner.load_config()
            runner.validate_config()
            print("配置文件验证通过")
            return 0
        except Exception as e:
            print(f"配置文件验证失败: {e}")
            return 1
    else:
        return runner.run()

if __name__ == "__main__":
    sys.exit(main())
