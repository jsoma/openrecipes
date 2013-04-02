from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem
from spider_egg import SpiderEgg

crawler = SpiderEgg.hatch("101cookbooks", "Crawl Spider")

crawlerClass = type(crawler.__name__, (crawler,CrawlSpider), {
    'rules': (
        Rule(SgmlLinkExtractor(allow=('archives/.+\.html')),
             callback='parse_item'),
    )
})