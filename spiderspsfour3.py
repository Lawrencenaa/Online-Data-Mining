import scrapy

class AmazonSpider(scrapy.Spider):
    name = 'amazon_games_ps4'
    allowed_domains = ['amazon.nl']
    start_urls = [f'https://www.amazon.nl/s?bbn=16242800031&rh=n%3A16480633031&fs=true&ref=lp_16480633031_sar']

    def parse(self, response):
        title_css = 'span.a-size-medium.a-color-base.a-text-normal::text'
        title_xpath = ('normalize-space(.//span[@class="a-size-medium a-color-base a-text-normal"]/text())')
        
        price_css = 'span.a-price-whole::text'
        price_xpath = ('normalize-space(.//span[@class="a-price-whole"]/text())')
        
        pegi_rating_css = 'span.a-size-base.a-color-secondary::text'
        pegi_rating_xpath = ('normalize-space(.//span[@class="a-size-base a-color-secondary"]/text())')
        
        platform_css = 'a.a-size-base.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-bold::text'
        platform_xpath = ('normalize-space(.//a[@class="a-size-base a-link-normal s-underline-text s-underline-link-text s-link-style a-text-bold"]/text())')
        
        
        for game in response.css('div.sg-col-inner'):
            yield {
                'title': game.css(title_css).get() or game.xpath(title_xpath).get(),
                'price': game.css(price_css).get() or game.xpath(price_xpath).get(),
                'pegi_rating': game.css(pegi_rating_css).get() or game.xpath(pegi_rating_xpath).get(),
                'platform': game.css(platform_css).get() or game.xpath(platform_xpath).get()
            }
            
        next_page_url = response.css('span.s-pagination-strip > a::attr(href)').extract()[-1]
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)