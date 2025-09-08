import sys
import os
from datetime import datetime

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
    def write(self, message):
        self.file.write(message)
        self.file.flush()
    def flush(self):
        self.file.flush()
    def close(self):
        self.file.close()
# ...existing code...