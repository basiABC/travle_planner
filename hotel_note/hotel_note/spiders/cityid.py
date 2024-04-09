import scrapy
import json
import codecs
class CityidSpider(scrapy.Spider):
    name = "cityid"
    allowed_domains = ["touch.qunar.com"]
    start_urls = ["https://touch.qunar.com/h-api/hotel/hotelcity/en"]

    def parse(self, response):
        if response.text:
            file = codecs.open('./city.json','w','utf-8')
            file.write(response.text)
            file.close()   
        
