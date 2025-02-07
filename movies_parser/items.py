# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MoviesParserItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    genre = scrapy.Field()
    country = scrapy.Field()
    year = scrapy.Field()
    director = scrapy.Field()
