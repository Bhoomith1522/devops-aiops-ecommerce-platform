from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from prometheus_flask_exporter import PrometheusMetrics

import psycopg2
import time
import os
import logging
import requests

# -----------------------------------
# LOAD ENV VARIABLES
# -----------------------------------

load_dotenv()

# -----------------------------------
# APP CONFIG
# -----------------------------------

app = Flask(__name__)

CORS(app)

# -----------------------------------
# PROMETHEUS METRICS
# -----------------------------------

metrics = PrometheusMetrics(app)

# -----------------------------------
# LOGGING CONFIG
# -----------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------

def get_db_connection():

    while True:

        try:

            conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "db"),
                database=os.getenv("DB_NAME", "ecommerce"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "postgres")
            )

            logging.info("Database connected successfully!")

            return conn

        except Exception as e:

            logging.error(f"Database connection failed: {e}")

            logging.info("Retrying in 5 seconds...")

            time.sleep(5)

# -----------------------------------
# INITIALIZE DATABASE
# -----------------------------------

def initialize_database():

    conn = get_db_connection()

    cur = conn.cursor()

    # Create products table
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

    # Insert default products only once
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

# Initialize DB
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
# HEALTH CHECK
# -----------------------------------

@app.route("/health")
def health_check():

    return jsonify({
        "status": "healthy"
    })

# -----------------------------------
# GET PRODUCTS
# -----------------------------------

@app.route("/products", methods=["GET"])
def get_products():

    try:

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

    except Exception as e:

        logging.error(f"Error fetching products: {e}")

        return jsonify({
            "error": str(e)
        }), 500

# -----------------------------------
# ADD PRODUCT
# -----------------------------------

@app.route("/products", methods=["POST"])
def add_product():

    try:

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

        logging.info(f"Product added: {name}")

        return jsonify({
            "message": "Product added successfully!"
        }), 201

    except Exception as e:

        logging.error(f"Error adding product: {e}")

        return jsonify({
            "error": str(e)
        }), 500

# -----------------------------------
# UPDATE PRODUCT
# -----------------------------------

@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):

    try:

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

        logging.info(f"Product updated: {id}")

        return jsonify({
            "message": "Product updated successfully!"
        })

    except Exception as e:

        logging.error(f"Error updating product: {e}")

        return jsonify({
            "error": str(e)
        }), 500

# -----------------------------------
# DELETE PRODUCT
# -----------------------------------

@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):

    try:

        conn = get_db_connection()

        cur = conn.cursor()

        cur.execute(
            "DELETE FROM products WHERE id = %s",
            (id,)
        )

        conn.commit()

        cur.close()
        conn.close()

        logging.info(f"Product deleted: {id}")

        return jsonify({
            "message": "Product deleted successfully!"
        })

    except Exception as e:

        logging.error(f"Error deleting product: {e}")

        return jsonify({
            "error": str(e)
        }), 500

# -----------------------------------
# AIOPS LOG ANALYZER (OLLAMA)
# -----------------------------------

@app.route("/analyze-log", methods=["POST"])
def analyze_log():

    try:

        data = request.get_json()

        log_message = data.get("log")

        if not log_message:

            return jsonify({
                "error": "Log message is required"
            }), 400

        prompt = f"""
        Analyze this DevOps system log.

        Explain:
        1. Possible issue
        2. Root cause
        3. Suggested fix

        Log:
        {log_message}
        """

        response = requests.post(
            "http://host.docker.internal:11434/api/generate",
            json={
                "model": "gemma:2b",
                "prompt": prompt,
                "stream": False
            }
        )

        result = response.json()["response"]

        logging.info("AI log analysis completed successfully")

        return jsonify({
            "analysis": result
        })

    except Exception as e:

        logging.error(f"AIOps analysis error: {e}")

        return jsonify({
            "error": str(e)
        }), 500

# -----------------------------------
# MAIN
# -----------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )