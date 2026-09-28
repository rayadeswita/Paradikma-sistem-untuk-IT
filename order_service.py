from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

orders = []

BOOK_SERVICE_URL = "http://127.0.0.1:5001"

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    book_id = data.get('book_id')

    try:
        response = requests.get(
            f"{BOOK_SERVICE_URL}/books/{book_id}"
        )

        if response.status_code != 200:
            return jsonify({
                "error": "Buku tidak ditemukan"
            }), 400

        book = response.json()

        if book["stock"] <= 0:
            return jsonify({
                "error": "Stok buku habis"
            }), 400

        order = {
            "id": len(orders) + 1,
            "book_id": book_id,
            "status": "berhasil"
        }

        orders.append(order)

        return jsonify(order), 201

    except requests.exceptions.ConnectionError:
        return jsonify({
            "error": "Book Service sedang down!"
        }), 503

if __name__ == '__main__':
    app.run(port=5002, debug=True)