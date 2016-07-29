import scrapy
from unclaimed.items import UnclaimedItem

class CasearchSpider(scrapy.Spider):
    name = "casearch"
    allowed_domains = ["ucpi.sco.ca.gov"]

    def build_urls(self):
        urls = []
        for x in range(29200000, 29300000):
            urls.append("https://ucpi.sco.ca.gov/ucp/PropertyDetails.aspx?propertyRecID=" + str(x))
        return urls

    start_urls = build_urls()

    def parse(self, response):
        item = UnclaimedItem()
        header_data = response.xpath("//table[@id='tbl_HeaderInformation']/tr/td/span/text()").extract()
        item['date'] = header_data[0].strip()
        item['source'] = header_data[1].strip()
        item['id'] = header_data[2].strip()
        item['recid'] = response.xpath("//form[@id='aspnetForm']/@action").extract()[0].strip('./PropertyDetails.aspx?propertyRecID=')
        item['name'] = response.xpath("//td[@id='OwnersNameData']/span/span/text()").extract()[0].strip()

        address = "".join(x.strip().replace('<br>', '\r\n') for x in response.xpath("//td[@id='ReportedAddressData']/node()").extract())
        item['address'] = address

        item['type'] = response.xpath("//td[@id='PropertyTypeData']/text()").extract()[0].strip()
        item['cash'] = float(response.xpath("//td[@id='ctl00_ContentPlaceHolder1_CashReportData']/text()").extract()[0].strip() \
            .split()[0].replace("$", "").replace(",", ""))
        item['reportedby'] = response.xpath("//td[@id='ReportedByData']/text()").extract()[0].strip()

        yield item
