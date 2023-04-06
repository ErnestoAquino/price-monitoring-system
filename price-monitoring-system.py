import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
MESSAGE_ERROR_URL = "Sorry, but we have encountered a problem with the URL."
url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
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
for key in keys:
    print(key.string)

for value in values:
    print(value.string)
# product_description = soup.find(id="product_description")
# for p in soup.select("p"):
#     print(p.get_text(strip = True, separator = "\n"))
#
# print(table_with_information)


def create_absolute_url(relative_url):
    if relative_url.startswith("../.."):
        complete_url = relative_url.replace("../../", BASE_URL)
        return complete_url
    else:
        return MESSAGE_ERROR_URL


def create_key_table():
    pass


def has_class_but_no_id(tag):
    return not tag.has_attr('class') and not tag.has_attr('id')


description_book = soup.find("article", class_ = "product_page").find("p", recursive = False).string
absolute_url = create_absolute_url(image_url)

print("Title book = ", title_book)
# print("UPC book = ", universal_product_code)
print("URL image = ", absolute_url)
print("Product description = ", description_book)

# print("URL image = ", image_url["src"])
# print(soup.find_all("h1"))
# print(soup.title.string)
