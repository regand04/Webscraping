import json
import os

# Sparar JSON-filen i variabeln
JSON_BOOKS_FILE = "books.json"

# Metod för att ladda böcker
def load_books():
    # OM JSON-filen inte finns returneras en tom lista
    if not os.path.exists(JSON_BOOKS_FILE):
        return []
    # Annars öppnas JSON-filen och dess innehåll returneras som Python-objekt
    with open(JSON_BOOKS_FILE, "r") as file:
        return json.load(file)

# Metod för att spara böcker
def save_books(books):
    # Öppnar JSON-filen i skriv-läge
    with open(JSON_BOOKS_FILE, "w", encoding = "utf-8") as file_obj:
        # Sparar Python-objektet books som JSON i filen
        json.dump(books, file_obj, indent=4, ensure_ascii = False)

# Metod för att lägga till bok
def add_book(book):
    # Ladda böcker till variabel
    books = load_books()

    # Loopa igenom laddade böcker
    for existing_book in books:
        if existing_book["id"] == book["id"]:
            # OM ID:et redan finns returneras False
            return False
    # Vid nytt ID läggs den nya boken till i listan
    books.append(book)

    # Den uppdaterade listan sparas i JSON-filen
    save_books(books)
    # True returneras när boken lagts till
    return True

# Metod för att uppdatera en bok
def update_book(book_id, new_data):
    # Ladda böcker till variabel
    books = load_books()

    # Loopa igenom böckerna med index
    for i, book in enumerate(books):
        if book["id"] == book_id:
            # Boken uppdateras av nya värden från new_data
            books[i].update(new_data)

            # Den uppdaterade listan sparas i JSON-filen och True returneras
            save_books(books)
            return True
    # OM ID:et inte hittas returneras False
    return False

# Metod för att ta bort bok
def remove_book(book_id):
    # Ladda böcker till variabel
    books = load_books()

    # En lista som innehåller alla böcker utan det angivna ID:et skapas
    new_books = [book for book in books if book["id"] != book_id]

    # Om längden på listorna är samma togs ingen bok bort, False returneras
    if len(new_books) == len(books):
        return False

    # Om längden är olika sparas den uppdaterade listan (new_books) i JSON-filen och True returneras
    save_books(new_books)
    return True

