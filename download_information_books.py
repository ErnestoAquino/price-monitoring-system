import requests
import csv
from bs4 import BeautifulSoup
from get_information_book import get_information_book


def download_information():
    url_page = "https://books.toscrape.com/index.html"
    response = requests.get(url_page)
    dictionary_of_category = {}
    if response.status_code:
        soup = BeautifulSoup(response.content, "html.parser")
        # print(soup.find("ul", class_ = "nav-list").findAll("a", href = True))
        for link in soup.find("ul", class_ = "nav-list").find("ul").findAll("a", href = True):
            dictionary_of_category[link.string.strip()] = link["href"]
            # print(link.text, " - ", link["href"])


def download_information_book_of(file_name, category):
    write_header(file_name)
    pages_of_category = find_all_pages_of(category)
    links_of_books = find_all_links_books_category(pages_of_category)
    get_books_from_links(links_of_books, file_name)


def write_header(file_name):
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
    with open(file_name + ".csv", "w") as file:
        write = csv.writer(file, delimiter = ",")
        write.writerow(header)


def find_all_pages_of(category):
    index_page = "/index.html"
    category_without_index = category.removesuffix("/index.html")
    # url_complete = "https://books.toscrape.com/catalogue/category/books/" + category + index_page
    url_complete = "https://books.toscrape.com/" + category_without_index + index_page
    are_more_books = True
    urls = [url_complete]
    while are_more_books:
        response = requests.get(url_complete)
        if response.status_code:
            soup = BeautifulSoup(response.content, "html.parser")
            if soup.find("li", class_ = "next"):
                index_page = "/" + soup.find("li", class_ = "next").find("a")["href"]
                # url_complete = "https://books.toscrape.com/catalogue/category/books/" + category + index_page
                url_complete = "https://books.toscrape.com/" + category_without_index + index_page
                urls.append(url_complete)
            else:
                are_more_books = False
        else:
            are_more_books = False
    return urls


def find_all_links_books_category(urls_of_category):
    links = []
    for url in urls_of_category:
        test_response_category = requests.get(url)
        if test_response_category.status_code:
            test_soup_category = BeautifulSoup(test_response_category.content, "html.parser")
            # if test_soup_category.find("li", class_ = "next").find("a")["href"]:
            #     print("hay link next")
            for i in test_soup_category.find_all("h3"):
                links.append(i.find("a")["href"])
    return create_absolutes_urls(links)
    # get_books_from_links(completes_links, category)


def create_absolutes_urls(links):
    test_base_url = "https://books.toscrape.com/catalogue"
    complete_links = []
    for link in links:
        complete_links.append(link.replace("../../..", test_base_url))
    return complete_links


def get_books_from_links(links, file_name):
    for link in links:
        add_book_information(get_information_book(link), file_name)


def add_book_information(information_book, file_name):
    with open(file_name + ".csv", "a") as file_csv:
        writer = csv.writer(file_csv, delimiter = ",")
        writer.writerow(information_book)
