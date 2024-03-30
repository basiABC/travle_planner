import os
import sys
import time
import subprocess
import json
# 获取main.py脚本的目录路径
current_directory = os.path.dirname(os.path.abspath(__file__))

# 构造hotel_note项目的目录路径
hotel_note_directory = os.path.join(current_directory, 'hotel_note')

# 确保hotel_note目录存在
if not os.path.exists(hotel_note_directory):
    print("hotel_note项目目录不存在")
    sys.exit(1)

os.chdir(hotel_note_directory)
city_name='宁波'
commands = [
    'scrapy crawl cityid',
    'scrapy crawl hotel_search -a tag={}'.format(city_name),
    'scrapy crawl travel_note -a tag={}'.format(city_name)
]

for cmd in commands:
    process = subprocess.Popen(cmd.split(), cwd=current_directory)
    process.wait()  # 等待命令执行完成
    time.sleep(2)


current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)  # 改变工作目录到包含 scrapy.cfg 的目录
print("当前工作目录:", os.getcwd())
with open('hotel.json', 'r',encoding='utf-8') as file:
        # 加载JSON内容
        data = json.load(file)
        
        print(json.dumps(data, ensure_ascii=False, indent=4))


