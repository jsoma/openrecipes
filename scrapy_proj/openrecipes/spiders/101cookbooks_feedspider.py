from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector, XmlXPathSelector
from openrecipes.items import RecipeItem
from spider_egg import SpiderEgg

crawler = SpiderEgg.hatch("101cookbooks", "Feed Spider")

crawlerClass = type(crawler.__name__, (crawler,), {})

print crawlerClass.section