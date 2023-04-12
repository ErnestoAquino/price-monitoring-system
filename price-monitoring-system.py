import requests
import csv
from bs4 import BeautifulSoup
from get_information_book import get_information_book

BASE_URL = "https://books.toscrape.com/"
MESSAGE_ERROR_URL = "Sorry, but we have encountered a problem with the URL."
url = "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"


def create_absolute_url(relative_url):
    if relative_url.startswith("../.."):
        complete_url = relative_url.replace("../../", BASE_URL)
        return complete_url
    else:
        return MESSAGE_ERROR_URL


def write_header(category):
    header = [
        "product_page_url",
        "universal_ product_code (upc)",
        "title",
        "price_including_tax",
        "price_excluding_tax",
        "number_available",
        "product_description",
        "category",
        "review_rating",
        "image_url"
    ]
    with open(category + ".csv", "w") as file:
        write = csv.writer(file, delimiter = ",")
        write.writerow(header)


def add_book_information(information_book, category):
    with open(category + ".csv", "a") as file_csv:
        writer = csv.writer(file_csv, delimiter = ",")
        writer.writerow(information_book)


# Test functions to retrieve books from a category
url_category = "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"


def test_find_all_books_category_url(urls_of_category):
    links = []
    for url in urls_of_category:
        test_response_category = requests.get(url)
        if test_response_category.status_code:
            test_soup_category = BeautifulSoup(test_response_category.content, "html.parser")
            # if test_soup_category.find("li", class_ = "next").find("a")["href"]:
            #     print("hay link next")
            for i in test_soup_category.find_all("h3"):
                # print(i.find("a")["href"])
                links.append(i.find("a")["href"])
    return test_create_absolutes_urls(links)


def test_create_absolutes_urls(links):
    test_base_url = "https://books.toscrape.com/catalogue"
    complete_links = []
    for link in links:
        complete_links.append(link.replace("../../..", test_base_url))
    return complete_links


def test_get_all_books_of_one_page(links, category):
    for link in links:
        add_book_information(get_information_book(link), category)


def find_all_books_of(category):
    index_page = "/index.html"
    url_complete = "https://books.toscrape.com/catalogue/category/books/" + category + index_page
    are_more_books = True
    urls = [url_complete]
    while are_more_books:
        response = requests.get(url_complete)
        if response.status_code:
            soup = BeautifulSoup(response.content, "html.parser")
            if soup.find("li", class_ = "next"):
                index_page = "/" + soup.find("li", class_ = "next").find("a")["href"]
                url_complete = "https://books.toscrape.com/catalogue/category/books/" + category + index_page
                urls.append(url_complete)
            else:
                are_more_books = False
    return urls


urls_para_descargar = (find_all_books_of("classics_6"))
libros = test_find_all_books_category_url(urls_para_descargar)
write_header("classics_6")
test_get_all_books_of_one_page(libros, "classics_6")
