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
    tag=scrapy.Field()
    pass

class Travel_noteItem(scrapy.Item):
    name = scrapy.Field()
    web = scrapy.Field()
    route = scrapy.Field()
    cost = scrapy.Field()
    days = scrapy.Field()
    tips = scrapy.Field()
    pass