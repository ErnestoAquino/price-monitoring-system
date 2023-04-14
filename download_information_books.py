import requests
import csv
from datetime import date
from bs4 import BeautifulSoup
from get_information_book import get_information_book
from os.path import isdir
from os import mkdir


def download_information():
    url_page = "https://books.toscrape.com/index.html"
    response = requests.get(url_page)
    dictionary_of_category = {}
    if response.status_code:
        soup = BeautifulSoup(response.content, "html.parser")
        for link in soup.find("ul", class_ = "nav-list").find("ul").findAll("a", href = True):
            dictionary_of_category[link.string.strip()] = link["href"]
        for key in dictionary_of_category:
            download_information_book_of(key, dictionary_of_category[key])


def download_information_book_of(file_name, category):
    file = file_name + " " + str(date.today())
    write_header(file)
    pages_of_category = find_all_pages_of(category)
    links_of_books = find_all_links_books_category(pages_of_category)
    get_books_from_links(links_of_books, file)


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
    url_complete = "https://books.toscrape.com/" + category_without_index + index_page
    are_more_books = True
    urls = [url_complete]
    while are_more_books:
        response = requests.get(url_complete)
        if response.status_code:
            soup = BeautifulSoup(response.content, "html.parser")
            if soup.find("li", class_ = "next"):
                index_page = "/" + soup.find("li", class_ = "next").find("a")["href"]
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
        response_category = requests.get(url)
        if response_category.status_code:
            test_soup_category = BeautifulSoup(response_category.content, "html.parser")
            for i in test_soup_category.find_all("h3"):
                links.append(i.find("a")["href"])
    return create_absolutes_urls(links)


def create_absolutes_urls(links):
    base_url = "https://books.toscrape.com/catalogue"
    complete_links = []
    for link in links:
        complete_links.append(link.replace("../../..", base_url))
    return complete_links


def get_books_from_links(links, file_name):
    for link in links:
        information = get_information_book(link)
        add_book_information(information, file_name)
        # download_image(information)


def add_book_information(information_book, file_name):
    with open(file_name + ".csv", "a") as file_csv:
        writer = csv.writer(file_csv, delimiter = ",")
        writer.writerow(information_book)


def download_image(information_book):
    path_image = "images/" + information_book[7]
    name_image = information_book[2].replace("/", " ")
    print(name_image)
    png = "./images/" + information_book[7] + "/" + name_image + ".png"
    print(png)
    if not isdir("images"):
        mkdir("images")
    if not isdir(path_image):
        mkdir(path_image)
    with open(png, "wb") as file:
        file.write(requests.get(information_book[9], stream = True).content)
