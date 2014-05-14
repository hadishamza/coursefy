from scrapy.spider import Spider
from scrapy.selector import Selector
from uuse.items import UuItem

class UuSpider(Spider):
    name = "uu"
    allowed_domains = ["uu.se"]

    def __init__(self, *args, **kwargs):
      super(UuSpider, self).__init__(*args, **kwargs)
      self.start_urls = [kwargs.get('start_url')]

    def parse(self, response):
        sel = Selector(response)
        selrows = sel.xpath('//div[@class="articleText"]//table/tbody//tr')
        data = []
        for selrow in selrows:
            code = selrow.xpath('td[2]//text()').extract()
            is_course = code[0].find('1') == 0 or code[0].find('2') == 0
            if code != [] and code[0] != u'\u00a0' and is_course: # Is it really a course code?
                period_extracted = self.empty_help(selrow.xpath('td[1]/p//text()').extract())
                if period_extracted != '' and period_extracted != None:
                    period = period_extracted

                row = UuItem()
                if period == "Alt.":
                    period = "34"

                row["period"] = period
                row["code"] = self.empty_help(code)
                row["name"] = self.empty_help(selrow.xpath('td[3]/p//text()').extract())
                row["credits"] = self.empty_help(selrow.xpath('td[4]/p//text()').extract())
                row["level"] = self.empty_help(selrow.xpath('td[5]/p//text()').extract())
                data.append(row)
        return data

    def empty_help(self, arr):
        if arr != []:
            return arr[0].replace(u'\u00a0', '')
        else:
            ""
