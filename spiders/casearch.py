import scrapy
import pymongo
from unclaimed.items import UnclaimedItem

class CasearchSpider(scrapy.Spider):
    name = "casearch"
    allowed_domains = ["ucpi.sco.ca.gov"]
    start_urls = []

    def __init__(self, start=None, end=None, *args, **kwargs):
        start = int(start)
        end = int(end)

        out_of_range = False

        if (start < 3427562):
            print('\nERROR: start RecID ' + str(start) + ' below allowed range: < 3427562 - 36500536')
            out_of_range = True

        if (end > 36500536):
            print('\nERROR: end RecID ' + str(end) + ' above allowed range: 3427562 - 36500536')
            out_of_range = True

        if out_of_range:
            print('\nEXITING... NOTHING WILL BE SCRAPED\n')
        else:
            super(CasearchSpider, self).__init__(*args, **kwargs)

            for x in range(start, end):
                # exists = self.db[self.collection_name].find({ "recid": str(x) }, { "recid": 1 }).count()
                # if (exists > 0):
                #     continue

                self.start_urls.append("https://ucpi.sco.ca.gov/ucp/PropertyDetails.aspx?propertyRecID=" + str(x))

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
