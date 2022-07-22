import scrapy


class QuotesSpider(scrapy.Spider):
    # name for spider -- important in larger projects
    name = 'quotes'
    
    # all urls for which scrapy should initiate this spider
    start_urls = [
        'http://quotes.toscrape.com/tag/humor/',
    ]
    
    # parse method -- after scrapy fetches the website it will
    # call `parse` and set `response` equal to the website content
    def parse(self, response):
        
        # remember that quotes are in a `div` element with class `quote`?
        for quote in response.css('div.quote'):
            
            yield {
                # ... and that inside that div we have `span` with `.text`?
                'text': quote.css('span.text::text').get(),
                'author': quote.xpath('span/small/text()').get(),
#                 'author': quote.css('small.author::text').get(),
            }
        
        # at the bottom of the page there's a list item with class
        # next. Inside it is a link -- we want the link destination,
        # which is given to us with the `href` attribute
        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)