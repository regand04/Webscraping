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

@app.route("/api/v1/books/<int:book_id>", methods = ["GET"])
def get_book(book_id):
    books = load_books()
    for book in books:
        if book["id"] == book_id:
            return jsonify(book), 200
    return jsonify({"error" : "Book Not Found"}), 404

@app.route("/api/v1/books", methods = ["POST"])
def post_book():
    new_book = request.json

    #Krav att ha id och titel
    if "id" not in new_book or "title" not in new_book:
        return jsonify({"error" : "Book Must Have ID And Title"}), 400
    if not add_book(new_book):
        return jsonify({"error" : "BookWith This ID Already Exists."}),  400
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

if __name__ == "__main__":
    app.run(debug = True)




