import scrapy


class AljazeeraSpider(scrapy.Spider):
    name = 'article_spider'
    start_urls = ['https://www.aljazeera.com/opinion/']

    def parse(self, response):
        article_list = response.css('.gc--with-image')

        for article in article_list:
            item ={
                'name' : article.css('.gc__title span::text').extract(),
                'url' :  "https://www.aljazeera.com"  + article.css('.gc__title a::attr(href)').extract_first(),
                'author' : article.css('.author-link::text').extract(),
            }
            
            yield item
