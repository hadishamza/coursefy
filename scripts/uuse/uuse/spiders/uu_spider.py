from scrapy.spider import Spider

class UuSpider(Spider):
    name = "uu"
    allowed_domains = ["uu.se"]
    start_urls = [
        "http://bit.ly/1i5frRP"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        open(filename, 'wb').write(response.body)
