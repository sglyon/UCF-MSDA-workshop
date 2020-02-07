import scrapy


class ReviewSpider(scrapy.Spider):
    name = 'reviews'

    # start at the main page
    start_urls = ['https://www.imdb.com/chart/top/']

    def parse(self, response):       
        for row in response.css("tbody.lister-list tr"):
            # TODO: find imdb id for movie
            #       construct the reviews url
            #       follow it, while passing the movie title as a kwarg
            id = None
            url = None
            movie_title = None
            yield response.follow(
                url, callback=parse_review_page,
                movie_title=movie_title,
            )
    
    def parse_review_page(self, response, movie_title):
        for review in response.css("TODO"):
            # TODO: extract the info
            yield { 
                "movie_title": movie_title,
                "rating":None,
                "title": None,
                "user": None,
                "date": None,
                "content": None,
            }