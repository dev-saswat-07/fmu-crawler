import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from fmu_crawler.items import FmuCrawlerItem

class FmuSpider(CrawlSpider):
    name = 'fmu'
    allowed_domains = ['fmuniversity.nic.in']
    start_urls = ['https://fmuniversity.nic.in/index']

    rules = (
        Rule(LinkExtractor(allow_domains=allowed_domains,
                           deny=(r'\.(pdf|jpg|jpeg|png|gif)$',)),
             callback='parse_page',
             follow=True),
        Rule(LinkExtractor(allow_domains=allowed_domains,
                           allow=(r'\.pdf$',)),
             callback='download_pdf'),
        Rule(LinkExtractor(allow_domains=allowed_domains,
                           allow=(r'\.(jpg|jpeg|png|gif)$',)),
             callback='download_image'),
    )

    def parse_page(self, response):
        text = ' '.join(response.css('body ::text').getall()).strip()
        if text:
            item = FmuCrawlerItem()
            item['url'] = response.url
            item['type'] = 'html'
            item['content'] = text
            yield item

    def download_pdf(self, response):
        item = FmuCrawlerItem()
        item['url'] = response.url
        item['type'] = 'pdf'
        item['file_body'] = response.body
        yield item

    def download_image(self, response):
        item = FmuCrawlerItem()
        item['url'] = response.url
        item['type'] = 'image'
        item['file_body'] = response.body
        yield item
