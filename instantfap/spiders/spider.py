# -*- coding: utf-8 -*-
import scrapy
import json
import re
from instantfap.items import InstantfapItem


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['instantfap.com']
    image_base_url = 'http://instantfap.com/image/'
    image_urls = []
    count = 0
    url_begin = 'http://instantfap.com/load.php?category=home&count='
    url_end = '&q=&contentFilters=gif,static&contentSort=hottest'
    start_urls = [url_begin + str(count) + url_end]

    def parse(self, response):

        item = InstantfapItem()
        image_datas = json.loads(response.body)
        image_datas = eval(re.sub('null', 'None', image_datas))
        for image in image_datas:
            item['image_suffix'] = image['ext']
            imgur_id = image['imgur_id']
            self.image_urls.append(self.image_base_url + imgur_id + '.' + image['ext'])
        item['image_urls'] = self.image_urls
        yield item

        self.count += 50
        next_url = self.url_begin + str(self.count) + self.url_end

        yield scrapy.Request(next_url, callback=self.parse)

