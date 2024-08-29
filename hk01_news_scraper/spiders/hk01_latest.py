import scrapy
from scrapy_playwright.page import PageMethod
from hk01_news_scraper.items import Hk01NewsItem
from dateutil import parser
from datetime import datetime, timedelta, timezone

class HK01LatestSpider(scrapy.Spider):
    name = "hk01_latest"
    allowed_domains = ["hk01.com"]
    start_urls = ["https://www.hk01.com/latest"]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", ".content-card--article"),
                    PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                ],
            },
        )

    def parse(self, response):
        articles = response.css(".content-card--article")
        for article in articles:
            # Extract channel from the cardheader div
            channel = article.css(".cardheader font::text").get()

            # Extract time and check if it's within the last hour
            time_str = article.css("time::attr(datetime)").get()
            article_time = parser.parse(time_str)

            # Convert current time to UTC timezone-aware datetime
            current_time = datetime.now(timezone.utc)

            if current_time - article_time > timedelta(hours=1):
                break

            # Extract title and link
            title = article.css(".card-title::text").get()
            link = article.css(".card-title::attr(href)").get()
            full_link = response.urljoin(link)

            # Store data in the item
            item = Hk01NewsItem(
                channel=channel,
                time=time_str,
                title=title,
                link=full_link
            )
            yield item
