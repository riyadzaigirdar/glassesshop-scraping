# -*- coding: utf-8 -*-
import scrapy


class GlassSpider(scrapy.Spider):
    name = 'glass'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers']

    def get_price(self, selector):
        original_price = selector.xpath(".//del/text()").get()
        if original_price is not None:
            return original_price
        else:
            return selector.xpath(".//div[@class='row']/div[contains(@class, 'pprice')]/span/text()").get()

    def parse(self, response):
        products = response.xpath("//div[@class='col-sm-6 col-md-4 m-p-product']")
        
        for product in products:
            name = product.xpath(".//div[@class='row']/p/a/text()").get()

            price = self.get_price(product)

            product_url = product.xpath(".//div[@class='pimg default-image-front']/a/@href").get()
            image_url = product.xpath(".//div[@class='pimg default-image-front']/a/img[1]/@src").get()
            
            yield {
                'name' : name,
                'price' : price,
                'product_url' : product_url,
                'image_url' : image_url 
            }

        next_page = response.xpath("//ul[@class='pagination']/li[position() = last()]/a/@href").get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
        
       
            