import scrapy
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from items import ArcadyItem


class ArcadySpider(CrawlSpider):
    name = "arcady"

    def start_requests(self):
        start_urls = ["https://en.wikipedia.org/wiki/Python_(programming_language)"]
        for url in start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        item = ArcadyItem()
        for h2 in response.xpath('//body//span[@class="mw-headline"]//text()').extract():
            yield {"h2": h2}
