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
            url = row.css("td.titleColumn a::attr(href)").get() + "reviews"
            yield response.follow(
                url, 
                callback=self.parse_review_page,
            )
    
    def parse_review_page(self, response):
        movie_title = response.css("div.subpage_title_block h3 a::text").get()
        for review in response.css("div.imdb-user-review"):
            try:
                review_content = (
                    review
                    .css("div.content div.text")
                    .re("<div .+?>(.+)</div>")
                    [0]
                    .replace("<br>", " ")
                )
            except IndexError:
                continue
            yield { 
                "movie_title": movie_title,
                "rating": review.css("span.rating-other-user-rating span::text").get(),
                "title": review.css("a.title::text").get(),
                "user": review.css("span.display-name-link a::text").get(),
                "date": review.css("span.review-date::text").get(),
                "content": review_content,
            }