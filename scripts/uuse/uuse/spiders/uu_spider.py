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
        period = "11"
        for selrow in selrows:
            code = selrow.xpath('td[2]//text()').extract()
            period_extracted = self.empty_help(selrow.xpath('td[1]/p//text()').extract())
            period_not_empty = (period_extracted != None and period_extracted != '' and period_extracted != '.')
            if period_not_empty and period_extracted.lower() != "alt.":
                period = period_extracted.replace(" ", "") #Get rid of whitespace

            if code != [] and code[0] != u'\u00a0' and len(code[0]) == 6: # Is it really a course code?
                periods = period.split("-")
                row = UuItem()
                row["period"] = period
                row["code"] = self.empty_help(code)
                row["name"] = self.empty_help(selrow.xpath('td[3]/p//text()').extract())
                row["credits"] = self.empty_help(selrow.xpath('td[4]/p//text()').extract())
                row["level"] = self.empty_help(selrow.xpath('td[5]/p//text()').extract())

                if len(periods) > 1:
                    row["period"] = periods[0]
                    row2 = row.copy()
                    row2["period"] = periods[1]
                    data.append(row2)

                data.append(row)

        return data

    def empty_help(self, arr):
        if arr != []:
            return arr[0].replace(u'\u00a0', '')
        else:
            ""

