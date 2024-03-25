import os
import sys
import time
import subprocess

# 获取main.py脚本的目录路径
current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)  # 改变工作目录到包含 scrapy.cfg 的目录

commands = [
    'scrapy crawl cityid',
    'scrapy crawl hotel_search -a tag=宁波',
    'scrapy crawl travel_note -a tag=宁波'
]

for cmd in commands:
    process = subprocess.Popen(cmd.split(), cwd=current_directory)
    process.wait()  # 等待命令执行完成
    time.sleep(2)
