import scrapy

class FmuCrawlerItem(scrapy.Item):
    url = scrapy.Field()
    type = scrapy.Field()          # 'html', 'pdf', 'image'
    content = scrapy.Field()
    file_path = scrapy.Field()
    file_hash = scrapy.Field()
    file_body = scrapy.Field()
