import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'author'

    # start at the main page
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # follow links to author pages
        for href in response.css('.author + a::attr(href)'):
            # for each author link, call self.parse_author
            yield response.follow(href, self.parse_author)

        # follow pagination links
        for href in response.css('li.next a::attr(href)'):
            # for each new page, come back to this parse method to
            # find new authors
            yield response.follow(href, self.parse)

    def parse_author(self, response):
        # helper function to get text at a css path
        def extract_with_css(query):
            return response.css(query).get(default='').strip()
        
        # get the data we are after, using css selection paths
        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }