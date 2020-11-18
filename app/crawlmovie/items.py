# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from movie_ranking.models import Movie
from movie_ranking.models import PttMovie


class CrawlmovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PttCloudItem(scrapy.Item):
    django_model = PttMovie
    title = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    contenttext = scrapy.Field()


class YahooCloudItem(scrapy.Item):
    django_model = Movie
    title = scrapy.Field()
    critics_consensus = scrapy.Field()
    release_date = scrapy.Field()
    duration = scrapy.Field()
    genre = scrapy.Field()
    rating = scrapy.Field()
    amount_reviews = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
