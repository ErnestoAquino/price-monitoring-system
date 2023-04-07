import requests
import csv
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
MESSAGE_ERROR_URL = "Sorry, but we have encountered a problem with the URL."
url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
# url = "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"
book_page = requests.get(url)
# remembrance esto a response
# print(book_page.content)
soup = BeautifulSoup(book_page.content, "html.parser")
title_book = soup.find("h1").string
# description_book = soup.find(id = "product_description", class_ = "sub-header")
# universal_product_code = soup.find("th")
image_url = soup.find("img")["src"]
# table_with_information = soup.find(class_ = "table")
keys = soup.find("table", class_ = "table").findAll("th")
values = soup.find("table", class_ = "table").findAll("td")
test_dictionary = {}

for key in keys:
    for value in values:
        test_dictionary[key.string] = value.string
        values.remove(value)
        break

print(test_dictionary)

# for value in values:
#     print(value.string)


# product_description = soup.find(id="product_description")
# for p in soup.select("p"):
#     print(p.get_text(strip = True, separator = "\n"))
#
# print(table_with_information)
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


def get_information_book(url_to_download):
    information_book = []
    response = requests.get(url_to_download)
    if response.ok:
        information_book.append(url_to_download)


def has_class_but_no_id(tag):
    return not tag.has_attr('class') and not tag.has_attr('id')


description_book = soup.find("article", class_ = "product_page").find("p", recursive = False).string
absolute_url = create_absolute_url(image_url)

print("Title book = ", title_book)
# print("UPC book = ", universal_product_code)
print("URL image = ", absolute_url)
print("Product description = ", description_book)
print(get_table_information(soup))
# write_header()

# print("URL image = ", image_url["src"])
# print(soup.find_all("h1"))
# print(soup.title.string)
# lista de campos a buscar:
#  product_page_url
# ● universal_ product_code (upc)
# ● title
# ● price_including_tax
# ● price_excluding_tax
# ● number_available
# ● product_description
# ● category
# ● review_rating
# ● image_url
