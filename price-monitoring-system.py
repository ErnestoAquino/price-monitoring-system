import requests
import csv
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
MESSAGE_ERROR_URL = "Sorry, but we have encountered a problem with the URL."
url = "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"


def find_url_image(soup_response):
    relative_url = soup_response.find("img")["src"]
    if relative_url.startswith("../../"):
        complete_url = relative_url.replace("../..", BASE_URL)
        return complete_url


def find_rating_review(soup_response):
    rating = " / Five"
    find_review = soup_response.select_one(".star-rating")
    # print(find_review.attrs.get("class")[1])
    return find_review.attrs.get("class")[1] + rating


def find_category_book(soup_response):
    list_of_links = soup_response.find("ul", class_ = "breadcrumb").find_all("a")
    category = "Not found"
    for link in list_of_links:
        if "category/books/" in link["href"]:
            return link.string
    return category


def get_table_information(soup_response):
    table_information = {}
    keys_t = soup_response.find("table", class_ = "table").findAll("th")
    values_t = soup_response.find("table", class_ = "table").findAll("td")
    for key_t in keys_t:
        for value_t in values_t:
            table_information[key_t.string] = value_t.string
            values_t.remove(value_t)
            break
    return table_information


def create_absolute_url(relative_url):
    if relative_url.startswith("../.."):
        complete_url = relative_url.replace("../../", BASE_URL)
        return complete_url
    else:
        return MESSAGE_ERROR_URL


def write_header():
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
    with open("test_file.cvs", "w") as test_file:
        write = csv.writer(test_file, delimiter = ",")
        write.writerow(header)


def get_description_book(s):
    d_book = s.find("article", class_ = "product_page").find("p", recursive = False).string
    return d_book


def get_information_book(url_to_download):
    information_book = []
    response = requests.get(url_to_download)
    if response.ok:
        soup_t = BeautifulSoup(response.content, "html.parser")
        table_t = get_table_information(soup_t)
        information_book.append(url_to_download)
        information_book.append(table_t["UPC"])
        information_book.append(soup_t.find("h1").string)
        information_book.append(table_t["Price (incl. tax)"])
        information_book.append(table_t["Price (excl. tax)"])
        information_book.append(table_t["Availability"])
        information_book.append(get_description_book(soup_t))
        information_book.append(find_category_book(soup_t))
        information_book.append(find_rating_review(soup_t))
        information_book.append(find_url_image(soup_t))
    return information_book


def add_book_information(information_book):
    with open("test_file.cvs", "a") as file_cvs:
        writer = csv.writer(file_cvs, delimiter = ",")
        writer.writerow(information_book)


url_category = "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"


def test_find_all_books_category_url(test_url_category):
    links = []
    test_response_category = requests.get(test_url_category)
    if test_response_category.status_code:
        test_soup_category = BeautifulSoup(test_response_category.content, "html.parser")
        for i in test_soup_category.find_all("h3"):
            print(i.find("a")["href"])
            links.append(i.find("a")["href"])
    print(len(links))

test_find_all_books_category_url(url_category)
