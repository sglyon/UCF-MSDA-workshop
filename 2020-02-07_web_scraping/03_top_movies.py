import scrapy


class MovieSpider(scrapy.Spider):
    name = 'movie'

    # start at the main page
    start_urls = ['https://www.imdb.com/chart/top/']

    def parse(self, response):
        yeild {
            "rank": response.css("td.titleColumn::text").get().strip().strip(".")
        }
        
        for row in response.css("tbody.lister-list tr"):
            # TODO: process each row
            yield {
                "rank": None,
                "title": None,
                "link": None,
                "rating": None,
                "year": None,
            }