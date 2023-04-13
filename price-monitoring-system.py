import requests
from bs4 import BeautifulSoup
from download_information_books import download_information_book_of


# BASE_URL = "https://books.toscrape.com/"
# MESSAGE_ERROR_URL = "Sorry, but we have encountered a problem with the URL."
# url = "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"


download_information_book_of("Sequential Art", "catalogue/category/books/sequential-art_5/index.html")
url_page = "https://books.toscrape.com/index.html"
response = requests.get(url_page)
dictionary_of_category = {}
if response.status_code:
    soup = BeautifulSoup(response.content, "html.parser")
    # print(soup.find("ul", class_ = "nav-list").findAll("a", href = True))
    for link in soup.find("ul", class_ = "nav-list").find("ul").findAll("a", href = True):
        dictionary_of_category[link.string.strip()] = link["href"]
        # print(link.text, " - ", link["href"])

print(dictionary_of_category)
print(len(dictionary_of_category))

# test_url = "catalogue/category/books/travel_2/index.html"
# print(test_url.removesuffix("/index.html"))
