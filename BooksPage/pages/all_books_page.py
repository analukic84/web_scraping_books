import re
from bs4 import BeautifulSoup
import csv
import os.path

from BooksPage.locators.all_books_locator import AllBooksPageLocators
from BooksPage.parsers.book_parser import BookParser


class AllBooksPage:
    def __init__(self, page_content):
        self.soup = BeautifulSoup(page_content, "html.parser")

        self.filename = "books.csv"

    @property
    def books(self):
        locator = AllBooksPageLocators.BOOKS_LOCATOR
        books = self.soup.select(locator)
        return [BookParser(book) for book in books]

    @property
    def page_count(self):
        locator = AllBooksPageLocators.PAGE_LOCATOR
        page_count = self.soup.select_one(locator).string.strip()
        page_number = re.search("Page [0-9]+ of ([0-9]+)", page_count)
        page_number = page_number.group(1)
        return int(page_number)

    def make_csv(self):
        book_dict_list = [b.book_dict for b in self.books]
        print("book_dict_list", book_dict_list)

        keys = book_dict_list[0].keys()

        file_exists = os.path.isfile(self.filename)

        with open(self.filename, "a", newline='') as file:
            dict_writer = csv.DictWriter(file, keys)

            if not file_exists:
                dict_writer.writeheader()
            else:
                dict_writer.writerows(book_dict_list)
