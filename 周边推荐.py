import requests
import os

# 腾讯地图API密钥
API_KEY = 'AH3BZ-6FX3J-RFVF5-DJOHC-MMRIF-M7BHD'


# 搜索参数
lat = 39.904989  # 纬度
lng = 116.405285  # 经度
radius = 1000  # 搜索半径，单位为米
keyword = '景点'  # 搜索关键词

# 构造请求URL
curl = f"https://apis.map.qq.com/ws/place/v1/explore"
params = {
    'boundary': f"nearby({lat},{lng},{radius})",
    'keyword': keyword,
    'key': API_KEY
}

# 发送GET请求
response = requests.get(curl, params=params, verify=True)
print(response.text)

# 文件保存路径
file_path = r'D:\学习资料\wenxinyiyan\服务外包\address.json'

with open(file_path, 'w', encoding='utf-8') as file:
    file.write(response.text)
print(os.getcwd())

# 检查请求是否成功
if response.status_code == 200:
    # 解析响应数据
    data = response.json()
    if data['status'] == 0:
        # 打印地点信息
        for place in data['data']:
            print(place['title'], place['address'])
    else:
        print("Error:", data['message'])
else:
    print("请求失败HTTP 状态码:", response.status_code)
