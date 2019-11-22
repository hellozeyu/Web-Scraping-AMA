from scrapy import Spider, Request 
from metacritic.items import MetacriticItem
import re 

class MetaCriticSpider(Spider):
    name = 'metacritic_spider'
    allowed_domains = ['www.metacritic.com']
    start_urls = ['https://www.metacritic.com/browse/movies/score/metascore/all/filtered?page=0']

    # find individual page of the movie list 
    def parse(self, response):
        # find the total number of pages
        total_number = int(response.xpath('//ul[@class="pages"]/li[@class="page last_page"]/a/text()').extract_first())
        result_urls = ['https://www.metacritic.com/browse/movies/score/metascore/all/filtered?page={}'.format(x) for x in range(0,total_number)]
        for url in result_urls[:2]:
            yield Request(url=url, callback=self.parse_result_page)

    def parse_result_page(self, response):
        # find the url of the movie detail page
        detail_urls = response.xpath('//td[@class="clamp-summary-wrap"]/a/@href').extract()
        review_pages = ['https://www.metacritic.com{}'.format(x) for x in detail_urls]
        for review in review_pages:
            yield Request(url=review, callback=self.parse_review_page)
        
    def parse_review_page(self, response):
        # movie title, genre, release date
        movie_title = response.xpath('//div[@class="product_page_title oswald"]/h1/text()').extract()[0]
        genre = response.xpath('//div[@class="genres"]/span[2]/span/text()').extract()
        release_date = response.xpath('//span[@class="release_date"]/span[2]/text()').extract()[0]

        # metascore is a little bit tricky. if they don't exist, we will impute them with None type object
        try:
            metascore = response.xpath('//div[contains(@class, "metascore_w larger movie")]/text()').extract_first()
            meta_positive, meta_mixed, meta_negative = response.xpath('//div[@class="distribution"]')[0].xpath('.//div[@class="count fr"]/text()').extract()
        except:
            metascore = meta_positive = meta_mixed = meta_negative = None

        try:
            userscore = response.xpath('//div[contains(@class, "metascore_w user larger movie")]/text()').extract_first()
            user_positive, user_mixed, user_negative = response.xpath('//div[@class="distribution"]')[1].xpath('.//div[@class="count fr"]/text()').extract()
        except:
            userscore = user_positive = user_mixed = user_negative = None

        # initialize an empty object for each movie
        item = MetacriticItem()
        item['movie_title'] = movie_title
        item['release_date'] = release_date
        item['genre'] = genre

        item['metascore'] = metascore
        item['userscore'] = userscore

        item['meta_positive'] = meta_positive
        item['meta_mixed'] = meta_mixed
        item['meta_negative'] = meta_negative
        item['user_positive'] = user_positive
        item['user_mixed'] = user_mixed
        item['user_negative'] = user_negative

        yield item
