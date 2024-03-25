from typing import Iterable
import scrapy
from bs4 import BeautifulSoup
from hotel_note.items import HotelNoteItem
import json
from pypinyin import pinyin, Style

class HotelSearchSpider(scrapy.Spider):
    name = "hotel_search"
    allowed_domains = ['hotel.qunar.com','apis.map.qq.com']
    custom_settings = {
        'CONCURRENT_REQUESTS_PER_DOMAIN': 5,  # 每个域名的并发请求限制为5
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 0.2,
        'AUTOTHROTTLE_MAX_DELAY': 5,
    }

    def start_requests(self):
        city_name=self.tag
        flag=False
        with open('city.json', 'r', encoding='utf-8') as file:
            city_json = json.load(file)
        for category in city_json['data']:
            for _, cities in category.items():
                for city in cities:
                    if city['cityName'] == city_name:
                        city_id=city['cityUrl']
                        flag=True
        if flag:
            url="https://hotel.qunar.com/cn/{}".format(city_id)
        else:
            pinyin_text = ''.join([item[0] for item in pinyin(city_name, style=Style.NORMAL)])
            url="https://hotel.qunar.com/cn/{}".format(pinyin_text)
        temp='SECKEY_ABVK=eURMM9L1r0PXQ6Jav4J00KT3LeF3AWDxUqhX8ueP13L8n4lNbMwqDqovxKKzbK4aQ4tN1fQ5Qfjvm9+Nzq7AWg%3D%3D; BMAP_SECKEY=eURMM9L1r0PXQ6Jav4J00KT3LeF3AWDxUqhX8ueP13KjGhAxeL_so-e-ro_8ZC9TgyXNfXNny6T7m6qX-yRXY-wA1DDWhqTq6mwGyP3-MxpCPb5atFffbu-bnGymFFNXwci_jeV5pLjAX2atlLdhrgX-zNgQx6_7H5_XXl6m5bLNvAi73MlHrtXRItgWRUUgNum_WVfBGvyCbbjvxBZhQEpNQVCh4NWG5v3fPg5mMbo; QN1=0000f10031985ca246100efa; HN1=v17f3f582e3eecdf4f7b7685881e257e08; HN2=qullsnrssqcuk; QN300=organic; QN205=organic; QN277=organic; _i=ueHd8LkXXXV7wN7Y-Lqy16k0VB1X; QN269=96612674D56011EEAF17621E859BCEBF; ctt_june=1683616182042##iK3wVRXnVhPwawPwasTIWsETaK28W2DNWDD8WRGGWS2OXKgwVPjsESaNWPXsiK3siK3saKg8VKvsaSDsaK3sVuPwaUvt; fid=cf17a7fd-17fd-404b-b115-7c2667e83266; tabIndex=0; cityUrl=beijing_city; cityName=%25E5%258C%2597%25E4%25BA%25AC; checkInDate=2024-02-29; checkOutDate=2024-03-01; QN267=118798997615a47bff; qunar-assist={%22version%22:%2220211215173359.925%22%2C%22show%22:false%2C%22audio%22:false%2C%22speed%22:%22middle%22%2C%22zomm%22:1%2C%22cursor%22:false%2C%22pointer%22:false%2C%22bigtext%22:false%2C%22overead%22:false%2C%22readscreen%22:false%2C%22theme%22:%22default%22}; csrfToken=Yl2IUKC8ITXZvCWk1GYLFBn5ZfzRiT1y; _vi=Ay4ymHg3BiiCG-ZVOFbvybMwokeoxDUs-Dn_sMZjDyswT0q1FwyD7AD-r0IwyiWVytR6Q5hPpYLc82rgmucPy8MY42t25zA8c-igGZAy8FrfsJJzlEWmUiVPpQAke0R6OgHjWkR_EOQJVoJwhB2EPmI75AsGljJ2CXWybBgM5DnW; QN25=192a9089-0690-47c4-8125-9ef8c3b8ace3-9f992f90; ariaDefaultTheme=undefined; ctf_june=1683616182042##iK3waS2waUPwawPwasXwERkRWDiRVDaOVRTRWDPsaPX%2BaKohEPiDaD3masGTiK3siK3saKg8VKa%3DWSXnVK2%3DVhPwaUvt; __qt=v1%7CVTJGc2RHVmtYMS9BdTNNeFQwdjRHdG5kWDFPYlpNOFh3WDdCZ1psS0VPN1VMMXNHUkZLOW1acTR5M005b1dUOG95b0FuOVNYRGIyVG1WYmhVYzZaQ1lDOXZPUlhLSjZOOVNodXF2SG5BSEpPNVM1STQ1WklrbXZIcDRTTzB3bFB3YXR4OG9xTUx4bk1PTHErazI5WWRnOWdYd2txRXU3THZadXJQZy9KRFgwPQ%3D%3D%7C1709346420114%7CVTJGc2RHVmtYMSsrTlRLaVYwNlAycGdrUG1iZVBEbWRWVCthUFc0eWJVV3dHeUFhaUZhWTA1clFxNzZYaVE0cGFaRkJMOG1abEZsSi9xdzMwTlY4d2c9PQ%3D%3D%7CVTJGc2RHVmtYMS9PTHV4alVDczJ0WlFNMUlBelI5RHJyRXptZHlUV1ZmS2F5L0gzYkVqcG5ZNjFnWGY3R1dGbUxSYVVTczgzM0xBMXozTk9QRHFhSkdsWEFlanBySkQyc2tGTC9CbW04KzlZdVRxTGphKzRCektabzQ3QWZXT2hHdVQxT29pYkNVUEhDZloxZU96L0Q5TExETk5XYzJobnAxaGR0Um9qSWZMVmZWaEhTcTV4eU9BU0J0SlRpN3AyS0NxcisyWCtTRS9YUkdKSVJJUzhpMXp6aGNOOEF4dkFJcnM5NWhDdW9nQjVGelZaNTVadzIzSXlyYVBqWWxPaVVFNFoyNlAyVjM1K2t2Zmd1WWNMWVhiYWdoVGcxTmJ5L0FQUmt3V24vTkJFOStZUVArbFM5a2ZYakVKdEJLNnkwUEEwUFNRcjVsQkFXcnNiR1ZvR1FmVEQwSkQvUjRCNkthZnZ3NHdhdHJFWU9GSlE2eXYvTVNhNW1OT2I3eTlPZENzbkNtNnFzTlE0SGZpb3dpUFd3N29vaVlGdGtKTzhUS1FqNVpWQWRkMlplcDl0ZmZmYXFaTGNXM2RsZ1E1MTF4QTg0bFNBWEdjenh6SWczNFFrN2RhUnBjaTdiUy9lK2dNWFM5aW9RdGw4d0ZxeFdVSTdWRGNUTm5xMGlwNjQzTDVOQ3NmTkpHSGtpejlDNTVVL3VMcU4wM1FSRkNnd0g0NFBia0ZWcklRV3NWZmsrTFdLdEYyZmM1elhzVUZVcS9LZUVKaGUvRG1TaFVaL2FVelpjcHFnaXJWR3l1enphMlpWNmhxN1FsNExtdTFrcDNwMVFrd1pZY3ZicEN6VWFuSFJwTUVZQlg3ZmFuY0tsUWsrU0Vkc0p0dVM3YVpQaFlFOEU4RHFqRW89; QN271=35480231-feab-4e29-a69b-314a0abbf957; cs_june=d7b63ab2f54122efda0ee71183609f1900e591f24eded1b44bbf91ab62283af3325aed99a54a57ec655d63893579ad47ea2dea7a2d149f53d102fa94fdae36efb17c80df7eee7c02a9c1a6a5b97c1179bd2a951c35f042b40bddbdc960b9a6425a737ae180251ef5be23400b098dd8ca'
        cookie={data.split('=')[0]:data.split('=')[-1]for data in temp.split(';')}
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            cookies=cookie
        )
    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        hotels = soup.find('ul', {'id': 'hotel_lst_body'})
        for hotel in hotels:
            item = HotelNoteItem()
            href=hotel.find('a', class_='hotel-name').get('href')
            detail_url='https://hotel.qunar.com'+href
            item['name'] = hotel.find('a', class_='hotel-name').text.strip()
            item['type'] = hotel.find('span', class_='type').text.strip()
            p_tag = soup.find('p', class_='comm')
            item['score'] = p_tag.find('span', class_='num').text.strip()
            item['preview'] = p_tag.find('span', class_='desc').text.strip()
            item['price'] = hotel.find('p', class_='price_new').text.strip().replace('?','0')
            yield scrapy.Request(
                url=detail_url,
                meta={
                    'item':item,
                },
                callback=self.detail_parse
            )
    def detail_parse(self,response):
        item=response.meta['item']
        address=response.xpath('//*[@id="root"]/div/section[2]/section/div[1]/div[1]/div/p[2]/text()').get()
        item['address']=address
        url='https://apis.map.qq.com/ws/geocoder/v1/?address={}&key=PA4BZ-E42L4-7THUO-K65NZ-I5UMH-ERF4A'.format(address)
        yield scrapy.Request(
            url=url,
            meta={
                'item':item,
            },
            callback=self.location_parse
        )
    def location_parse(self,response):
        item=response.meta['item']
        data=json.loads(response.text)
        location = data.get('result', {}).get('location', None)
        if location:
            lng = location.get('lng', None)  # 获取经度
            lat = location.get('lat', None)  # 获取纬度
        # 这里你可以根据需要处理location信息，例如将其添加到item中或打印出来
            item['location']=location
        yield item

        