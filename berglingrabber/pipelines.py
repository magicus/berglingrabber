# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime

import PyRSS2Gen

class BerglingrabberPipeline(object):
    rss_items = []

    def process_item(self, item, spider):
        rss_item = PyRSS2Gen.RSSItem(
            title = item['title'],
            link = item['image_url'],
            description = '&lt;img src="{}" title="{}" /&gt;'.format(
                item['image_url'], "Berglin " + item['title']),
            guid = item['uuid'])
        self.rss_items.append(rss_item)
        return item

    def close_spider(self, spider):
      rss_feed = PyRSS2Gen.RSS2(
          title = "Dagens Berglin",
          link = "http://www.svd.se/las-de-senaste-berglin-serierna-har",
          description = "Dagens Berglin",
          lastBuildDate = datetime.datetime.now(),
          items = self.rss_items)

      rss_feed.write_xml(open("berglin.rss", "w"))
