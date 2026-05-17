from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import time

app = Flask(__name__)

# Enable CORS
CORS(app)

# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------

def get_db_connection():

    while True:

        try:

            conn = psycopg2.connect(
                host="db",
                database="ecommerce",
                user="postgres",
                password="postgres"
            )

            print("Database connected successfully!")

            return conn

        except Exception as e:

            print("Database connection failed:")
            print(e)

            print("Retrying in 5 seconds...")

            time.sleep(5)

# -----------------------------------
# INITIALIZE DATABASE
# -----------------------------------

def initialize_database():

    conn = get_db_connection()

    cur = conn.cursor()

    # Create table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            price INTEGER
        );
    """)

    # Check existing products
    cur.execute("SELECT COUNT(*) FROM products;")

    count = cur.fetchone()[0]

    # Insert default data only once
    if count == 0:

        cur.execute("""
            INSERT INTO products (name, price)
            VALUES
            ('Laptop', 50000),
            ('Phone', 20000),
            ('Headphones', 3000);
        """)

    conn.commit()

    cur.close()
    conn.close()

# Initialize DB at startup
initialize_database()

# -----------------------------------
# HOME ROUTE
# -----------------------------------

@app.route("/")
def home():

    return jsonify({
        "message": "DevOps + AIOps Backend Running Successfully!"
    })

# -----------------------------------
# GET PRODUCTS
# -----------------------------------

@app.route("/products", methods=["GET"])
def get_products():

    conn = get_db_connection()

    cur = conn.cursor()

    cur.execute("SELECT * FROM products;")

    rows = cur.fetchall()

    products = []

    for row in rows:

        products.append({
            "id": row[0],
            "name": row[1],
            "price": row[2]
        })

    cur.close()
    conn.close()

    return jsonify(products)

# -----------------------------------
# ADD PRODUCT
# -----------------------------------

@app.route("/products", methods=["POST"])
def add_product():

    data = request.get_json()

    name = data["name"]
    price = data["price"]

    conn = get_db_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO products (name, price)
        VALUES (%s, %s)
        """,
        (name, price)
    )

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({
        "message": "Product added successfully!"
    }), 201

# -----------------------------------
# UPDATE PRODUCT
# -----------------------------------

@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):

    data = request.get_json()

    name = data["name"]
    price = data["price"]

    conn = get_db_connection()

    cur = conn.cursor()

    cur.execute(
        """
        UPDATE products
        SET name = %s, price = %s
        WHERE id = %s
        """,
        (name, price, id)
    )

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({
        "message": "Product updated successfully!"
    })

# -----------------------------------
# DELETE PRODUCT
# -----------------------------------

@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):

    conn = get_db_connection()

    cur = conn.cursor()

    cur.execute(
        "DELETE FROM products WHERE id = %s",
        (id,)
    )

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({
        "message": "Product deleted successfully!"
    })

# -----------------------------------
# MAIN
# -----------------------------------

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)