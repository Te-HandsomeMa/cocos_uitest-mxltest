#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import socket
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DeviceConfig:
    """设备配置数据类"""
    name: str
    device_id: str
    device_type: str
    ws_port: int
    max_chapter: int
    skip_chapters: List[int]
    script_file: str
    enable_recording: bool = False
    
    def __post_init__(self):
        """验证设备配置"""
        if not self.name:
            raise ValueError("设备名称不能为空")
        if not self.device_id:
            raise ValueError("设备ID不能为空")
        if self.device_type not in ['android', 'ios', 'pc']:
            raise ValueError(f"不支持的设备类型: {self.device_type}")
        if not (1 <= self.ws_port <= 65535):
            raise ValueError(f"端口号必须在1-65535之间: {self.ws_port}")
        if not (1 <= self.max_chapter <= 7):
            raise ValueError(f"最大章节必须在1-7之间: {self.max_chapter}")


class DeviceManager:
    """设备管理器"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.devices: List[DeviceConfig] = []
        self.used_ports: set = set()
    
    def parse_devices(self, config: Dict[str, Any]) -> List[DeviceConfig]:
        """解析多设备配置"""
        if 'devices' not in config:
            raise ValueError("配置文件中缺少 'devices' 字段")
        
        devices_config = config['devices']
        if not isinstance(devices_config, list):
            raise ValueError("'devices' 字段必须是列表")
        
        devices = []
        for i, device_config in enumerate(devices_config):
            try:
                device = DeviceConfig(
                    name=device_config.get('name', f'设备{i+1}'),
                    device_id=device_config['device_id'],
                    device_type=device_config['device_type'],
                    ws_port=device_config['ws_port'],
                    max_chapter=device_config.get('max_chapter', 7),
                    skip_chapters=device_config.get('skip_chapters', []),
                    script_file=device_config['script_file'],
                    enable_recording=device_config.get('enable_recording', False)
                )
                devices.append(device)
            except KeyError as e:
                raise ValueError(f"设备配置缺少必需字段: {e}")
            except Exception as e:
                raise ValueError(f"设备配置验证失败: {e}")
        
        self.devices = devices
        return devices
    
    def validate_devices(self) -> bool:
        """验证设备配置"""
        if not self.devices:
            raise ValueError("没有配置任何设备")
        
        # 检查设备名称唯一性
        names = [device.name for device in self.devices]
        if len(names) != len(set(names)):
            raise ValueError("设备名称必须唯一")
        
        # 检查端口唯一性
        ports = [device.ws_port for device in self.devices]
        if len(ports) != len(set(ports)):
            raise ValueError("设备端口必须唯一")
        
        # 检查脚本文件存在性
        for device in self.devices:
            script_path = self.project_root / 'scripts' / device.script_file
            if not script_path.exists():
                raise FileNotFoundError(f"脚本文件不存在: {script_path}")
        
        print(f"✅ 验证通过，共配置 {len(self.devices)} 个设备")
        return True
    
    def allocate_ports(self) -> None:
        """分配端口资源"""
        self.used_ports = set()
        
        for device in self.devices:
            # 检查端口是否被占用
            if self._is_port_in_use(device.ws_port):
                # 自动分配可用端口
                new_port = self._find_available_port()
                print(f"⚠️  端口 {device.ws_port} 被占用，自动分配端口 {new_port} 给设备 {device.name}")
                device.ws_port = new_port
            
            self.used_ports.add(device.ws_port)
    
    def _is_port_in_use(self, port: int) -> bool:
        """检查端口是否被占用"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex(('localhost', port))
                return result == 0
        except Exception:
            return False
    
    def _find_available_port(self, start_port: int = 5101) -> int:
        """查找可用端口"""
        port = start_port
        while port <= 65535:
            if port not in self.used_ports and not self._is_port_in_use(port):
                return port
            port += 1
        raise RuntimeError("无法找到可用端口")
    
    def check_device_status(self) -> Dict[str, bool]:
        """检查设备状态"""
        device_status = {}
        
        for device in self.devices:
            try:
                if device.device_type == 'android':
                    # 检查ADB连接
                    result = os.system(f'adb devices | grep "{device.device_id}" > /dev/null 2>&1')
                    device_status[device.name] = result == 0
                elif device.device_type == 'ios':
                    # 检查WDA连接（这里简化处理）
                    device_status[device.name] = True
                else:
                    device_status[device.name] = True
            except Exception:
                device_status[device.name] = False
        
        return device_status
    
    def get_device_info(self) -> str:
        """获取设备信息摘要"""
        info_lines = ["📱 设备配置信息:"]
        
        for i, device in enumerate(self.devices, 1):
            info_lines.append(f"├── {device.name}")
            info_lines.append(f"│   ├── 设备ID: {device.device_id}")
            info_lines.append(f"│   ├── 设备类型: {device.device_type}")
            info_lines.append(f"│   ├── WebSocket端口: {device.ws_port}")
            info_lines.append(f"│   ├── 最大章节: {device.max_chapter}")
            info_lines.append(f"│   ├── 跳过章节: {device.skip_chapters if device.skip_chapters else '无'}")
            info_lines.append(f"│   └── 脚本文件: {device.script_file}")
        
        return "\n".join(info_lines)
    
    def get_devices(self) -> List[DeviceConfig]:
        """获取设备列表"""
        return self.devices.copy()
    
    def get_device_by_name(self, name: str) -> Optional[DeviceConfig]:
        """根据名称获取设备配置"""
        for device in self.devices:
            if device.name == name:
                return device
        return None
