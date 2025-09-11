#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import os
import sys
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

class TestRunner:
    def __init__(self, config_file='test_config.yaml'):
        """初始化测试运行器"""
        self.config_file = config_file
        self.config = None
        self.project_root = Path(__file__).parent
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
        except yaml.YAMLError as e:
            raise ValueError(f"YAML配置文件格式错误: {e}")
        except Exception as e:
            raise ValueError(f"读取配置文件失败: {e}")
    
    def validate_config(self):
        """验证配置文件的完整性"""
        if not self.config:
            raise ValueError("配置文件未加载")
        
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
        
        print("配置文件验证通过")
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
            
            print("设置日志...")
            self.setup_logging()
            
            print("开始执行测试...")
            return self.execute_script()
            
        except Exception as e:
            print(f"运行失败: {e}")
            return 1

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
