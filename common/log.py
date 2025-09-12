import sys
import os
from datetime import datetime
from .report_generator import TestReportGenerator

# class LoggerWriter:
#     def __init__(self, log_file_path):
#         self.terminal = sys.stdout
#         self.log = open(log_file_path, "a", encoding="utf-8")

#     def write(self, message):
#         self.terminal.write(message)
#         self.log.write(message)

#     def flush(self):
#         self.terminal.flush()
#         self.log.flush()

# ...existing code...
class LoggerWriter:
    def __init__(self, filename):
        self.file = open(filename, "a", encoding="utf-8", errors="replace")  # 加 errors="replace"
        self.log_file_path = filename
        self.report_generated = False
    
    def write(self, message):
        self.file.write(message)
        self.file.flush()
        
        # 检测测试结束，自动生成报告
        if "测试结束" in message and not self.report_generated:
            self._generate_test_report()
    
    def flush(self):
        self.file.flush()
    
    def close(self):
        # 先关闭文件，确保所有内容都已写入
        self.file.close()
        
        # 在文件关闭后生成报告，确保时间信息完整
        if not self.report_generated:
            self._generate_test_report()
    
    def _generate_test_report(self):
        """生成测试报告"""
        try:
            # 确保reports目录存在
            reports_dir = os.path.join(os.path.dirname(os.path.dirname(self.log_file_path)), "reports")
            os.makedirs(reports_dir, exist_ok=True)
            
            # 生成报告
            generator = TestReportGenerator(self.log_file_path, reports_dir)
            report_path = generator.generate_report()
            
            # 获取报告摘要
            summary = generator.get_report_summary()
            
            if summary['success']:
                stats = summary['summary']
                report_message = f"""
                
==================== 测试报告生成完成 ====================
📄 HTML报告已生成: {report_path}
💡 请在浏览器中打开查看详细报告

========================================================
"""
            else:
                report_message = f"""
                
==================== 报告生成失败 ====================
❌ 生成报告时出现错误: {summary['error']}
📄 日志文件位置: {self.log_file_path}

====================================================
"""
            
            # 只打印到控制台，不再写入已关闭的文件
            print(report_message)
            
            self.report_generated = True
            
        except Exception as e:
            error_message = f"""
            
==================== 报告生成异常 ====================
❌ 生成报告时出现异常: {str(e)}
📄 日志文件位置: {self.log_file_path}

====================================================
"""
            # 只打印到控制台
            print(error_message)
            self.report_generated = True
# ...existing code...