# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

# import scrapy
from scrapy.item import Item, Field


class MetacriticItem(Item):
	
	movie_title = Field()
	genre = Field()
	release_date = Field()

	metascore = Field()
	meta_positive = Field()
	meta_mixed = Field()
	meta_negative = Field()

	userscore = Field()
	user_positive = Field()
	user_mixed = Field()
	user_negative = Field()
	


