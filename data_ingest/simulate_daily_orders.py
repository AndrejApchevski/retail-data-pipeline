import psycopg2
import random
from datetime import datetime, timedelta
import argparse

# Database config (update with your real credentials)
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "retail_data_pipeline",
    "user": "postgres",
    "password": "admin"
}

# Connect to PostgreSQL
def connect_db():
    return psycopg2.connect(**DB_CONFIG)

# Fetch user and product IDs
def fetch_ids(cur):
    cur.execute("SELECT id FROM users;")
    users = [r[0] for r in cur.fetchall()]
    
    cur.execute("SELECT id FROM products;")
    products = [r[0] for r in cur.fetchall()]
    
    return users, products

# Generate a random timestamp within business hours
def generate_order_time(order_date):
    start = datetime.combine(order_date, datetime.min.time()) + timedelta(hours=9)
    end = datetime.combine(order_date, datetime.min.time()) + timedelta(hours=20)
    delta = end - start
    random_minutes = random.randint(0, int(delta.total_seconds() / 60))
    return start + timedelta(minutes=random_minutes)

# Generate and insert orders
def generate_orders(target_date, conn):
    cur = conn.cursor()
    
    users, products = fetch_ids(cur)

    # Weight popular users and products
    user_weights = users + random.choices(users, k=10)  # Loyal users show up more
    product_weights = products + random.choices(products, k=30)  # Some products sell more

    order_count = random.randint(20, 100)
    cart_id_start = get_next_cart_id(cur)
    new_cart_id = cart_id_start

    total_items = 0

    for _ in range(order_count):
        user_id = random.choice(user_weights)
        order_time = generate_order_time(target_date)

        # Insert cart
        cur.execute("""
            INSERT INTO carts (id, user_id, date)
            VALUES (%s, %s, %s)
        """, (new_cart_id, user_id, order_time))

        # Choose products for this cart
        num_products = random.randint(1, 5)
        chosen_products = random.choices(product_weights, k=num_products)
        added = set()

        for product_id in chosen_products:
            if product_id in added:
                continue  # avoid duplicates
            quantity = random.randint(1, 3)
            cur.execute("""
                INSERT INTO cart_items (cart_id, product_id, quantity)
                VALUES (%s, %s, %s)
            """, (new_cart_id, product_id, quantity))
            added.add(product_id)
            total_items += 1

        new_cart_id += 1

    conn.commit()
    cur.close()
    
    print(f"✅ Created {order_count} new carts with {total_items} total items for {target_date}")

# Get next available cart ID
def get_next_cart_id(cur):
    cur.execute("SELECT MAX(id) FROM carts;")
    result = cur.fetchone()[0]
    return (result or 0) + 1

# Argument parsing
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="Target date in YYYY-MM-DD format", default=None)
    return parser.parse_args()

# Main
if __name__ == "__main__":
    args = parse_args()

    # Parse date or use today
    if args.date:
        target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
    else:
        target_date = datetime.now().date()

    print(f"📦 Simulating retail orders for: {target_date}")

    conn = connect_db()
    generate_orders(target_date, conn)
    conn.close()
