import json
import os

JSON_BOOKS_FILE = "books.json"

def load_books():
    if not os.path.exists(JSON_BOOKS_FILE):
        return []
    with open(JSON_BOOKS_FILE, "r") as file:
        return json.load(file)

def save_books(books):
    with open(JSON_BOOKS_FILE, "w", encoding = "utf-8") as file_obj:
        json.dump(books, file_obj, indent=4, ensure_ascii = False)

def add_book(book):
    books = load_books()
    for existing_book in books:
        if existing_book["id"] == book["id"]:
            return False
    books.append(book)
    save_books(books)
    return True

def update_book(book_id, new_data):
    books = load_books()
    for i, book in enumerate(books):
        if book["id"] == book_id:
            books[i].update(new_data)
            save_books(books)
            return True
    return False

def remove_book(book_id):
    books = load_books()
    new_books = [book for book in books if book["id"] != book_id]
    if len(new_books) == len(books):
        return False
    save_books(new_books)
    return True

