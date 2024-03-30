# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HotelNoteItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field() 
    type = scrapy.Field() 
    score = scrapy.Field() 
    preview = scrapy.Field() 
    price = scrapy.Field() 
    address = scrapy.Field() 
    location=scrapy.Field()
    pass

class CityIdItem(scrapy.Item):
    response = scrapy.Field()
    pass