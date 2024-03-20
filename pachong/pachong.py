import requests
import json
import codecs
import time
from bs4 import BeautifulSoup
# 去哪儿城市列表
def get_citys():
    url_city = "https://touch.qunar.com/h-api/hotel/hotelcity/en"
    s = requests.get(url_city)
    file = codecs.open('./city.json','w','utf-8')
    file.write(s.text)
    file.close()    
    
# 定义根据城市名获取city_id的函数
def get_city_id(city_name, city_json):
    for category in city_json['data']:
        for _, cities in category.items():
            for city in cities:
                if city['cityName'] == city_name:
                    return city['cityUrl']
    return None
def hotel_search(city_name):
    get_citys()
    with open('city.json', 'r', encoding='utf-8') as file:
        city_json = json.load(file)
    city_id = get_city_id(city_name, city_json)
    if city_id=='':
        print("找不到指定的城市。")
    if 1==1:
        url="https://hotel.qunar.com/cn/{}".format(city_id)
    else:
        url = "https://hotel.qunar.com/cn/{}/?fromDate={}&toDate={}".format(city_id,intime,outime)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Cookie':'SECKEY_ABVK=eURMM9L1r0PXQ6Jav4J00KT3LeF3AWDxUqhX8ueP13L8n4lNbMwqDqovxKKzbK4aQ4tN1fQ5Qfjvm9+Nzq7AWg%3D%3D; BMAP_SECKEY=eURMM9L1r0PXQ6Jav4J00KT3LeF3AWDxUqhX8ueP13KjGhAxeL_so-e-ro_8ZC9TgyXNfXNny6T7m6qX-yRXY-wA1DDWhqTq6mwGyP3-MxpCPb5atFffbu-bnGymFFNXwci_jeV5pLjAX2atlLdhrgX-zNgQx6_7H5_XXl6m5bLNvAi73MlHrtXRItgWRUUgNum_WVfBGvyCbbjvxBZhQEpNQVCh4NWG5v3fPg5mMbo; QN1=0000f10031985ca246100efa; HN1=v17f3f582e3eecdf4f7b7685881e257e08; HN2=qullsnrssqcuk; QN300=organic; QN205=organic; QN277=organic; _i=ueHd8LkXXXV7wN7Y-Lqy16k0VB1X; QN269=96612674D56011EEAF17621E859BCEBF; ctt_june=1683616182042##iK3wVRXnVhPwawPwasTIWsETaK28W2DNWDD8WRGGWS2OXKgwVPjsESaNWPXsiK3siK3saKg8VKvsaSDsaK3sVuPwaUvt; fid=cf17a7fd-17fd-404b-b115-7c2667e83266; tabIndex=0; cityUrl=beijing_city; cityName=%25E5%258C%2597%25E4%25BA%25AC; checkInDate=2024-02-29; checkOutDate=2024-03-01; QN267=118798997615a47bff; qunar-assist={%22version%22:%2220211215173359.925%22%2C%22show%22:false%2C%22audio%22:false%2C%22speed%22:%22middle%22%2C%22zomm%22:1%2C%22cursor%22:false%2C%22pointer%22:false%2C%22bigtext%22:false%2C%22overead%22:false%2C%22readscreen%22:false%2C%22theme%22:%22default%22}; csrfToken=Yl2IUKC8ITXZvCWk1GYLFBn5ZfzRiT1y; _vi=Ay4ymHg3BiiCG-ZVOFbvybMwokeoxDUs-Dn_sMZjDyswT0q1FwyD7AD-r0IwyiWVytR6Q5hPpYLc82rgmucPy8MY42t25zA8c-igGZAy8FrfsJJzlEWmUiVPpQAke0R6OgHjWkR_EOQJVoJwhB2EPmI75AsGljJ2CXWybBgM5DnW; QN25=192a9089-0690-47c4-8125-9ef8c3b8ace3-9f992f90; ariaDefaultTheme=undefined; ctf_june=1683616182042##iK3waS2waUPwawPwasXwERkRWDiRVDaOVRTRWDPsaPX%2BaKohEPiDaD3masGTiK3siK3saKg8VKa%3DWSXnVK2%3DVhPwaUvt; __qt=v1%7CVTJGc2RHVmtYMS9BdTNNeFQwdjRHdG5kWDFPYlpNOFh3WDdCZ1psS0VPN1VMMXNHUkZLOW1acTR5M005b1dUOG95b0FuOVNYRGIyVG1WYmhVYzZaQ1lDOXZPUlhLSjZOOVNodXF2SG5BSEpPNVM1STQ1WklrbXZIcDRTTzB3bFB3YXR4OG9xTUx4bk1PTHErazI5WWRnOWdYd2txRXU3THZadXJQZy9KRFgwPQ%3D%3D%7C1709346420114%7CVTJGc2RHVmtYMSsrTlRLaVYwNlAycGdrUG1iZVBEbWRWVCthUFc0eWJVV3dHeUFhaUZhWTA1clFxNzZYaVE0cGFaRkJMOG1abEZsSi9xdzMwTlY4d2c9PQ%3D%3D%7CVTJGc2RHVmtYMS9PTHV4alVDczJ0WlFNMUlBelI5RHJyRXptZHlUV1ZmS2F5L0gzYkVqcG5ZNjFnWGY3R1dGbUxSYVVTczgzM0xBMXozTk9QRHFhSkdsWEFlanBySkQyc2tGTC9CbW04KzlZdVRxTGphKzRCektabzQ3QWZXT2hHdVQxT29pYkNVUEhDZloxZU96L0Q5TExETk5XYzJobnAxaGR0Um9qSWZMVmZWaEhTcTV4eU9BU0J0SlRpN3AyS0NxcisyWCtTRS9YUkdKSVJJUzhpMXp6aGNOOEF4dkFJcnM5NWhDdW9nQjVGelZaNTVadzIzSXlyYVBqWWxPaVVFNFoyNlAyVjM1K2t2Zmd1WWNMWVhiYWdoVGcxTmJ5L0FQUmt3V24vTkJFOStZUVArbFM5a2ZYakVKdEJLNnkwUEEwUFNRcjVsQkFXcnNiR1ZvR1FmVEQwSkQvUjRCNkthZnZ3NHdhdHJFWU9GSlE2eXYvTVNhNW1OT2I3eTlPZENzbkNtNnFzTlE0SGZpb3dpUFd3N29vaVlGdGtKTzhUS1FqNVpWQWRkMlplcDl0ZmZmYXFaTGNXM2RsZ1E1MTF4QTg0bFNBWEdjenh6SWczNFFrN2RhUnBjaTdiUy9lK2dNWFM5aW9RdGw4d0ZxeFdVSTdWRGNUTm5xMGlwNjQzTDVOQ3NmTkpHSGtpejlDNTVVL3VMcU4wM1FSRkNnd0g0NFBia0ZWcklRV3NWZmsrTFdLdEYyZmM1elhzVUZVcS9LZUVKaGUvRG1TaFVaL2FVelpjcHFnaXJWR3l1enphMlpWNmhxN1FsNExtdTFrcDNwMVFrd1pZY3ZicEN6VWFuSFJwTUVZQlg3ZmFuY0tsUWsrU0Vkc0p0dVM3YVpQaFlFOEU4RHFqRW89; QN271=35480231-feab-4e29-a69b-314a0abbf957; cs_june=d7b63ab2f54122efda0ee71183609f1900e591f24eded1b44bbf91ab62283af3325aed99a54a57ec655d63893579ad47ea2dea7a2d149f53d102fa94fdae36efb17c80df7eee7c02a9c1a6a5b97c1179bd2a951c35f042b40bddbdc960b9a6425a737ae180251ef5be23400b098dd8ca'
    }
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        content = response.text

# 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(content, 'html.parser')
# 从HTML中提取所需信息
        
        hotels = soup.find('ul', {'id': 'hotel_lst_body'})
        with open('hotels_info.txt', 'w', encoding='utf-8') as file:
            for hotel in hotels:
                name = hotel.find('a', class_='hotel-name').text.strip()
                type_ = hotel.find('span', class_='type').text.strip()
                p_tag = soup.find('p', class_='comm')
                score = p_tag.find('span', class_='num').text.strip()
                review = p_tag.find('span', class_='desc').text.strip()
                price = hotel.find('p', class_='price_new').text.strip().replace('?','0')
                hotel_info = f"酒店名称: {name}, 类型: {type_}, 评分: {score}, 评价: {review}, 价格: {price}\n"
                file.write(hotel_info)
        print('酒店信息请求成功')
    else:
        print("请求失败，状态码：", response.status_code)


def travelnotes_search(cityname):
    with open('travel_note.txt','w',encoding='utf-8') as file:
        for page_num in range(1,6):
            url='https://travel.qunar.com/travelbook/list/{}/hot_heat/{}.htm'.format(city_name,page_num)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Cookie':'SECKEY_ABVK=eURMM9L1r0PXQ6Jav4J00KT3LeF3AWDxUqhX8ueP13L8n4lNbMwqDqovxKKzbK4aQ4tN1fQ5Qfjvm9+Nzq7AWg%3D%3D; BMAP_SECKEY=eURMM9L1r0PXQ6Jav4J00KT3LeF3AWDxUqhX8ueP13KjGhAxeL_so-e-ro_8ZC9TgyXNfXNny6T7m6qX-yRXY-wA1DDWhqTq6mwGyP3-MxpCPb5atFffbu-bnGymFFNXwci_jeV5pLjAX2atlLdhrgX-zNgQx6_7H5_XXl6m5bLNvAi73MlHrtXRItgWRUUgNum_WVfBGvyCbbjvxBZhQEpNQVCh4NWG5v3fPg5mMbo; QN1=0000f10031985ca246100efa; HN1=v17f3f582e3eecdf4f7b7685881e257e08; HN2=qullsnrssqcuk; QN300=organic; QN205=organic; QN277=organic; _i=ueHd8LkXXXV7wN7Y-Lqy16k0VB1X; QN269=96612674D56011EEAF17621E859BCEBF; ctt_june=1683616182042##iK3wVRXnVhPwawPwasTIWsETaK28W2DNWDD8WRGGWS2OXKgwVPjsESaNWPXsiK3siK3saKg8VKvsaSDsaK3sVuPwaUvt; fid=cf17a7fd-17fd-404b-b115-7c2667e83266; tabIndex=0; cityUrl=beijing_city; cityName=%25E5%258C%2597%25E4%25BA%25AC; checkInDate=2024-02-29; checkOutDate=2024-03-01; QN267=118798997615a47bff; qunar-assist={%22version%22:%2220211215173359.925%22%2C%22show%22:false%2C%22audio%22:false%2C%22speed%22:%22middle%22%2C%22zomm%22:1%2C%22cursor%22:false%2C%22pointer%22:false%2C%22bigtext%22:false%2C%22overead%22:false%2C%22readscreen%22:false%2C%22theme%22:%22default%22}; csrfToken=Yl2IUKC8ITXZvCWk1GYLFBn5ZfzRiT1y; _vi=Ay4ymHg3BiiCG-ZVOFbvybMwokeoxDUs-Dn_sMZjDyswT0q1FwyD7AD-r0IwyiWVytR6Q5hPpYLc82rgmucPy8MY42t25zA8c-igGZAy8FrfsJJzlEWmUiVPpQAke0R6OgHjWkR_EOQJVoJwhB2EPmI75AsGljJ2CXWybBgM5DnW; QN25=192a9089-0690-47c4-8125-9ef8c3b8ace3-9f992f90; ariaDefaultTheme=undefined; ctf_june=1683616182042##iK3waS2waUPwawPwasXwERkRWDiRVDaOVRTRWDPsaPX%2BaKohEPiDaD3masGTiK3siK3saKg8VKa%3DWSXnVK2%3DVhPwaUvt; __qt=v1%7CVTJGc2RHVmtYMS9BdTNNeFQwdjRHdG5kWDFPYlpNOFh3WDdCZ1psS0VPN1VMMXNHUkZLOW1acTR5M005b1dUOG95b0FuOVNYRGIyVG1WYmhVYzZaQ1lDOXZPUlhLSjZOOVNodXF2SG5BSEpPNVM1STQ1WklrbXZIcDRTTzB3bFB3YXR4OG9xTUx4bk1PTHErazI5WWRnOWdYd2txRXU3THZadXJQZy9KRFgwPQ%3D%3D%7C1709346420114%7CVTJGc2RHVmtYMSsrTlRLaVYwNlAycGdrUG1iZVBEbWRWVCthUFc0eWJVV3dHeUFhaUZhWTA1clFxNzZYaVE0cGFaRkJMOG1abEZsSi9xdzMwTlY4d2c9PQ%3D%3D%7CVTJGc2RHVmtYMS9PTHV4alVDczJ0WlFNMUlBelI5RHJyRXptZHlUV1ZmS2F5L0gzYkVqcG5ZNjFnWGY3R1dGbUxSYVVTczgzM0xBMXozTk9QRHFhSkdsWEFlanBySkQyc2tGTC9CbW04KzlZdVRxTGphKzRCektabzQ3QWZXT2hHdVQxT29pYkNVUEhDZloxZU96L0Q5TExETk5XYzJobnAxaGR0Um9qSWZMVmZWaEhTcTV4eU9BU0J0SlRpN3AyS0NxcisyWCtTRS9YUkdKSVJJUzhpMXp6aGNOOEF4dkFJcnM5NWhDdW9nQjVGelZaNTVadzIzSXlyYVBqWWxPaVVFNFoyNlAyVjM1K2t2Zmd1WWNMWVhiYWdoVGcxTmJ5L0FQUmt3V24vTkJFOStZUVArbFM5a2ZYakVKdEJLNnkwUEEwUFNRcjVsQkFXcnNiR1ZvR1FmVEQwSkQvUjRCNkthZnZ3NHdhdHJFWU9GSlE2eXYvTVNhNW1OT2I3eTlPZENzbkNtNnFzTlE0SGZpb3dpUFd3N29vaVlGdGtKTzhUS1FqNVpWQWRkMlplcDl0ZmZmYXFaTGNXM2RsZ1E1MTF4QTg0bFNBWEdjenh6SWczNFFrN2RhUnBjaTdiUy9lK2dNWFM5aW9RdGw4d0ZxeFdVSTdWRGNUTm5xMGlwNjQzTDVOQ3NmTkpHSGtpejlDNTVVL3VMcU4wM1FSRkNnd0g0NFBia0ZWcklRV3NWZmsrTFdLdEYyZmM1elhzVUZVcS9LZUVKaGUvRG1TaFVaL2FVelpjcHFnaXJWR3l1enphMlpWNmhxN1FsNExtdTFrcDNwMVFrd1pZY3ZicEN6VWFuSFJwTUVZQlg3ZmFuY0tsUWsrU0Vkc0p0dVM3YVpQaFlFOEU4RHFqRW89; QN271=35480231-feab-4e29-a69b-314a0abbf957; cs_june=d7b63ab2f54122efda0ee71183609f1900e591f24eded1b44bbf91ab62283af3325aed99a54a57ec655d63893579ad47ea2dea7a2d149f53d102fa94fdae36efb17c80df7eee7c02a9c1a6a5b97c1179bd2a951c35f042b40bddbdc960b9a6425a737ae180251ef5be23400b098dd8ca'
            }
            response = requests.get(url,headers=headers)
            if response.status_code == 200:
                content = response.text
                original_web='https://travel.qunar.com'
                soup = BeautifulSoup(content, 'html.parser')
                travel_list=soup.find('ul',class_='b_strategy_list')
                if travel_list:
                    for tri in travel_list:
                        hrefs=tri.find('h2',class_='tit')
                        file.write(hrefs.text+'\n')
                        href_=hrefs.find('a')['href']
                        note_web=original_web+href_
                        file.write(note_web+'\n')
                        places=tri.find_all('p',class_='places')
                        for place in places:
                            if '行程：' in place.text:
                                file.write(place.text+'\n')
                        cost=tri.find('span',class_='fee')
                        if cost:
                            file.write(cost.text)
                        days=tri.find('span',class_='days')
                        if days:
                            file.write(days.text+'\n')
                        tips=tri.find('span',class_='trip')
                        if tips:
                            file.write('tips:'+tips.text+'\n')
                        file.write('\n')
                print('第{}页游记信息请求成功'.format(page_num))
            else:
                print('oops!Please try again')
            time.sleep(0.5)

city_name='宁波'
hotel_search(city_name)
travelnotes_search(city_name)