import requests

from BooksPage.pages.all_books_page import AllBooksPage
from BooksPage.parsers.separate_book_parser import SeparateBookParser

page_content = requests.get("http://books.toscrape.com").content
page = AllBooksPage(page_content)

#page.make_csv()

books = []

for i in range(page.page_count):
    page_content = requests.get(f"http://books.toscrape.com/catalogue/page-{i+1}.html").content
    page = AllBooksPage(page_content)
    books.extend(page.books)

    page.make_csv()

for book in books:
    print(book)

# make links
links = [b.link for b in books]


for link in links:
    separate_page_content = requests.get(f"http://books.toscrape.com/catalogue/{link}").content
    separate_page = SeparateBookParser(separate_page_content)

    separate_page.save_content()


