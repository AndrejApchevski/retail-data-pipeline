import requests
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime

# Database connection config
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "retail_data_pipeline",
    "user": "postgres",
    "password": "admin"
}

# API endpoints
API_BASE = "https://fakestoreapi.com"
ENDPOINTS = {
    "products": "/products",
    "users": "/users",
    "carts": "/carts"
}

# Connect to PostgreSQL
def connect_db():
    return psycopg2.connect(**DB_CONFIG)

# Fetch from API
def fetch_data(endpoint):
    url = API_BASE + ENDPOINTS[endpoint]
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Insert products
def insert_products(cur, products):
    values = [
        (
            p['id'], p['title'], p['price'], p['description'],
            p['category'], p['image'], p['rating']['rate'], p['rating']['count']
        )
        for p in products
    ]
    execute_values(cur, """
        INSERT INTO products (
            id, title, price, description, category, image, rating_rate, rating_count
        ) VALUES %s
        ON CONFLICT DO NOTHING;
    """, values)

# Insert users
def insert_users(cur, users):
    values = [
        (
            u['id'], u['email'], u['username'], u['password'],
            u['name']['firstname'], u['name']['lastname'],
            u['address']['street'], u['address']['number'],
            u['address']['city'], u['address']['zipcode'],
            u['address']['geolocation']['lat'], u['address']['geolocation']['long'],
            u['phone']
        )
        for u in users
    ]
    execute_values(cur, """
        INSERT INTO users (
            id, email, username, password, firstname, lastname,
            street, street_number, city, zipcode, lat, long, phone
        ) VALUES %s
        ON CONFLICT DO NOTHING;
    """, values)

# Insert carts and cart_items
def insert_carts_and_items(cur, carts):
    for cart in carts:
        cart_id = cart['id']
        user_id = cart['userId']
        date = datetime.fromisoformat(cart['date'].replace("Z", "+00:00"))

        # Insert into carts
        cur.execute("""
            INSERT INTO carts (id, user_id, date)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, (cart_id, user_id, date))

        # Insert into cart_items
        for item in cart['products']:
            cur.execute("""
                INSERT INTO cart_items (cart_id, product_id, quantity)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING;
            """, (cart_id, item['productId'], item['quantity']))

# Main run
def main():
    print("📦 Starting data ingestion...")

    conn = connect_db()
    cur = conn.cursor()

    # Fetch and insert products
    products = fetch_data("products")
    insert_products(cur, products)
    print(f"✅ Inserted {len(products)} products")

    # Fetch and insert users
    users = fetch_data("users")
    insert_users(cur, users)
    print(f"✅ Inserted {len(users)} users")

    # Fetch and insert carts
    carts = fetch_data("carts")
    insert_carts_and_items(cur, carts)
    print(f"✅ Inserted {len(carts)} carts and items")

    conn.commit()
    cur.close()
    conn.close()
    print("🎉 Data ingestion complete.")

if __name__ == "__main__":
    main()
