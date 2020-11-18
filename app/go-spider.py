from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from crawlmovie.spiders.ptt import PttMoviesSpider
from crawlmovie.spiders.yahoo import YahooSpider


process = CrawlerProcess(get_project_settings())
process.crawl(YahooSpider)
process.crawl(PttMoviesSpider)
process.start()