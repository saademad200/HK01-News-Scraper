import scrapy

class Hk01NewsItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    channel = scrapy.Field()
    time = scrapy.Field()
