import scrapy

from scrapy.loader import ItemLoader

from ..items import En1754euItem
from itemloaders.processors import TakeFirst


class En1754euSpider(scrapy.Spider):
	name = 'en1754eu'
	start_urls = ['https://en.1754.eu/category/news']

	def parse(self, response):
		post_links = response.xpath('//a[@class="link-block w-inline-block"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="w-pagination-next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//p[@class="paragraph-3"]//text()[normalize-space()] | //div[@class="rich-text-block w-richtext"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//a[@class="mini-title-post-date"]/text()').get()

		item = ItemLoader(item=En1754euItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
