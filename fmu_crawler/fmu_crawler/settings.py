# Scrapy settings for fmu_crawler project
BOT_NAME = 'fmu_crawler'

SPIDER_MODULES = ['fmu_crawler.spiders']
NEWSPIDER_MODULE = 'fmu_crawler.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS_PER_DOMAIN = 4
DOWNLOAD_DELAY = 1.0
COOKIES_ENABLED = False
DEPTH_LIMIT = 10

ITEM_PIPELINES = {
    'fmu_crawler.pipelines.FmuPipeline': 300,
}

FEEDS = {
    'results.jsonl': {
        'format': 'jsonlines',
        'encoding': 'utf8',
        'store_empty': False,
        'fields': ['url', 'type', 'file_path', 'file_hash', 'content'],
    }
}
