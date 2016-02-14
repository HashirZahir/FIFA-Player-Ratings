# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class PlayerItem(Item):
    # define the fields for your item here like:
	def __setitem__(self, key, value):
		if key not in self.fields:
			self.fields[key] = Field()  #if key does not exist, then create a new one in self.fields (ie dynamic list)
		self._values[key] = value


