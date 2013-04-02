from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector, XmlXPathSelector
from openrecipes.items import RecipeItem
import ConfigParser

class CommonSpider(BaseSpider):    
      
  def value(self, key):
    if self.cp.has_option(self.section, key):
      return self.cp.get(self.section, key) 
    elif self.cp.has_option("Default", key):
      return self.cp.get("Default", key)

  def parse(self, response):
      if(self.value('link_extractor') != None):
          xxs = XmlXPathSelector(response)
          links = xxs.select(self.value("link_extractor")).extract()
          return [Request(x, callback=self.parse_item) for x in links]
      else:
          return super(CommonSpider, self).parse(response)

  def parse_item(self, response):
      """
      this is identical to
      spiders.OnehundredonecookbookscrawlSpider.parse_item(), which is
      probably not good. we should sort out a way to not repeat ourselves
      """
      hxs = HtmlXPathSelector(response)

      base_path = self.value("base_path")

      recipes_scopes = hxs.select(base_path)

      name_path = self.value("name_path")
      description_path = self.value("description_path")
      url_path = self.value("url_path")
      image_path = self.value("image_path")
      prepTime_path = self.value("prepTime_path")
      cookTime_path = self.value("cookTime_path")

      recipeYield_path = "|".join(self.value("recipeYield_path").split("\n"))
      ingredients_path = self.value("ingredients_path")
      datePublished = self.value("datePublished")

      recipes = []
      for r_scope in recipes_scopes:
          item = RecipeItem()
          item['name'] = r_scope.select(name_path).extract()
          item['image'] = r_scope.select(image_path).extract()
          item['url'] = r_scope.select(url_path).extract()
          item['description'] = r_scope.select(description_path).extract()

          item['prepTime'] = r_scope.select(prepTime_path).extract()
          item['cookTime'] = r_scope.select(cookTime_path).extract()
          item['recipeYield'] = r_scope.select(recipeYield_path).extract()

          item['ingredients'] = r_scope.select(ingredients_path).extract()

          item['datePublished'] = r_scope.select(datePublished).extract()

          recipes.append(item)

      return recipes