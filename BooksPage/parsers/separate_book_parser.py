import re
import requests
import os
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from BooksPage.locators.separate_book_locators import SeparateBookLocators

PAGE_URL = "http://books.toscrape.com"


class SeparateBookParser:
    characters = ['?', '.', '!', '/', ';', ':', '#', '"', '%', '*']

    ratings = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    def __init__(self, separate_page_content):
        self.parent = BeautifulSoup(separate_page_content, "html.parser")

        locator = SeparateBookLocators.P_I_ALL_TYPE_LOCATOR
        self.p_i_all_type = self.parent.select(locator)

        locator = SeparateBookLocators.P_I_ALL_CONTENT_LOCATOR
        self.p_i_all_content = self.parent.select(locator)

        self.title_file_name = self.title
        for char in SeparateBookParser.characters:
            if char in self.title_file_name:
                self.title_file_name = self.title_file_name.replace(char, " ")[:30].strip()
                self.title_file_name = self.title_file_name.replace("  ", " ")

        print("naziv", self.title_file_name)

        # create directory
        self.file_path = f"Books/Book {self.title_file_name}/{self.title_file_name}.txt"
        directory = os.path.dirname(self.file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    @property
    def title(self):
        locator = SeparateBookLocators.TITLE_LOCATOR
        title = self.parent.select_one(locator).string
        return title

    @property
    def price(self):
        locator = SeparateBookLocators.PRICE_LOCATOR
        self.full_price = self.parent.select_one(locator).string
        price_re = re.search("£([0-9]+\.[0-9]+)", self.full_price)
        price_number = price_re.group(1)
        return price_number

    @property
    def in_stock(self):
        locator = SeparateBookLocators.IN_STOCK_LOCATOR
        in_stock = self.parent.select_one(locator).text.strip()
        return in_stock

    @property
    def rating(self):
        locator = SeparateBookLocators.RATING_LOCATOR
        rating_class = self.parent.select_one(locator)["class"]
        rating_class = [r for r in rating_class if r != "star-rating"][0]
        rating_class_number = SeparateBookParser.ratings[rating_class]
        return rating_class_number

    @property
    def description(self):
        locator = SeparateBookLocators.DESCRIPTION_LOCATOR
        description = self.parent.select(locator)[3].string
        return description

    @property
    def image(self):
        locator = SeparateBookLocators.IMAGE_LOCATOR
        image_link = self.parent.select_one(locator).attrs["src"]
        image_url = urljoin(PAGE_URL, image_link)
        return image_url

    @property
    def p_i_upc_type(self):
        p_i_upc_type = self.p_i_all_type[0].string
        return p_i_upc_type

    @property
    def p_i_upc_content(self):
        p_i_upc_content = self.p_i_all_content[0].string
        return p_i_upc_content

    @property
    def p_i_pt_type(self):
        p_i_pt_type = self.p_i_all_type[1].string
        return p_i_pt_type

    @property
    def p_i_pt_content(self):
        p_i_pt_content = self.p_i_all_content[1].string
        return p_i_pt_content

    @property
    def p_i_price_type(self):
        p_i_price_type = self.p_i_all_type[2].string
        return p_i_price_type

    @property
    def p_i_price_content(self):
        p_i_price_content = self.p_i_all_content[2].string
        return p_i_price_content

    @property
    def p_i_price1_type(self):
        p_i_price1_type = self.p_i_all_type[3].string
        return p_i_price1_type

    @property
    def p_i_price1_content(self):
        p_i_price1_content = self.p_i_all_content[3].string
        return p_i_price1_content

    @property
    def p_i_tax_type(self):
        p_i_tax_type = self.p_i_all_type[4].string
        return p_i_tax_type

    @property
    def p_i_tax_content(self):
        p_i_tax_content = self.p_i_all_content[4].string
        return p_i_tax_content

    @property
    def p_i_av_type(self):
        p_i_av_type = self.p_i_all_type[5].string
        return p_i_av_type

    @property
    def p_i_av_content(self):
        p_i_av_content = self.p_i_all_content[5].string
        return p_i_av_content

    @property
    def p_i_rev_type(self):
        p_i_rev_type = self.p_i_all_type[6].string
        return p_i_rev_type

    @property
    def p_i_rev_content(self):
        p_i_rev_content = self.p_i_all_content[6].string
        return p_i_rev_content

    def save_content(self):
        image_url = self.image
        with open(f"Books/Book {self.title_file_name}/{self.title_file_name}.jpg", "wb") as f:
            f.write(requests.get(image_url).content)

        with open(self.file_path, "w") as file:
            try:
                file.writelines(f"Title: {self.title}\n"
                            f"Price: {self.price} pounds ({self.full_price})\n"
                            f"{self.in_stock}\n"
                            f"Rating: {self.rating}\n"
                            f"Desccription: {self.description}\n\n"
                            f"Table content:\n"
                            f"{self.p_i_upc_type}: {self.p_i_upc_content}\n"
                            f"{self.p_i_pt_type}: {self.p_i_pt_content}\n"
                            f"{self.p_i_price_type}: {self.p_i_price_content}\n"
                            f"{self.p_i_price1_type}: {self.p_i_price1_content}\n"
                            f"{self.p_i_tax_type}: {self.p_i_tax_content}\n"
                            f"{self.p_i_av_type}: {self.p_i_av_content}\n"
                            f"{self.p_i_rev_type}: {self.p_i_rev_content}")
            except:
                pass
