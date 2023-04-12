import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"


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


def get_description_book(s):
    description_book = "NOT FOUND DESCRIPTION"
    if s.find("article", class_ = "product_page").find("p", recursive = False):
        description_book = s.find("article", class_ = "product_page").find("p", recursive = False).string
    return description_book


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