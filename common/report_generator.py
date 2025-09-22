#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML测试报告生成器
基于日志文件自动生成测试报告
"""

import os
import re
import json
import glob
import argparse
import yaml
from datetime import datetime
from typing import Dict, List, Any, Optional
import time


class LogParser:
    """日志解析器"""
    
    def __init__(self, log_file_path: str, config_file_path: str = "test_config.yaml"):
        self.log_file_path = log_file_path
        self.config_file_path = config_file_path
        self.data = {
            'test_info': {},
            'chapters': [],
            'operations': [],
            'errors': [],
            'summary': {}
        }
        # 添加便捷属性访问
        self.chapters = self.data['chapters']
        self.operations = self.data['operations']
        self.exceptions = self.data['errors']
        self.test_info = self.data['test_info']
        self.summary = self.data['summary']
        self.total_operations = 0
        self.planned_chapters = self._load_planned_chapters()
        self.expected_steps = self._load_expected_steps()
        self.device_info = self._extract_device_info()
    
    def _extract_device_info(self) -> Dict[str, str]:
        """从日志文件中提取设备信息"""
        device_info = {
            'device_name': '未知设备',
            'device_id': '未知',
            'device_type': '未知',
            'ws_port': '未知'
        }
        
        try:
            with open(self.log_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # 从设备头部信息中提取
                device_name_match = re.search(r'设备名称:\s*(.+)', content)
                if device_name_match:
                    device_info['device_name'] = device_name_match.group(1).strip()
                
                device_id_match = re.search(r'设备ID:\s*(.+)', content)
                if device_id_match:
                    device_info['device_id'] = device_id_match.group(1).strip()
                
                device_type_match = re.search(r'设备类型:\s*(.+)', content)
                if device_type_match:
                    device_info['device_type'] = device_type_match.group(1).strip()
                
                ws_port_match = re.search(r'WebSocket端口:\s*(.+)', content)
                if ws_port_match:
                    device_info['ws_port'] = ws_port_match.group(1).strip()
                
                # 从设备标识前缀中提取（备用方法）
                device_prefix_match = re.search(r'\[DEVICE:([^_]+)_([^\]]+)\]', content)
                if device_prefix_match:
                    device_info['device_type'] = device_prefix_match.group(1)
                    device_info['device_id'] = device_prefix_match.group(2).replace('_', ':').replace('_', '.')
                    
        except Exception as e:
            print(f"⚠️  提取设备信息失败: {e}")
        
        return device_info
    
    def _load_planned_chapters(self) -> int:
        """从配置文件加载计划测试的章节数"""
        try:
            if os.path.exists(self.config_file_path):
                with open(self.config_file_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    max_chapter = config.get('test_scope', {}).get('max_chapter')
                    if max_chapter:
                        return max_chapter
            print(f"⚠️  配置文件 {self.config_file_path} 不存在或未找到 max_chapter 配置，将使用默认值7")
            return 7
        except Exception as e:
            print(f"⚠️  读取配置文件失败: {e}，将使用默认值7")
            return 7
    
    def _load_expected_steps(self) -> Dict[int, int]:
        """从测试脚本中读取每章的预计步骤数"""
        script_path = "scripts/guide_test_Android.py"
        expected_steps = {}
        
        try:
            if os.path.exists(script_path):
                with open(script_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 查找所有章节函数
                chapter_pattern = r'async def chapter_(\w+)\(bp: BasePage\):'
                chapters = re.findall(chapter_pattern, content)
                
                for chapter_name in chapters:
                    chapter_num = chapter_name.replace('one', '1').replace('two', '2').replace('three', '3').replace('four', '4').replace('five', '5').replace('six', '6').replace('seven', '7').replace('eight', '8')
                    
                    # 查找该章节的所有perform_list
                    chapter_func_pattern = rf'async def chapter_{chapter_name}\(bp: BasePage\):(.*?)(?=async def chapter_|\Z)'
                    chapter_match = re.search(chapter_func_pattern, content, re.DOTALL)
                    
                    if chapter_match:
                        chapter_content = chapter_match.group(1)
                        
                        # 查找所有perform_list
                        perform_list_pattern = r'perform_list(?:_\d+)?\s*=\s*\[(.*?)\]'
                        perform_lists = re.findall(perform_list_pattern, chapter_content, re.DOTALL)
                        
                        total_steps = 0
                        for perform_list in perform_lists:
                            # 计算每个perform_list中的步骤数
                            # 移除注释行
                            lines = [line.strip() for line in perform_list.split('\n') if line.strip() and not line.strip().startswith('#')]
                            steps = len([line for line in lines if line.startswith('ElementsData.')])
                            total_steps += steps
                        
                        expected_steps[int(chapter_num)] = total_steps
                
                print(f"📊 从脚本中读取到预计步骤数: {expected_steps}")
                return expected_steps
            else:
                print(f"⚠️  测试脚本 {script_path} 不存在，将使用默认步骤数")
                return {}
        except Exception as e:
            print(f"⚠️  读取测试脚本失败: {e}，将使用默认步骤数")
            return {}
    
    def parse(self) -> Dict[str, Any]:
        """解析日志文件"""
        if not os.path.exists(self.log_file_path):
            raise FileNotFoundError(f"日志文件不存在: {self.log_file_path}")
        
        current_chapter = None
        chapter_start_line = None
        completed_chapters = []  # 存储已完成的章节，用于后续解析结束时间
        
        with open(self.log_file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                # 过滤设备专用日志的设备标识前缀
                # 格式: [DEVICE:android_172_16_37_174_5555] 原始日志内容
                if line.startswith('[DEVICE:'):
                    # 找到第一个]后的内容
                    prefix_end = line.find(']')
                    if prefix_end != -1:
                        line = line[prefix_end + 1:].strip()
                    else:
                        continue  # 如果格式不正确，跳过这行
                
                # 解析计划执行的章节数
                if '使用命令行参数: 测试到第' in line:
                    self._parse_planned_chapters(line)
                
                # 解析测试开始时间（全局测试开始，不是章节内的）
                elif '脚本开始时间:' in line and not current_chapter:
                    self._parse_test_start(line)
                
                # 解析章节开始（支持中文数字和阿拉伯数字）
                elif re.match(r'================第[一二三四五六七八九十\d]+章开始======================', line):
                    current_chapter = self._parse_chapter_start(line, line_num)
                    chapter_start_line = line_num
                    self.data['chapters'].append(current_chapter)
                
                # 解析章节开始时间（在章节开始后）
                elif ('脚本开始时间:' in line or re.search(r'第\d+章开始时间:', line)) and current_chapter and not current_chapter.get('start_time'):
                    self._parse_chapter_start_time(line, current_chapter)
                
                # 解析章节结束时间（在章节结束前）
                elif ('脚本结束时间:' in line or re.search(r'第\d+章结束时间:', line)) and current_chapter and not current_chapter.get('end_time'):
                    self._parse_chapter_end_time(line, current_chapter)
                
                # 解析章节步骤进度
                elif current_chapter and re.search(r'\d+ / \d+', line):
                    self._parse_chapter_step(line, current_chapter)
                
                # 解析章节结束（只匹配数字格式，避免重复）
                elif re.match(r'================第\d+章结束======================', line):
                    if current_chapter:
                        self._parse_chapter_end(line, current_chapter, chapter_start_line, line_num)
                        completed_chapters.append(current_chapter)  # 添加到已完成章节列表
                        # 不立即设置为None，让后续的脚本时间解析来处理
                        current_chapter = None
                
                # 解析章节结束时间（在章节结束后，用于处理没有章节结束标记的情况）
                elif ('脚本结束时间:' in line or re.search(r'第\d+章结束时间:', line)) and not current_chapter:
                    # 查找最后一个章节并设置结束时间
                    if self.data['chapters']:
                        last_chapter = self.data['chapters'][-1]
                        if not last_chapter.get('end_time'):
                            self._parse_chapter_end_time(line, last_chapter)
                
                # 解析章节结束时间（在章节结束后，用于处理已完成章节的结束时间）
                elif ('脚本结束时间:' in line or re.search(r'第\d+章结束时间:', line)) and completed_chapters:
                    # 查找最后一个没有结束时间的已完成章节
                    for chapter in reversed(completed_chapters):
                        if not chapter.get('end_time'):
                            self._parse_chapter_end_time(line, chapter)
                            break
                
                # 解析章节开始时间（在章节结束后，用于处理已完成章节的开始时间）
                elif ('脚本开始时间:' in line or re.search(r'第\d+章开始时间:', line)) and completed_chapters:
                    # 查找最后一个没有开始时间的已完成章节
                    for chapter in reversed(completed_chapters):
                        if not chapter.get('start_time'):
                            self._parse_chapter_start_time(line, chapter)
                            break
                
                # 解析操作组开始
                elif '====click_a_until_b_appear_list：' in line:
                    operation = self._parse_operation_group(line, line_num)
                    if current_chapter:
                        current_chapter['operations'].append(operation)
                    self.data['operations'].append(operation)
                
                # 解析操作结果
                elif ('click_element_safe 成功' in line or 
                      'click_until_disappear 成功' in line):
                    operation = self._parse_operation(line, line_num)
                    if current_chapter:
                        current_chapter['operations'].append(operation)
                    self.data['operations'].append(operation)
                
                # 解析操作失败
                elif ('click_element_safe 失败' in line or 
                      'click_until_disappear 失败' in line):
                    operation = self._parse_operation(line, line_num, success=False)
                    if current_chapter:
                        current_chapter['operations'].append(operation)
                    self.data['operations'].append(operation)
                
                # 解析异常
                elif '未知异常:' in line:
                    error = self._parse_error(line, line_num)
                    if current_chapter:
                        current_chapter['errors'].append(error)
                    self.data['errors'].append(error)
                
                # 解析测试结束
                elif ('脚本结束时间:' in line or re.search(r'第\d+章结束时间:', line)):
                    self._parse_test_end(line)
                elif '总耗时:' in line:
                    self._parse_test_end(line)
        
        # 计算汇总数据
        self._calculate_summary()
        self.total_operations = len(self.operations)
        
        # 后处理：统一解析章节的开始和结束时间
        self._post_process_chapter_times()
        
        # 后处理：查找整个测试的最终结束时间
        self._post_process_final_test_end()
        
        return self.data
    
    def _post_process_chapter_times(self):
        """后处理：统一解析章节的开始和结束时间"""
        with open(self.log_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 为每个章节查找开始和结束时间
        for chapter in self.data['chapters']:
            chapter_num = chapter['number']
            
            # 查找章节结束标记
            chapter_end_line = None
            for i, line in enumerate(lines):
                if re.match(rf'================第{chapter_num}章结束======================', line.strip()):
                    chapter_end_line = i
                    break
            
            if chapter_end_line is not None:
                # 在章节结束标记前查找开始和结束时间（向前搜索）
                for i in range(max(0, chapter_end_line - 10), chapter_end_line):
                    line = lines[i].strip()
                    if ('脚本开始时间:' in line or re.search(r'第\d+章开始时间:', line)) and not chapter.get('start_time'):
                        time_match = re.search(r'(?:脚本开始时间:|第\d+章开始时间:) (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
                        if time_match:
                            chapter['start_time'] = time_match.group(1)
                    elif ('脚本结束时间:' in line or re.search(r'第\d+章结束时间:', line)) and not chapter.get('end_time'):
                        time_match = re.search(r'(?:脚本结束时间:|第\d+章结束时间:) (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
                        if time_match:
                            chapter['end_time'] = time_match.group(1)
                            break
            
            # 计算章节耗时
            if chapter.get('start_time') and chapter.get('end_time') and not chapter.get('duration'):
                try:
                    start_dt = datetime.strptime(chapter['start_time'], '%Y-%m-%d %H:%M:%S')
                    end_dt = datetime.strptime(chapter['end_time'], '%Y-%m-%d %H:%M:%S')
                    duration = end_dt - start_dt
                    chapter['duration'] = self._format_duration(str(duration))
                except:
                    pass
    
    def _parse_planned_chapters(self, line: str):
        """解析计划执行的章节数"""
        # 解析格式: "📋 使用命令行参数: 测试到第7章"
        match = re.search(r'测试到第(\d+)章', line)
        if match:
            self.data['test_info']['planned_chapters'] = int(match.group(1))
    
    def _parse_test_start(self, line: str):
        """解析测试开始信息"""
        # 查找脚本开始时间
        time_match = re.search(r'脚本开始时间: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
        if time_match:
            self.data['test_info']['start_time'] = time_match.group(1)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """将中文数字转换为阿拉伯数字"""
        chinese_to_arabic_map = {
            '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
            '六': 6, '七': 7, '八': 8, '九': 9, '十': 10
        }
        
        # 如果是纯阿拉伯数字，直接转换
        if chinese_num.isdigit():
            return int(chinese_num)
        
        # 如果是中文数字，进行转换
        if chinese_num in chinese_to_arabic_map:
            return chinese_to_arabic_map[chinese_num]
        
        # 默认返回0
        return 0
    
    def _parse_chapter_start(self, line: str, line_num: int) -> Dict[str, Any]:
        """解析章节开始"""
        # 支持中文数字和阿拉伯数字
        chapter_match = re.search(r'第([一二三四五六七八九十\d]+)章', line)
        if chapter_match:
            chapter_str = chapter_match.group(1)
            # 转换中文数字为阿拉伯数字
            chapter_num = self._chinese_to_arabic(chapter_str)
        else:
            chapter_num = 0
        
        return {
            'number': chapter_num,
            'name': f'第{chapter_num}章',
            'start_line': line_num,
            'start_time': None,  # 初始化为None，等待后续解析
            'operations': [],
            'errors': [],
            'status': 'running'
        }
    
    def _parse_chapter_start_time(self, line: str, chapter: Dict[str, Any]):
        """解析章节开始时间"""
        time_match = re.search(r'(?:脚本开始时间:|第\d+章开始时间:) (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
        if time_match:
            chapter['start_time'] = time_match.group(1)
    
    def _parse_chapter_end_time(self, line: str, chapter: Dict[str, Any]):
        """解析章节结束时间"""
        time_match = re.search(r'(?:脚本结束时间:|第\d+章结束时间:) (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
        if time_match:
            chapter['end_time'] = time_match.group(1)
            # 计算章节耗时
            if chapter.get('start_time'):
                try:
                    start_dt = datetime.strptime(chapter['start_time'], '%Y-%m-%d %H:%M:%S')
                    end_dt = datetime.strptime(chapter['end_time'], '%Y-%m-%d %H:%M:%S')
                    duration = end_dt - start_dt
                    chapter['duration'] = str(duration)
                except:
                    pass

    def _parse_chapter_end(self, line: str, chapter: Dict[str, Any], start_line: int, end_line: int):
        """解析章节结束"""
        chapter['end_line'] = end_line
        # 不在这里设置结束时间，让后续的脚本结束时间解析来处理
        chapter['status'] = 'completed'
    
    def _parse_chapter_step(self, line: str, chapter: Dict[str, Any]):
        """解析章节步骤进度"""
        # 匹配格式: "1 / 36" 或 "36 / 36"
        step_match = re.search(r'(\d+) / (\d+)', line)
        if step_match:
            current_step = int(step_match.group(1))
            total_steps = int(step_match.group(2))
            
            # 初始化章节步骤统计
            if 'step_stats' not in chapter:
                chapter['step_stats'] = {
                    'step_groups': [],
                    'total_all_steps': 0,
                    'completed_all_steps': 0
                }
            
            # 检查是否已经处理过这个步骤组
            step_groups = chapter['step_stats']['step_groups']
            existing_group = None
            
            # 查找是否已经存在相同总步骤数的组
            for group in step_groups:
                if group['total'] == total_steps:
                    existing_group = group
                    break
            
            if existing_group:
                # 更新现有组
                existing_group['current'] = current_step
                existing_group['completed'] = current_step
                existing_group['progress'] = (current_step / total_steps) * 100
            else:
                # 创建新组
                new_group = {
                    'total': total_steps,
                    'current': current_step,
                    'completed': current_step,
                    'progress': (current_step / total_steps) * 100
                }
                step_groups.append(new_group)
            
            # 重新计算总进度
            total_all_steps = sum(group['total'] for group in step_groups)
            completed_all_steps = sum(group['completed'] for group in step_groups)
            
            chapter['step_stats']['total_all_steps'] = total_all_steps
            chapter['step_stats']['completed_all_steps'] = completed_all_steps
    
    def _parse_operation_group(self, line: str, line_num: int) -> Dict[str, Any]:
        """解析操作组记录"""
        # 提取操作组名称
        group_match = re.search(r'====click_a_until_b_appear_list：([^=]+)====', line)
        group_name = group_match.group(1) if group_match else 'unknown'
        
        return {
            'type': 'click_a_until_b_appear_list',
            'locator': f'操作组: {group_name}',
            'focus': '批量操作',
            'success': True,
            'line_num': line_num,
            'time': f'L{line_num}',
            'line': line,
            'group_name': group_name
        }
    
    def _parse_operation(self, line: str, line_num: int, success: bool = True) -> Dict[str, Any]:
        """解析操作记录"""
        # 提取操作类型
        if 'click_element_safe' in line:
            op_type = 'click_element_safe'
        elif 'click_until_disappear' in line:
            op_type = 'click_until_disappear'
        else:
            op_type = 'unknown'
        
        # 提取locator信息
        locator_match = re.search(r"'locator': '([^']+)'", line)
        locator = locator_match.group(1) if locator_match else 'unknown'
        
        # 提取focus位置信息
        focus_match = re.search(r"'focus': \(([^)]+)\)", line)
        focus = focus_match.group(1) if focus_match else 'unknown'
        
        return {
            'type': op_type,
            'locator': locator,
            'focus': focus,
            'success': success,
            'line_num': line_num,
            'time': f'L{line_num}',
            'line': line
        }
    
    def _parse_error(self, line: str, line_num: int) -> Dict[str, Any]:
        """解析异常记录"""
        # 提取异常信息
        error_match = re.search(r'未知异常: (.+)', line)
        error_message = error_match.group(1) if error_match else '未知异常'
        
        return {
            'message': error_message,
            'line_num': line_num,
            'time': f'L{line_num}',
            'line': line
        }
    
    def _parse_test_end(self, line: str):
        """解析测试结束信息"""
        # 查找脚本结束时间
        time_match = re.search(r'(?:脚本结束时间:|第\d+章结束时间:) (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
        if time_match:
            self.data['test_info']['end_time'] = time_match.group(1)
        
        # 提取总耗时
        duration_match = re.search(r'总耗时: (.+)', line)
        if duration_match:
            raw_duration = duration_match.group(1)
            self.data['test_info']['total_duration'] = self._format_duration(raw_duration)
    
    def _post_process_final_test_end(self):
        """后处理：查找整个测试的最终结束时间"""
        with open(self.log_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 从后往前查找"测试结束"标记
        test_end_found = False
        for i in range(len(lines) - 1, -1, -1):
            line = lines[i].strip()
            
            if '测试结束' in line:
                test_end_found = True
                # 在"测试结束"标记前查找脚本结束时间和总耗时
                for j in range(max(0, i - 5), i):
                    prev_line = lines[j].strip()
                    
                    # 查找脚本结束时间
                    time_match = re.search(r'(?:脚本结束时间:|第\d+章结束时间:) (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', prev_line)
                    if time_match:
                        self.data['test_info']['end_time'] = time_match.group(1)
                    
                    # 查找总耗时
                    duration_match = re.search(r'总耗时: (.+)', prev_line)
                    if duration_match:
                        raw_duration = duration_match.group(1)
                        self.data['test_info']['total_duration'] = self._format_duration(raw_duration)
                break
        
        # 如果没有找到"测试结束"标记，使用最后一个脚本结束时间
        if not test_end_found:
            for i in range(len(lines) - 1, -1, -1):
                line = lines[i].strip()
                if ('脚本结束时间:' in line or re.search(r'第\d+章结束时间:', line)):
                    time_match = re.search(r'(?:脚本结束时间:|第\d+章结束时间:) (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
                    if time_match:
                        self.data['test_info']['end_time'] = time_match.group(1)
                        break
                elif '总耗时:' in line:
                    duration_match = re.search(r'总耗时: (.+)', line)
                    if duration_match:
                        raw_duration = duration_match.group(1)
                        self.data['test_info']['total_duration'] = self._format_duration(raw_duration)
                        break
    
    def _extract_time_from_line(self, line: str) -> str:
        """从日志行中提取时间"""
        time_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
        return time_match.group(1) if time_match else ''
    
    def _calculate_duration(self, start_time: str, end_time: str) -> int:
        """计算持续时间（秒）"""
        try:
            start = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            end = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
            return int((end - start).total_seconds())
        except:
            return 0
    
    def _format_duration(self, duration_str: str) -> str:
        """格式化持续时间，将 0:07:23.554893 格式转换为 00:07:23"""
        try:
            # 解析时间字符串，去掉微秒部分
            if '.' in duration_str:
                duration_str = duration_str.split('.')[0]
            
            # 分割时:分:秒
            parts = duration_str.split(':')
            if len(parts) == 3:
                hours, minutes, seconds = parts
                # 确保格式为两位数
                hours = hours.zfill(2)
                minutes = minutes.zfill(2)
                seconds = seconds.zfill(2)
                return f"{hours}:{minutes}:{seconds}"
            else:
                return duration_str
        except:
            return duration_str
    
    def _calculate_summary(self):
        """计算汇总数据"""
        chapters = self.data['chapters']
        operations = self.data['operations']
        errors = self.data['errors']
        
        # 后处理：检查没有明确结束标记的章节，如果它们有完整的步骤执行，则标记为完成
        for chapter in chapters:
            if chapter['status'] != 'completed' and 'step_stats' in chapter:
                step_stats = chapter['step_stats']
                # 如果章节有步骤统计且所有步骤都完成了，标记为完成
                if (step_stats.get('total_all_steps', 0) > 0 and 
                    step_stats.get('completed_all_steps', 0) >= step_stats.get('total_all_steps', 0)):
                    chapter['status'] = 'completed'
                    print(f"📝 第{chapter['number']}章：根据步骤完成情况标记为成功")
        
        # 章节统计
        completed_chapters = [c for c in chapters if c['status'] == 'completed']
        failed_chapters = [c for c in chapters if c['status'] != 'completed']
        
        # 操作统计
        successful_operations = [op for op in operations if op['success']]
        failed_operations = [op for op in operations if not op['success']]
        
        # 操作类型统计
        click_safe_count = len([op for op in operations if op['type'] == 'click_element_safe'])
        click_disappear_count = len([op for op in operations if op['type'] == 'click_until_disappear'])
        click_a_until_b_count = len([op for op in operations if op['type'] == 'click_a_until_b_appear_list'])
        
        # 计算通过率（基于配置文件中的计划章节数）
        planned_chapters = self.planned_chapters
        
        if planned_chapters > 0:
            # 计算每章的实际进度
            chapter_progress = []
            for i in range(1, planned_chapters + 1):
                chapter = next((c for c in chapters if c['number'] == i), None)
                if chapter:
                    if chapter['status'] == 'completed':
                        progress = 100
                    elif 'step_stats' in chapter:
                        # 使用预计步骤数计算进度
                        step_stats = chapter['step_stats']
                        expected_steps = self.expected_steps.get(i, 0)
                        
                        if expected_steps > 0:
                            # 使用预计步骤数作为分母
                            progress = (step_stats['completed_all_steps'] / expected_steps) * 100
                        elif step_stats['total_all_steps'] > 0:
                            # 如果没有预计步骤数，使用实际总步骤数
                            progress = (step_stats['completed_all_steps'] / step_stats['total_all_steps']) * 100
                        else:
                            progress = 0
                    else:
                        progress = 0
                else:
                    progress = 0
                chapter_progress.append(progress)
            
            # 计算总体通过率（基于章节完成情况）
            completed_count = len([p for p in chapter_progress if p == 100])
            success_rate = (completed_count / planned_chapters) * 100
        else:
            success_rate = 0
            chapter_progress = []
        
        self.data['summary'] = {
            'planned_chapters': planned_chapters,
            'total_chapters': len(chapters),
            'completed_chapters': len(completed_chapters),
            'failed_chapters': len(failed_chapters),
            'total_operations': len(operations),
            'successful_operations': len(successful_operations),
            'failed_operations': len(failed_operations),
            'total_errors': len(errors),
            'click_safe_count': click_safe_count,
            'click_disappear_count': click_disappear_count,
            'click_a_until_b_count': click_a_until_b_count,
            'success_rate': round(success_rate, 1),
            'chapter_progress': chapter_progress
        }


class HTMLReportGenerator:
    """HTML报告生成器"""
    
    def __init__(self, template_path: Optional[str] = None):
        self.template_path = template_path or self._get_default_template()
    
    def generate(self, log_data: Dict[str, Any], output_path: str) -> str:
        """生成HTML报告"""
        html_content = self._load_template()
        
        # 替换模板变量
        html_content = self._replace_template_variables(html_content, log_data)
        
        # 写入文件
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
    
    def _get_default_template(self) -> str:
        """获取默认模板路径"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_dir, 'report_template.html')
    
    def _load_template(self) -> str:
        """加载HTML模板"""
        if os.path.exists(self.template_path):
            with open(self.template_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            # 如果模板文件不存在，使用内嵌模板
            return self._get_embedded_template()
    
    def _replace_template_variables(self, template: str, data: Dict[str, Any]) -> str:
        """替换模板变量"""
        # 基本信息
        template = template.replace('{{TEST_START_TIME}}', data['test_info'].get('start_time', ''))
        template = template.replace('{{TEST_END_TIME}}', data['test_info'].get('end_time', ''))
        template = template.replace('{{TOTAL_DURATION}}', data['test_info'].get('total_duration', ''))
        
        # 设备信息
        device_info = data.get('device_info', {})
        template = template.replace('{{DEVICE_NAME}}', device_info.get('device_name', '未知设备'))
        template = template.replace('{{DEVICE_ID}}', device_info.get('device_id', '未知'))
        template = template.replace('{{DEVICE_TYPE}}', device_info.get('device_type', '未知'))
        template = template.replace('{{WS_PORT}}', device_info.get('ws_port', '未知'))
        
        # 汇总数据
        summary = data['summary']
        template = template.replace('{{COMPLETED_CHAPTERS}}', str(summary['completed_chapters']))
        template = template.replace('{{FAILED_CHAPTERS}}', str(summary['failed_chapters']))
        template = template.replace('{{TOTAL_OPERATIONS}}', str(summary['total_operations']))
        template = template.replace('{{TOTAL_ERRORS}}', str(summary['total_errors']))
        template = template.replace('{{SUCCESS_RATE}}', str(summary['success_rate']))
        
        # 根据通过率确定颜色类
        success_rate = summary['success_rate']
        if success_rate >= 80:
            success_rate_color_class = 'success'  # 绿色 - 80%以上
        elif success_rate >= 60:
            success_rate_color_class = 'warning'  # 黄色 - 60%-80%
        else:
            success_rate_color_class = 'danger'   # 红色 - 60%以下
        template = template.replace('{{SUCCESS_RATE_COLOR_CLASS}}', success_rate_color_class)
        
        # 生成章节HTML
        chapters_html = self._generate_chapters_html(data['chapters'])
        template = template.replace('{{CHAPTERS_HTML}}', chapters_html)
        
        # 生成时间线HTML
        timeline_html = self._generate_timeline_html(data)
        template = template.replace('{{TIMELINE_HTML}}', timeline_html)
        
        # 生成统计图表HTML
        charts_html = self._generate_charts_html(data)
        template = template.replace('{{CHARTS_HTML}}', charts_html)
        
        return template
    
    def _generate_chapters_html(self, chapters: List[Dict[str, Any]]) -> str:
        """生成章节HTML"""
        html = ""
        for chapter in chapters:
            status_class = 'status-success' if chapter['status'] == 'completed' else 'status-failed'
            status_text = '成功' if chapter['status'] == 'completed' else '失败'
            
            operations_html = ""
            for op in chapter['operations']:
                op_class = 'operation-item' if op['success'] else 'operation-item failed'
                operations_html += f"""
                <div class="{op_class}">
                    <div class="operation-type">{op['type']}</div>
                    <div class="operation-details">定位器: {op['locator']} | 焦点: {op['focus']}</div>
                </div>
                """
            
            errors_html = ""
            if chapter['errors']:
                errors_html = '<div class="error-list">'
                for error in chapter['errors']:
                    errors_html += f"""
                    <div class="error-item">
                        <div class="error-time">{error['time']}</div>
                        <div class="error-message">{error['message']}</div>
                    </div>
                    """
                errors_html += '</div>'
            
            html += f"""
            <div class="chapter-card">
                <div class="chapter-header" onclick="toggleChapter('chapter{chapter['number']}')">
                    <h3>第{chapter['number']}章</h3>
                    <div class="chapter-status {status_class}">{status_text}</div>
                </div>
                <div id="chapter{chapter['number']}" class="chapter-content">
                    <div class="operation-list">
                        {operations_html}
                    </div>
                    {errors_html}
                </div>
            </div>
            """
        
        return html
    
    def _generate_timeline_html(self, data: Dict[str, Any]) -> str:
        """生成时间线HTML"""
        html = ""
        
        # 测试开始
        if data['test_info'].get('start_time'):
            html += f"""
            <div class="timeline-item">
                <div class="timeline-time">{data['test_info']['start_time']}</div>
                <div class="timeline-title">测试开始</div>
                <div>初始化设备连接，开始执行测试</div>
            </div>
            """
        
        # 章节时间线
        for chapter in data['chapters']:
            if chapter.get('start_time'):
                html += f"""
                <div class="timeline-item">
                    <div class="timeline-time">{chapter['start_time']}</div>
                    <div class="timeline-title">第{chapter['number']}章开始</div>
                    <div>开始执行第{chapter['number']}章测试</div>
                </div>
                """
            
            if chapter.get('end_time'):
                status_text = "成功完成" if chapter['status'] == 'completed' else "异常中断"
                duration_text = f"，耗时: {chapter.get('duration', '')}" if chapter.get('duration') else ""
                html += f"""
                <div class="timeline-item">
                    <div class="timeline-time">{chapter['end_time']}</div>
                    <div class="timeline-title">第{chapter['number']}章{status_text}</div>
                    <div>第{chapter['number']}章{status_text}{duration_text}</div>
                </div>
                """
            elif chapter.get('start_time') and chapter['status'] != 'completed':
                # 如果章节开始了但没有结束时间，显示异常中断
                html += f"""
                <div class="timeline-item">
                    <div class="timeline-time">L{chapter.get('end_line', '?')}</div>
                    <div class="timeline-title">第{chapter['number']}章异常中断</div>
                    <div>第{chapter['number']}章异常中断</div>
                </div>
                """
        
        # 测试结束
        if data['test_info'].get('end_time'):
            html += f"""
            <div class="timeline-item">
                <div class="timeline-time">{data['test_info']['end_time']}</div>
                <div class="timeline-title">测试结束</div>
                <div>测试执行完成，总耗时: {data['test_info'].get('total_duration', '')}</div>
            </div>
            """
        
        return html
    
    def _generate_charts_html(self, data: Dict[str, Any]) -> str:
        """生成统计图表HTML"""
        summary = data['summary']
        planned_chapters = summary.get('planned_chapters', 7)  # 默认7章
        
        # 章节完成情况 - 显示所有计划章节
        chapters_html = ""
        chapter_progress = data['summary'].get('chapter_progress', [])
        
        for chapter_num in range(1, planned_chapters + 1):
            # 获取章节进度
            if chapter_num <= len(chapter_progress):
                progress = chapter_progress[chapter_num - 1]
            else:
                progress = 0
            
            # 查找对应的章节数据
            chapter_data = next((c for c in data['chapters'] if c['number'] == chapter_num), None)
            
            # 根据进度百分比确定颜色和状态
            if progress == 100:
                color = "#28a745"  # 绿色 - 完成
                status_text = "100%"
                progress_width = 100.0
            elif progress > 0:
                color = "#007bff"  # 蓝色 - 进行中
                status_text = f"{progress:.1f}%"
                progress_width = progress
            else:
                color = "#dc3545"  # 红色 - 未开始或失败
                status_text = "0%"
                progress_width = 0.0
            
            # 为0%进度添加特殊样式，让红色更明显
            if progress == 0:
                progress_bar_html = f"""
                <div class="progress-bar" style="background: #f8f9fa; border: 2px solid #dc3545; position: relative;">
                    <div class="progress-fill" style="width: 0%; background: #dc3545; opacity: 0.3;"></div>
                    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #dc3545; font-weight: bold; font-size: 12px;">未开始</div>
                </div>
                """
            else:
                progress_bar_html = f"""
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress_width:.1f}%; background: {color};"></div>
                </div>
                """
            
            chapters_html += f"""
            <div style="margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>第{chapter_num}章</span>
                    <span>{status_text}</span>
                </div>
                {progress_bar_html}
            </div>
            """
        
        # 操作类型统计
        total_ops = summary['total_operations']
        click_safe_percent = (summary['click_safe_count'] / total_ops * 100) if total_ops > 0 else 0
        click_disappear_percent = (summary['click_disappear_count'] / total_ops * 100) if total_ops > 0 else 0
        click_a_until_b_percent = (summary['click_a_until_b_count'] / total_ops * 100) if total_ops > 0 else 0
        
        # 计算饼图角度
        click_safe_angle = click_safe_percent * 3.6  # 360度 / 100%
        click_disappear_angle = click_disappear_percent * 3.6
        click_a_until_b_angle = click_a_until_b_percent * 3.6
        
        operations_html = f"""
        <div class="pie-chart-container">
            <div class="pie-chart" style="--color-1: #4CAF50; --color-2: #2196F3; --color-3: #FF9800; --angle-1: {click_safe_angle:.1f}deg; --angle-2: {click_safe_angle + click_disappear_angle:.1f}deg;"></div>
            <div class="pie-legend">
                <div class="legend-item">
                    <div class="legend-color" style="background: #4CAF50;"></div>
                    <span>click_element_safe: {summary['click_safe_count']}次 ({click_safe_percent:.1f}%)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #2196F3;"></div>
                    <span>click_until_disappear: {summary['click_disappear_count']}次 ({click_disappear_percent:.1f}%)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #FF9800;"></div>
                    <span>click_a_until_b_appear_list: {summary['click_a_until_b_count']}次 ({click_a_until_b_percent:.1f}%)</span>
                </div>
            </div>
        </div>
        """
        
        return f"""
        <div class="chart-container">
            <h3 class="chart-title">章节完成情况</h3>
            {chapters_html}
        </div>
        <div class="chart-container">
            <h3 class="chart-title">操作类型统计</h3>
            {operations_html}
        </div>
        """
    
    def _get_embedded_template(self) -> str:
        """获取内嵌的HTML模板"""
        return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cocos UI自动化测试报告</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #007bff 0%, #0056b3 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header .subtitle { font-size: 1.2em; opacity: 0.9; }
        .stats-grid { display: grid; grid-template-columns: 1fr; gap: 20px; margin-bottom: 30px; justify-items: center; }
        .stat-card { background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); text-align: center; transition: transform 0.3s ease; }
        .stat-card:hover { transform: translateY(-5px); }
        .stat-card .icon { font-size: 3em; margin-bottom: 15px; }
        .stat-card .number { font-size: 2.5em; font-weight: bold; margin-bottom: 10px; }
        .stat-card .label { color: #666; font-size: 1.1em; }
        .success-rate-card { width: 100%; }
        .success-rate-card .sub-stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee; }
        .sub-stat { text-align: center; }
        .sub-stat .sub-number { display: block; font-size: 1.5em; font-weight: bold; color: #333; }
        .sub-stat .sub-label { display: block; font-size: 0.9em; color: #666; margin-top: 5px; }
        .success { color: #28a745; }
        .warning { color: #ffc107; }
        .danger { color: #dc3545; }
        .info { color: #17a2b8; }
        .tabs { background: white; border-radius: 10px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); margin-bottom: 30px; }
        .tab-nav { display: flex; border-bottom: 1px solid #eee; }
        .tab-nav button { flex: 1; padding: 15px 20px; border: none; background: none; cursor: pointer; font-size: 1.1em; transition: all 0.3s ease; }
        .tab-nav button.active { background: #007bff; color: white; border-radius: 10px 10px 0 0; }
        .tab-content { padding: 30px; }
        .tab-panel { display: none; }
        .tab-panel.active { display: block; }
        .chapter-card { background: white; border-radius: 10px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); margin-bottom: 20px; overflow: hidden; }
        .chapter-header { background: #f8f9fa; padding: 20px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; transition: background-color 0.3s ease; }
        .chapter-header:hover { background: #e9ecef; }
        .chapter-header h3 { font-size: 1.3em; color: #333; }
        .chapter-status { padding: 5px 15px; border-radius: 20px; font-size: 0.9em; font-weight: bold; }
        .status-success { background: #d4edda; color: #155724; }
        .status-failed { background: #f8d7da; color: #721c24; }
        .chapter-content { padding: 20px; border-top: 1px solid #eee; display: none; }
        .chapter-content.expanded { display: block; }
        .operation-list { max-height: 400px; overflow-y: auto; }
        .operation-item { padding: 10px 15px; border-left: 4px solid #28a745; background: #f8f9fa; margin-bottom: 10px; border-radius: 0 5px 5px 0; }
        .operation-item.failed { border-left-color: #dc3545; background: #f8d7da; }
        .operation-item .operation-type { font-weight: bold; color: #495057; }
        .operation-item .operation-details { font-size: 0.9em; color: #6c757d; margin-top: 5px; }
        .error-list { background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 5px; padding: 15px; margin-top: 15px; }
        .error-item { padding: 10px; background: white; border-radius: 5px; margin-bottom: 10px; border-left: 4px solid #dc3545; }
        .error-item:last-child { margin-bottom: 0; }
        .error-time { font-size: 0.9em; color: #6c757d; }
        .error-message { font-weight: bold; color: #721c24; margin-top: 5px; }
        .chart-container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); margin-bottom: 30px; }
        .chart-title { font-size: 1.5em; margin-bottom: 20px; color: #333; }
        .progress-bar { background: #e9ecef; border-radius: 10px; height: 20px; margin: 10px 0; overflow: hidden; }
        .progress-fill { height: 100%; background: linear-gradient(90deg, #28a745, #20c997); border-radius: 10px; transition: width 0.3s ease; }
        .pie-chart-container { display: flex; align-items: center; gap: 20px; margin: 20px 0; }
        .pie-chart { width: 200px; height: 200px; border-radius: 50%; position: relative; background: conic-gradient(var(--color-1) 0deg var(--angle-1), var(--color-2) var(--angle-1) var(--angle-2), var(--color-3) var(--angle-2) 360deg); box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        .pie-chart::before { content: ''; position: absolute; top: 50%; left: 50%; width: 80px; height: 80px; background: white; border-radius: 50%; transform: translate(-50%, -50%); box-shadow: inset 0 2px 4px rgba(0,0,0,0.1); }
        .pie-legend { flex: 1; }
        .legend-item { display: flex; align-items: center; margin-bottom: 12px; font-size: 14px; }
        .legend-color { width: 16px; height: 16px; border-radius: 3px; margin-right: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.2); }
        .timeline { position: relative; padding-left: 30px; }
        .timeline::before { content: ''; position: absolute; left: 15px; top: 0; bottom: 0; width: 2px; background: #007bff; }
        .timeline-item { position: relative; margin-bottom: 30px; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); }
        .timeline-item::before { content: ''; position: absolute; left: -22px; top: 20px; width: 12px; height: 12px; background: #007bff; border-radius: 50%; border: 3px solid white; }
        .timeline-time { font-size: 0.9em; color: #6c757d; margin-bottom: 5px; }
        .timeline-title { font-weight: bold; color: #333; margin-bottom: 10px; }
        .search-box { width: 100%; padding: 15px; border: 1px solid #ddd; border-radius: 10px; font-size: 1.1em; margin-bottom: 20px; }
        .search-box:focus { outline: none; border-color: #007bff; box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1); }
        @media (max-width: 768px) { .container { padding: 10px; } .header h1 { font-size: 2em; } .stats-grid { grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); } .tab-nav { flex-direction: column; } .tab-nav button { border-radius: 0; } .tab-nav button.active { border-radius: 0; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Cocos UI自动化测试报告</h1>
            <div class="subtitle">
                测试时间: {{TEST_START_TIME}} - {{TEST_END_TIME}} | 总耗时: {{TOTAL_DURATION}}
            </div>
            <div class="device-info" style="margin-top: 15px; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; font-size: 0.95em;">
                    <div><strong>设备名称:</strong> {{DEVICE_NAME}}</div>
                    <div><strong>设备ID:</strong> {{DEVICE_ID}}</div>
                    <div><strong>设备类型:</strong> {{DEVICE_TYPE}}</div>
                    <div><strong>WebSocket端口:</strong> {{WS_PORT}}</div>
                </div>
            </div>
        </div>
        <div class="stats-grid">
            <div class="stat-card success-rate-card">
                <div class="icon {{SUCCESS_RATE_COLOR_CLASS}}">●</div>
                <div class="number {{SUCCESS_RATE_COLOR_CLASS}}">{{SUCCESS_RATE}}%</div>
                <div class="label">测试通过率</div>
                <div class="sub-stats">
                    <div class="sub-stat">
                        <span class="sub-number">{{COMPLETED_CHAPTERS}}</span>
                        <span class="sub-label">成功章节</span>
                    </div>
                    <div class="sub-stat">
                        <span class="sub-number">{{FAILED_CHAPTERS}}</span>
                        <span class="sub-label">失败章节</span>
                    </div>
                    <div class="sub-stat">
                        <span class="sub-number">{{TOTAL_OPERATIONS}}</span>
                        <span class="sub-label">总操作</span>
                    </div>
                    <div class="sub-stat">
                        <span class="sub-number">{{TOTAL_ERRORS}}</span>
                        <span class="sub-label">异常</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="tabs">
            <div class="tab-nav">
                <button class="tab-btn active" onclick="showTab('overview')">概览</button>
                <button class="tab-btn" onclick="showTab('chapters')">章节详情</button>
                <button class="tab-btn" onclick="showTab('timeline')">时间线</button>
            </div>
            <div class="tab-content">
                <div id="overview" class="tab-panel active">
                    <h2>测试概览</h2>
                    <p>本次测试通过率为 {{SUCCESS_RATE}}%，共执行 {{COMPLETED_CHAPTERS}} 个成功章节，{{FAILED_CHAPTERS}} 个失败章节。</p>
                    {{CHARTS_HTML}}
                </div>
                <div id="chapters" class="tab-panel">
                    <h2>章节详情</h2>
                    <input type="text" class="search-box" placeholder="搜索操作步骤..." onkeyup="filterOperations(this.value)">
                    {{CHAPTERS_HTML}}
                </div>
                <div id="timeline" class="tab-panel">
                    <h2>执行时间线</h2>
                    <div class="timeline">
                        {{TIMELINE_HTML}}
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script>
        function showTab(tabName) {
            const panels = document.querySelectorAll('.tab-panel');
            panels.forEach(panel => panel.classList.remove('active'));
            const buttons = document.querySelectorAll('.tab-btn');
            buttons.forEach(btn => btn.classList.remove('active'));
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }
        function toggleChapter(chapterId) {
            const content = document.getElementById(chapterId);
            if (content.classList.contains('expanded')) {
                content.classList.remove('expanded');
            } else {
                content.classList.add('expanded');
            }
        }
        function filterOperations(searchTerm) {
            const operationItems = document.querySelectorAll('.operation-item');
            const searchLower = searchTerm.toLowerCase();
            operationItems.forEach(item => {
                const text = item.textContent.toLowerCase();
                if (text.includes(searchLower)) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        }
    </script>
</body>
</html>'''


class TestReportGenerator:
    """测试报告生成器主类"""
    
    def __init__(self, log_file_path: str = None, output_dir: str = "reports"):
        self.log_file_path = log_file_path
        self.output_dir = output_dir
        self.parser = None
        self.html_generator = HTMLReportGenerator()
        
        # 如果没有指定日志文件路径，自动检测最新的日志文件
        if self.log_file_path is None:
            self.log_file_path = self._find_latest_log_file()
        
        if self.log_file_path:
            self.parser = LogParser(self.log_file_path, "test_config.yaml")
        else:
            raise ValueError("未找到日志文件")
    
    def _find_latest_log_file(self) -> Optional[str]:
        """自动查找最新的日志文件"""
        logs_dir = "logs"
        if not os.path.exists(logs_dir):
            return None
        
        # 优先查找设备专用日志文件
        device_log_pattern = os.path.join(logs_dir, "device_*.log")
        device_log_files = glob.glob(device_log_pattern)
        
        if device_log_files:
            # 按修改时间排序，返回最新的设备日志文件
            latest_file = max(device_log_files, key=os.path.getmtime)
            return latest_file
        
        # 如果没有设备日志文件，查找传统的run_*.log文件
        run_log_pattern = os.path.join(logs_dir, "run_*.log")
        run_log_files = glob.glob(run_log_pattern)
        
        if run_log_files:
            # 按修改时间排序，返回最新的文件
            latest_file = max(run_log_files, key=os.path.getmtime)
            return latest_file
        
        return None
    
    @staticmethod
    def find_latest_log_file(logs_dir: str = "logs") -> Optional[str]:
        """静态方法：查找最新的日志文件"""
        if not os.path.exists(logs_dir):
            return None
        
        # 优先查找设备专用日志文件
        device_log_pattern = os.path.join(logs_dir, "device_*.log")
        device_log_files = glob.glob(device_log_pattern)
        
        if device_log_files:
            # 按修改时间排序，返回最新的设备日志文件
            latest_file = max(device_log_files, key=os.path.getmtime)
            return latest_file
        
        # 如果没有设备日志文件，查找传统的run_*.log文件
        run_log_pattern = os.path.join(logs_dir, "run_*.log")
        run_log_files = glob.glob(run_log_pattern)
        
        if run_log_files:
            # 按修改时间排序，返回最新的文件
            latest_file = max(run_log_files, key=os.path.getmtime)
            return latest_file
        
        return None
    
    def generate_report(self) -> str:
        """生成测试报告"""
        try:
            # 解析日志文件
            log_data = self.parser.parse()
            
            # 添加设备信息到日志数据
            log_data['device_info'] = self.parser.device_info
            
            # 生成输出文件名（包含设备信息）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            device_type = self.parser.device_info.get('device_type', 'unknown')
            device_id = self.parser.device_info.get('device_id', 'unknown').replace(':', '_').replace('.', '_')
            output_filename = f"test_report_{device_type}_{device_id}_{timestamp}.html"
            output_path = os.path.join(self.output_dir, output_filename)
            
            # 生成HTML报告
            report_path = self.html_generator.generate(log_data, output_path)
            
            return report_path
            
        except Exception as e:
            raise Exception(f"生成测试报告失败: {str(e)}")
    
    def get_report_summary(self) -> Dict[str, Any]:
        """获取报告摘要信息"""
        try:
            log_data = self.parser.parse()
            return {
                'success': True,
                'summary': log_data['summary'],
                'test_info': log_data['test_info'],
                'total_chapters': len(log_data['chapters']),
                'total_operations': len(log_data['operations']),
                'total_errors': len(log_data['errors'])
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


def main():
    """主函数：支持命令行参数"""
    parser = argparse.ArgumentParser(description='生成Cocos UI自动化测试报告')
    parser.add_argument('-l', '--log-file', 
                       help='指定日志文件路径（如果不指定，将自动使用最新的日志文件）')
    parser.add_argument('-o', '--output-dir', 
                       default='reports',
                       help='输出目录（默认：reports）')
    parser.add_argument('--logs-dir', 
                       default='logs',
                       help='日志文件目录（默认：logs）')
    
    args = parser.parse_args()
    
    try:
        # 如果没有指定日志文件，自动查找最新的
        if args.log_file:
            log_file = args.log_file
            print(f"使用指定的日志文件: {log_file}")
        else:
            log_file = TestReportGenerator.find_latest_log_file(args.logs_dir)
            if not log_file:
                print(f"错误：在 {args.logs_dir} 目录中未找到日志文件")
                return 1
            print(f"自动检测到最新日志文件: {log_file}")
        
        # 创建报告生成器
        generator = TestReportGenerator(log_file, args.output_dir)
        
        # 生成报告
        report_path = generator.generate_report()
        print(f"测试报告生成成功: {report_path}")
        
        # 显示报告摘要
        summary = generator.get_report_summary()
        if summary['success']:
            print(f"报告摘要: {summary['summary']}")
        else:
            print(f"获取摘要失败: {summary['error']}")
            
        return 0
        
    except Exception as e:
        print(f"生成报告失败: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
