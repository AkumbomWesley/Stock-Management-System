from flask import Flask, jsonify, request
import psycopg2
import config

app = Flask(__name__)


# Function to open database connection
def open_db_connection():
    conn = psycopg2.connect(
        host=config.DB_HOST,
        database=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD
    )
    return conn


# Function to close database connection
def close_db_connection(conn):
    conn.close()


# API endpoint to get all stocks
@app.route("/stocks", methods=["GET"])
def get_stocks():
    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM stocks")
    rows = cur.fetchall()
    close_db_connection(conn)
    return jsonify(rows)


# API endpoint to get a specific stock by id
@app.route("/stocks/<int:val>", methods=["GET"])
def get_stock(val):
    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM stocks WHERE val = %s", (val,))
    row = cur.fetchone()
    close_db_connection(conn)
    if row is None:
        return jsonify({"error": "Stock not found"}), 404
    else:
        return jsonify(row)


# API endpoint to add a new stock
@app.route("/stocks", methods=["POST"])
def add_stock():
    data = request.get_json()
    name = data["name"]
    price = data["price"]
    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO stocks (name, price) VALUES (%s, %s)", (name, price))
    conn.commit()
    close_db_connection(conn)
    return jsonify({"message": "Stock added successfully"})


# API endpoint to update an existing stock by id
@app.route("/stocks/<int:val>", methods=["PUT"])
def update_stock(val):
    data = request.get_json()
    name = data["name"]
    price = data["price"]
    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE stocks SET name = %s, price = %s WHERE val = %s", (name, price, val))
    conn.commit()
    close_db_connection(conn)
    return jsonify({"message": "Stock updated successfully"})


# API endpoint to delete an existing stock by id
@app.route("/stocks/<int:val>", methods=["DELETE"])
def delete_stock(val):
    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM stocks WHERE val = %s", (val,))
    conn.commit()
    close_db_connection(conn)
    return jsonify({"message": "Stock deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)
