import os
import sys
import time
import subprocess
import json
from math import radians, cos, sin, sqrt, atan2
import requests

city_name='北京'
scen_name='颐和园'
max_price = 300.0 

def get_district(city_name,scen_name):

    url='https://apis.map.qq.com/ws/place/v1/search?boundary=region({})&keyword={}&filter=category=旅游景点&key=PA4BZ-E42L4-7THUO-K65NZ-I5UMH-ERF4A'.format(city_name,scen_name)
    content=requests.get(url=url).json()
    detail=content['data'][0]['ad_info']['district']
    return(detail)

# 获取main.py脚本的目录路径
current_directory = os.path.dirname(os.path.abspath(__file__))
# 构造hotel_note项目的目录路径
hotel_note_directory = os.path.join(current_directory, 'hotel_note')
# 确保hotel_note目录存在
if not os.path.exists(hotel_note_directory):
    print("hotel_note项目目录不存在")
    sys.exit(1)
os.chdir(hotel_note_directory)
district=get_district(city_name,scen_name)
if district:
    commands = [
    'scrapy crawl cityid',
    'scrapy crawl hotel_search -a tag={}'.format(district)
    ]
else:
    commands = [
    'scrapy crawl cityid',
    'scrapy crawl hotel_search -a tag={}'.format(city_name)
    ]
for cmd in commands:
    process = subprocess.Popen(cmd.split(), cwd=current_directory)
    process.wait()  # 等待命令执行完成
    time.sleep(1)
current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)  # 改变工作目录到包含 scrapy.cfg 的目录


def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    R = 6371.0  # 地球平均半径，单位千米
    distance = R * c
    return distance

# 伪造景点位置函数
def postion(city_name,scen_name):

    url='https://apis.map.qq.com/ws/place/v1/search?boundary=region({})&keyword={}&filter=category=旅游景点&key=PA4BZ-E42L4-7THUO-K65NZ-I5UMH-ERF4A'.format(city_name,scen_name)
    content=requests.get(url=url).json()
    first_location = content["data"][0]["location"]
    return(first_location)

# 加权评分算法
def weighted_score(hotels, max_price, pos, initial_weights,alt_weights=(2, 8)):
    # weights: (rating_weight, price_weight, distance_weight)
    scored_hotels = []
    for hotel in hotels:
        price = float(hotel['price'][1:-1])
        dis = haversine(pos['lng'], pos['lat'], hotel['location']['lng'], hotel['location']['lat'])
        rating = float(hotel['score'])
        within_budget = False
        if price <= max_price:
            within_budget = True
            price_score = 10 - (price / max_price) * 10
            distance_score = 10 if dis == 0 else 10 / (dis / 10 + 1)
            weighted_score = (rating * initial_weights[0] + price_score * initial_weights[1] + distance_score * initial_weights[2]) / sum(initial_weights)
        else:
            # 当价格超出预算时，使用备用加权方案
            over_budget_score = 10 - (price / max_price) * 10
            distance_score = 10 if dis == 0 else 10 / (dis / 10 + 1)
            weighted_score = (over_budget_score * alt_weights[0] + distance_score * alt_weights[1]) / sum(alt_weights)

        scored_hotels.append((hotel, weighted_score, dis))

    if within_budget:
        # 如果有符合预算的酒店，按加权得分排序
        scored_hotels.sort(key=lambda x: -x[1])
    else:
        # 如果所有酒店都超出预算，可能需要根据备用方案调整排序依据
        print("所有酒店都超出预算，采用备用评分策略。")
        scored_hotels.sort(key=lambda x: -x[1])
    return scored_hotels[:3]

def main(max_price):
    with open('hotel.json', 'r', encoding='utf-8') as f:
        hotels = json.load(f)

     # 用户预算
    pos = postion(city_name, scen_name)  # 获取景点位置
    weights = (1, 3, 6)  # 定义权重：评分权重为5，价格权重为3，距离权重为2

    top_hotels = weighted_score(hotels, max_price, pos, weights)
    
    formatted_hotels = []  # 用于保存格式化后的酒店数据
    for hotel, score, dis in top_hotels:
        formatted_hotel = hotel  # 假设hotel已是一个包含所有酒店信息的字典
        formatted_hotel['weighted_score'] = score
        formatted_hotel['distance'] = f"{dis:.2f} km"
        
        formatted_hotels.append(formatted_hotel)
    
    # 将格式化后的酒店数据转换为JSON字符串
    formatted_json = json.dumps(formatted_hotels, indent=4, ensure_ascii=False)
    print(formatted_json)

main(max_price)


