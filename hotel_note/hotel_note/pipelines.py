# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class HotelNotePipeline:
    def open_spider(self, spider):
        self.items = []  # 初始化列表以收集项目

    def process_item(self, item, spider):
        item_dict = dict(item)
        item_dict['rank'] = len(self.items) + 1  # 添加名次信息
        self.items.append(item_dict)  # 将带有名次信息的项目添加到列表中
        return item

    def close_spider(self, spider):
        if self.items!=[]:
            with open('hotel.json', 'w', encoding='utf-8') as file:
                # 使用json.dumps一次性将列表转换为JSON字符串并写入文件
                json_data = json.dumps(self.items, ensure_ascii=False, indent=4)
                file.write(json_data)

