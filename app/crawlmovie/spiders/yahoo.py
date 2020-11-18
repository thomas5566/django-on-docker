import scrapy
import sys
import os
import django
sys.path.append("..")
os.environ["DJANGO_SETTINGS_MODULE"] = "best_movies.settings"
django.setup()

from crawlmovie.items import YahooCloudItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from best_movies.settings import MEDIA_ROOT


class YahooSpider(CrawlSpider):
    name = 'yahoo'
    allowed_domains = ['yahoo.com.tw']
    start_urls = ['https://movies.yahoo.com.tw/movie_intheaters.html?page=1']

    IMAGE_DIR = MEDIA_ROOT

    custom_settings = {
        "IMAGES_STORE": IMAGE_DIR,
        "DOWNLOAD_DELAY": 3,
        "ITEM_PIPELINES": {
            "crawlmovie.pipelines.CustomImagePipeline": 1,
            "crawlmovie.pipelines.YahooPipeline": 100,
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
            LinkExtractor(
                restrict_xpaths="//div[@class='release_movie_name']/a"),
            callback="parse_item",
            follow=True,
        ),
        Rule(LinkExtractor(restrict_xpaths="//li[@class='nexttxt']/a")),
    )

    def parse_item(self, response):
        item = YahooCloudItem()
        title = response.xpath(
            "normalize-space(//div[@class='movie_intro_info_r']/h1/text())"
        ).extract()
        item["title"] = "".join(title)

        critics_consensus = response.xpath(
            "normalize-space(//span[@id='story']/text())"
        ).extract()
        item["critics_consensus"] = "".join(
            [i.replace(u"\xa0", u"") for i in critics_consensus]
        )
        item["release_date"] = response.xpath(
            "(//div[@class='movie_intro_info_r']/span[1]/text())"
        ).extract()[0]

        duration = response.xpath(
            "//div[@class='movie_intro_info_r']/span[2]/text()"
        ).extract()
        item["duration"] = "".join(
            [i.replace(u"\\u3000\\", u"") for i in duration])

        item["genre"] = response.xpath(
            "normalize-space((//div[@class='level_name'])[2]/a/text())"
        ).extract()
        # i['rating'] = response.css(
        #     '.ratingValue ::text').extract()[1]
        item["rating"] = response.xpath(
            "//div[@class='score_num count']/text()"
        ).extract()
        item["amount_reviews"] = response.xpath(
            "//div[@class='circlenum']/div[@class='num']/span/text()"
        ).extract()
        url = response.xpath(
            "//div[@class='movie_intro_foto']/img/@src").extract()
        link = "".join(url)
        item["images"] = {item["title"]: link}

        yield item
