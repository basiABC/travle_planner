import requests
from bs4 import BeautifulSoup

def get_district(city_name,scen_name):

    url='https://apis.map.qq.com/ws/place/v1/search?boundary=region({})&keyword={}&filter=category=旅游景点&key=PA4BZ-E42L4-7THUO-K65NZ-I5UMH-ERF4A'.format(city_name,scen_name)
    content=requests.get(url=url).json()
    first_location = content["data"][0]["location"]
    return(first_location)

city_name='宁波'
scen_name='四明湖'
dis=get_district(city_name,scen_name)
travel_list=[]
for index in (1,20):
    url='https://apis.map.qq.com/ws/place/v1/explore?key=PA4BZ-E42L4-7THUO-K65NZ-I5UMH-ERF4A&boundary=nearby({},{},10000,1)&filter=category=旅游景点&page_size=20&page_index={}'.format(dis['lat'],dis['lng'],index)
    content=requests.get(url=url).json()
    place_list=content['data']
    for place in place_list:
        travel_list.append(place)
print(travel_list)
