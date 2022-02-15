import re
import os
import csv

from BooksPage.locators.book_locator import BookLocator


class BookParser:

    RATINGS = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    def __init__(self, parent):
        self.parent = parent

    def __repr__(self):
        return f"<Book title: {self.title} has price £{self.price} and rating with {self.rating} stars>"

    @property
    def title(self):
        locator = BookLocator.TITLE_LOCATOR
        title = self.parent.select_one(locator).attrs["title"].strip()
        return title

    @property
    def link(self):
        locator = BookLocator.LINK_LOCATOR
        link = self.parent.select_one(locator).attrs["href"]
        return link

    @property
    def price(self):
        locator = BookLocator.PRICE_LOCATOR
        price = self.parent.select_one(locator).string
        price_number = re.search("£([0-9]+\.[0-9]+)", price).group(1)
        return float(price_number)

    @property
    def rating(self):
        locator = BookLocator.RATING_LOCATOR
        rating = self.parent.select_one(locator).attrs["class"]
        only_rating = [rate for rate in rating if rate != "star-rating"][0]
        rating_number = BookParser.RATINGS.get(only_rating)
        return rating_number

    @property
    def book_dict(self):
        book = {
            "title": self.title,
            "link": self.link,
            "price": self.price,
            "rating": self.rating
        }
        return book

