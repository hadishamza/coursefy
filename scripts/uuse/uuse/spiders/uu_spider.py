from scrapy.spider import Spider
from scrapy.selector import Selector
from uuse.items import UuItem

class UuSpider(Spider):
    name = "uu"
    allowed_domains = ["uu.se"]
    start_urls = [
        "http://bit.ly/1i5frRP"
    ]

    def parse(self, response):
        sel = Selector(response)
        selrows = sel.xpath('//div[@class="articleText"]//table/tbody//tr')
        data = []
        for selrow in selrows:
            code = selrow.xpath('td[2]/p//text()').extract()
            if code != [] and code[0] != u'\u00a0' and code[0].find('1') == 0: # Is it really a course code?
                row = UuItem()
                row["period"] = self.empty_help(selrow.xpath('td[1]/p//text()').extract())
                row["code"] = self.empty_help(code)
                row["name"] = self.empty_help(selrow.xpath('td[3]/p//text()').extract())
                row["credits"] = self.empty_help(selrow.xpath('td[4]/p//text()').extract())
                row["level"] = self.empty_help(selrow.xpath('td[5]/p//text()').extract())
                data.append(row)
        print data
        return data
                
        #filename = response.url.split("/")[-2]
        #open(filename, 'wb').write(response.body)
    
    def empty_help(self, arr):
        if arr != []:
            return arr[0].replace(u'\u00a0', '')
        else:
            ""
