import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://www.legalporno.com/hot-videos/',
    ]

    def parse(self, response):
        for quote in response.css('div.thumbnail-title gradient'):
            yield {
                'text': quote.css('a.title::text').extract_first(),
                # 'author': quote.xpath('span/small/text()').extract_first(),
            }

        next_page = response.css('li.next a::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
