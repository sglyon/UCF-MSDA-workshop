import scrapy


class MovieSpider(scrapy.Spider):
    name = 'movie'

    # start at the main page
    start_urls = ['https://www.imdb.com/chart/top/']

    def parse(self, response):       
        for row in response.css("tbody.lister-list tr"):
            # TODO: process each row
            
            yield {
                "rank": row.css("td.titleColumn::text").get().strip().strip("."),
                "title": row.css("td.titleColumn a::text").get(),
                "link": row.css("td.titleColumn a::attr(href)").get(),
                "rating": row.css("td.imdbRating strong::text").get(),
                "year": row.css("td.titleColumn span.secondaryInfo::text").get(),
            }