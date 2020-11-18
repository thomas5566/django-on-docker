import sys
import os
import django
sys.path.append("..")
os.environ["DJANGO_SETTINGS_MODULE"] = "best_movies.settings"
django.setup()

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
from crawlmovie.items import PttCloudItem

from datetime import datetime


class PttMoviesSpider(CrawlSpider):
    name = "ptt_movies"
    allowed_domains = ["www.ptt.cc"]
    start_urls = ["https://www.ptt.cc/bbs/movie/index.html"]

    count = 2000

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        # 'CLOSESPIDER_PAGECOUNT': 5,
        "ITEM_PIPELINES": {
            "crawlmovie.pipelines.PttPipeline": 100,
            "crawlmovie.pipelines.DeleteNullTitlePipeline": 200,
            "crawlmovie.pipelines.DuplicatesTitlePipeline": 200,
            "crawlmovie.pipelines.CsvExportPipeline": 300,
        },
        "AUTOTHROTTLE_ENABLED": True,
        # The initial download delay
        "AUTOTHROTTLE_START_DELAY": 5,
        # The maximum download delay to be set in case of high latencies
        "AUTOTHROTTLE_MAX_DELAY": 60,
        # The average number of requests Scrapy should be sending in parallel to
        # each remote server
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 1.0,
        # "CLOSESPIDER_ITEMCOUNT": 150,
    }

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths="//div[@class='title']/a"),
            callback="parse_item",
            follow=True,
        ),
        Rule(
            LinkExtractor(
                restrict_xpaths="//div[@class='btn-group btn-group-paging']/a[2]"
            )
        ),
    )

    def parse_item(self, response):
        item = PttCloudItem()
        # item['title'] = response.xpath(
        #     "normalize-space((//span[@class='article-meta-value'])[3]/text())").extract()
        # i['title'] = ''.join(title)
        for s in response.xpath(
            "normalize-space((//span[@class='article-meta-value'])[3]/text())"
        ).extract():
            if "雷" in s:
                item["title"] = s

                item["author"] = response.xpath(
                    "(//span[@class='article-meta-value'])[1]/text()"
                ).extract()
                # i['author'] = ''.join(author)

                pttdatetime = response.xpath(
                    "(//span[@class='article-meta-value'])[4]/text()"
                ).extract()
                datetime_str = ''.join(str(date) for date in pttdatetime)
                item["date"] = datetime.strptime(datetime_str, "%a %b %d %H:%M:%S %Y").strftime(
                    "%Y-%m-%d %H:%M:%S")

                item["contenttext"] = response.xpath(
                    "//div[@id='main-content']/text()"
                ).extract()

                # 如果滿足指定頁數就停止
                if self.count <= 0:
                    raise CloseSpider('close it')
                self.count -= 1

                yield item

            else:
                yield None
