from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector, XmlXPathSelector
from openrecipes.items import RecipeItem
import ConfigParser
from common_spider import CommonSpider

class SpiderEgg:
  
    @classmethod
    def hatch(self, config, config_section_name):
        config_parser = ConfigParser.ConfigParser()
        config_parser.read("openrecipes/spiders/" + config + ".cfg")
        
        class cls(CommonSpider):
            section = config_section_name
            name = config_parser.get(config_section_name, "name")
            allowed_domains = config_parser.get(config_section_name, "allowed_domains").split(",")
            start_urls = config_parser.get(config_section_name, "start_urls").split(",")
            cp = config_parser
            pass

        cls.__name__ = config_parser.get("Default", "classbasename") + config_section_name.replace(' ','')
        return cls
