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
    return find_review.attrs.get("class")[1] + rating


def find_category_book(soup_response):
    list_of_links = soup_response.find("ul", class_ = "breadcrumb").find_all("a")
    category = "Not found"
    for link in list_of_links:
        if "category/books/" in link["href"]:
            return link.string
    return category


def get_description_book(soup_response):
    description_book = "NOT FOUND DESCRIPTION"
    if soup_response.find("article", class_ = "product_page").find("p", recursive = False):
        description_book = soup_response.find("article", class_ = "product_page").find("p", recursive = False).string
    return description_book


def get_table_information(soup_response):
    table_information = {}
    keys = soup_response.find("table", class_ = "table").findAll("th")
    values = soup_response.find("table", class_ = "table").findAll("td")
    for key in keys:
        for value in values:
            table_information[key.string] = value.string
            values.remove(value)
            break
    return table_information


def get_information_book(url_to_download):
    information_book = []
    response = requests.get(url_to_download)
    if response.ok:
        soup = BeautifulSoup(response.content, "html.parser")
        table_information = get_table_information(soup)
        information_book.append(url_to_download)
        information_book.append(table_information["UPC"])
        information_book.append(soup.find("h1").string)
        information_book.append(table_information["Price (incl. tax)"])
        information_book.append(table_information["Price (excl. tax)"])
        information_book.append(table_information["Availability"])
        information_book.append(get_description_book(soup))
        information_book.append(find_category_book(soup))
        information_book.append(find_rating_review(soup))
        information_book.append(find_url_image(soup))
    return information_book
