import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from rlbooe.items import Article


class RlbooeSpider(scrapy.Spider):
    name = 'rlbooe'
    start_urls = ['https://www.rlbooe.de/de/ueber-uns/presse.html']

    def parse(self, response):
        links = response.xpath('//a[@class="btn btn-primary"][span[text()="zum Pressebericht"]]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        content = response.xpath('//div[@class="component-text rte "]//text()').getall()
        content = [text for text in content if text.strip()]
        date = content[0].split()[0]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
