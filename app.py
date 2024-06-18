
from flask import Flask, jsonify, request, abort
import psycopg2
import configparser

app = Flask(__name__)

# Load database configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

DB_HOST = config['database']['host']
DB_NAME = config['database']['dbname']
DB_USER = config['database']['user']
DB_PASS = config['database']['password']

# Connect to the database
def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    return conn

class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'price': self.price}

    @classmethod
    def from_row(cls, row):
        return cls(id=row[0], name=row[1], price=row[2])

# Route to retrieve the list of products
@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT product_ID, product_Name, price FROM product")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    products = [Product.from_row(row).to_dict() for row in rows]
    return jsonify({'products': products})

# Route to delete a product by id
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT product_ID FROM product WHERE product_ID = %s", (product_id,))
    product = cursor.fetchone()

    if product is None:
        cursor.close()
        conn.close()
        abort(404)

    cursor.execute("DELETE FROM product WHERE product_ID = %s", (product_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'result': True})

# Route to update the price of a product by id
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product_price(product_id):
    if not request.json or 'price' not in request.json:
        abort(400)
    new_price = request.json['price']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT product_ID FROM product WHERE product_ID = %s", (product_id,))
    product = cursor.fetchone()

    if product is None:
        cursor.close()
        conn.close()
        abort(404)

    cursor.execute("UPDATE product SET price = %s WHERE product_ID = %s", (new_price, product_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'result': True})

# Error handler for 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
