import scrapy
#.nav-bar .item


class OutfittersSpider(scrapy.Spider):
    name = 'outfitters_spider'
    start_urls = [
        'https://outfitters.com.pk/collections/new-men',
        ]
    
    def parse(self, response):
        url = response.url
        #for href in response.css('.main-banner-items .index-link'):
            #url = response.urljoin(css('::attr(href)').extract()) 
        yield scrapy.Request(
            url,
           callback = self.parse_main_page
           )
    
    def parse_main_page(self, response):
        for p in response.css('.col-6 .product-item .inner-top .product-top .product-image'):
            item = {}
            product_url = p.css('a::attr(href)').extract_first()
            item['url'] = response.urljoin(product_url)
            yield scrapy.Request(
                response.urljoin(product_url),
                meta={'item': item},
                dont_filter=True,
                callback=self.parse_product_page
            )     

    def parse_product_page(self, response):
        item = response.meta.get('item', {})
        my_list = []

        item['sku_id'] = response.css('.sku-product span::text').extract_first()
        item['Title'] = response.css('.product-shop .product-title span::text').extract_first()
        item['brand'] = response.css('.header-items .header-logo .logo-img .lazyloaded alt').extract_first()
        item['Description'] = response.css('.product-shop ul li::text').extract()

        for im in response.css('.slider-nav .item'):
            my_list.append(im.css('a ::attr(data-image)').extract_first())

        item['image_urls'] = my_list

        my_list = []

        for s in response.css('.size .available'):
            sku = {
                'size' : s.css('::attr(data-value)').extract_first(),
                'colour' : response.css('.Rcolor-header .Rcolor-label span::text').extract_first(),
                'Price' : response.css('.product-shop .price .money::text').extract_first(),

            }
            my_list.append(sku)

        item['skus'] = my_list

        yield item