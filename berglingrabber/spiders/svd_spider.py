from scrapy.selector import Selector
from scrapy.spider import Spider
from berglingrabber.items import BerglingrabberItem

from subprocess import check_output

class SvdSpiderSpider(Spider):
    name = 'svd_spider'
    allowed_domains = ['svd.se']
    start_urls = ['http://www.svd.se/las-de-senaste-berglin-serierna-har']

    def parse(self, response):
        sel = Selector(response)
        images = sel.xpath("//ul[@class='ThumbnailList']/li/a/img/@src").extract()
        items = []
        for image_url in images:
          item = BerglingrabberItem()
          item['image_url'] = image_url

          # Use the base filename http://.../BASENAME.jpg as uuid.
          uuid = image_url.rsplit('/', 1)[-1].split('.', 1)[0]
          item['uuid'] = uuid

          get_title_line = 'wget %s -O - 2>/dev/null | exiftool -s3 -UserDefined239 -' % image_url
          self.log('Executing: ' + get_title_line)
          title = check_output(get_title_line, shell=True).rstrip()
          item['title']  = title

          items.append(item)

        return items
