import json
import requests
from bs4 import BeautifulSoup
import os
import sys
import time
import subprocess


city_name='北京'
scen_name='颐和园'
# 假设预算和天数
budget = 2000
days = 7

# 获取main.py脚本的目录路径
current_directory = os.path.dirname(os.path.abspath(__file__))
# 构造hotel_note项目的目录路径
hotel_note_directory = os.path.join(current_directory, 'hotel_note')
# 确保hotel_note目录存在
if not os.path.exists(hotel_note_directory):
    print("hotel_note项目目录不存在")
    sys.exit(1)
os.chdir(hotel_note_directory)

commands = [
    'scrapy crawl cityid',
    'scrapy crawl travel_note -a tag={}'.format(city_name)
    ]

for cmd in commands:
    process = subprocess.Popen(cmd.split(), cwd=current_directory)
    process.wait()  # 等待命令执行完成
    time.sleep(1)
current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)  # 改变工作目录到包含 scrapy.cfg 的目录


# 定义过滤和排序函数
def filter_and_sort_travel_logs(travel_logs, budget, days):
    for log in travel_logs:
        # 处理'cost'键
        if 'cost' in log:
            log["cost_int"] = int(log["cost"].replace("人均", "").replace("元", ""))
        else:
            log["cost_int"] = 0  # 默认值
        
        # 处理'days'键
        if 'days' in log:
            log["days_int"] = int(log["days"].replace("共", "").replace("天", ""))
        else:
            log["days_int"] = 0  # 默认值
        
        # 处理'tips'键
        if 'tips' in log:
            log["tips_length"] = len(log["tips"])
        else:
            log["tips_length"] = 0  # 默认值

        # 处理'route'键
        if 'route' in log:
            log["route_length"] = len(log["route"])
        else:
            log["route_length"] = 0  # 默认值
    
    # 根据新增加的长度键进行排序
    filtered_logs = [log for log in travel_logs if log["cost_int"] <= budget and log["days_int"] <= days]
    sorted_logs = sorted(filtered_logs, key=lambda x: (x["route_length"]), reverse=True)
    
    # 清理用于排序的临时键
    for log in sorted_logs:
        del log["cost_int"], log["days_int"], log["tips_length"], log["route_length"]
    best_log = sorted_logs[0] if sorted_logs else None
    return best_log

# 确保使用正确的文件路径和编码打开JSON文件
with open('travel_note.json', 'r', encoding='utf-8') as file:
    travel_logs = json.load(file)

filtered_sorted_logs = filter_and_sort_travel_logs(travel_logs, budget, days)

# 打印结果
if filtered_sorted_logs:
    print(filtered_sorted_logs)

url=filtered_sorted_logs['web']
content=requests.get(url=url)
soup = BeautifulSoup(content.text, 'html.parser')
text_all=soup.find_all('p',class_='first')
for text_ in text_all:
    print(text_.text)