import scrapy
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from items import ArcadyItem


class ArcadySpider(CrawlSpider):
    name = "arcady"

    def start_requests(self):
        start_urls = ["https://en.wikipedia.org/wiki/Python_(programming_language)",
                      "https://en.wikipedia.org/wiki/Renaissance_Cleveland_Hotel",
                      "https://en.wikipedia.org/wiki/2018_NCAA_Division_I_Men%27s_Basketball_Tournament"]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        item = ArcadyItem()
        title = response.xpath('//h1/text()')[0].extract()
        print("Title is: " + title)
        item['title'] = title
        return item
