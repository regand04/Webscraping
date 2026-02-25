import requests
from bs4 import BeautifulSoup

# Metod för webscraping
def scrape_books():
    # Spara URL i variabel
    url = "https://books.toscrape.com/"

    # GET-förfrågan till URL:en sparas i variabel
    response_obj = requests.get(url)
    # Sätter teckenkodning till utf-8
    response_obj.encoding = "utf-8"

    # Parsar HTML-innehållet till format som Python kan förstå och söka
    soup = BeautifulSoup(response_obj.text, "html.parser")

    # Hämtar alla bok-element på sidan
    books_html = soup.find_all("article", class_= "product_pod")

    scraped_books = [] # Skapa tom lista

    # Loopa igenom books_html (bok-element från websidan)
    for index, book_tag in enumerate(books_html, start=1):
        # Hämtar titel, pris, lagerstatus och betyg från html-koden
        title = book_tag.h3.a["title"]
        price = book_tag.find("p", class_="price_color").text
        stock = book_tag.find("p", class_="instock availability").text.strip()
        rating = book_tag.p["class"][1]  

        # Dictionary för varje bok läggs till i listan
        scraped_books.append({
            "id": index,
            "title": title,
            "price": price,
            "stock": stock,
            "rating": rating
        })
    # Returnerar de hämtade böckerna
    return scraped_books

def scrape_category():
    url = "https://books.toscrape.com/"
    # GET-förfrågan till URL:en sparas i variabel
    response_obj = requests.get(url)
    # Sätter teckenkodning till utf-8
    response_obj.encoding = "utf-8"

    # Parsar/tolka HTML-innehållet till format som Python kan förstå och söka
    soup = BeautifulSoup(response_obj.text, "html.parser")

    # Hämtar kategorier
    category_list = soup.find("ul", class_="nav nav-list")

    # Hämtar länkarna (alla <a> taggar)
    category_links = category_list.find_all("a")

    categories = []

    # Loopa igenom länkarna
    for link in category_links:
        # hämta text från länk och ta bort mellanslag och raddbrytningar
        category_name = link.text.strip()

        # Om namnet inte är books läggs kategorin in i listan
        if category_name != "Books":
            categories.append(category_name)

    # Returnerar de hämtade böckerna och kategorier
    return categories

