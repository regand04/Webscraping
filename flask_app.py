from flask import Flask, request, jsonify
from webscraping_bp import scrape_books
from book_data_bp import load_books, save_books, add_book, update_book, remove_book

# Skapa flask-appen
app = Flask(__name__)

# Om load_books() är tom körs scrape_books() som sparas i save_books()
if not load_books():
    save_books(scrape_books())

# Funktionen home() körs vid GET-förfrågan till root-URL:en (/)
@app.route("/", methods = ["GET"])
def home():
    # Startsida
    return "Hello from flask"

# Funktionen get_books() körs vid en GET-förfågan till URL:en nedan
@app.route("/api/v1/books", methods = ["GET"])
# Metod som anropar metoden load_books() och sparar i variabeln books
def get_books():
    books = load_books()
    # Omvandlar python-objektet till JSON-format
    # 200 ==> HTTP-statuskod OK
    return jsonify(books), 200

# Endpoint gäller för en bestämd bok. ID ska vara heltal
@app.route("/api/v1/books/<int:book_id>", methods = ["GET"])
def get_book(book_id):
    # Laddar  böcker
    books = load_books()

    # Loopa igenom böckerna för att hitta rätt ID
    for book in books:
        if book["id"] == book_id:
            # Returnera efterfrågade bok som JSON med statuskod OK
            return jsonify(book), 200
    # Om ID:et inte hittas returneras felmeddelande
    # 404 = not found
    return jsonify({"error" : "Book Not Found"}), 404

# Funktionen post_book() körs om en POST-förfrågan ges till URL:en
@app.route("/api/v1/books", methods = ["POST"])
def post_book():
    # Hämtar JSON-data som skickades i HTTP-förfrågan ==> python dictionary
    new_book = request.json

    # Kollar om JSON-datan innehåller både ID och titel
    if "id" not in new_book or "title" not in new_book:
        # OM något saknas returneras felmeddelande (400 = bad request)
        return jsonify({"error" : "Book Must Have ID And Title"}), 400
    # Testa att spara boken
    if not add_book(new_book):
        # OM ID:et redan finns returneras felmeddelande
        return jsonify({"error" : "Book With This ID Already Exists."}),  400
    # Annars returneras den nya boken som JSON med statuskod 201 (created)
    return jsonify(new_book), 201

@app.route("/api/v1/books/<int:book_id>", methods = ["PUT"])
def put_book(book_id):
    updated_data = request.json
    if update_book(book_id, updated_data):
        books = load_books()
        for book  in books:
            if book["id"] == book_id:
                return jsonify(book), 200
    return jsonify({"error" :  "Book Not Found"}), 404

@app.route("/api/v1/books/<int:book_id>", methods = ["DELETE"])
def delete_book(book_id):
    if not remove_book(book_id):
        return jsonify({"error": "Book Not Found"}), 404
    return jsonify({"message" : f"Book {book_id} deleted"}), 200

# Starta Flask-servern om filen körs direkt (inte importerad)
if __name__ == "__main__":
    app.run(debug = True)






