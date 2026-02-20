import requests
from bs4 import BeautifulSoup

def scrape_books():
    url = "https://books.toscrape.com/"
    response_obj = requests.get(url)
    response_obj.encoding = "utf-8"
    soup = BeautifulSoup(response_obj.text, "html.parser")
    books_html = soup.find_all("article", class_= "product_pod")

    scraped_books = []
    for index, book_tag in enumerate(books_html, start=1):
        title = book_tag.h3.a["title"]
        price = book_tag.find("p", class_="price_color").text
        stock = book_tag.find("p", class_="instock availability").text.strip()
        rating = book_tag.p["class"][1]  # t.ex. "Three", "Five"

        scraped_books.append({
            "id": index,
            "title": title,
            "price": price,
            "stock": stock,
            "rating": rating
        })
    return scraped_books

