import sqlite3
import json
import random
from faker import Faker
from datetime import datetime, timedelta

DB_FILE = "ecommerce.db"

# Initialize Faker for generating mock data
fake = Faker('en_GB')  # Using Great Britain locale for addresses

# --- Core Data Definitions ---

# Product categories based on the PDF list
CATEGORIES = {
    'Headphones & Audio': 'Audio devices for personal and home listening.',
    'Cameras': 'Digital cameras and accessories for photography and videography.',
    'Smartphones & Laptops': 'Mobile phones and portable computers.',
    'Gaming & Drones': 'Consoles, games, and unmanned aerial vehicles.',
}

# Products that have a corresponding PDF manual from your list
# This creates the crucial semantic link for the RAG task.
PDF_LINKED_PRODUCTS = [
    ('Sony WH-1000XM5 Wireless Headphones', 'Headphones & Audio', 349.99,
     {'color': 'Black', 'type': 'Over-ear', 'connectivity': 'Bluetooth 5.2'}),
    ('Bose QuietComfort Ultra Headphones', 'Headphones & Audio', 449.95, {
     'color': 'Black', 'type': 'Over-ear', 'feature': 'Immersive Audio'}),
    ('JBL Charge 5 Speaker', 'Headphones & Audio', 159.99, {
     'color': 'Blue', 'type': 'Portable Speaker', 'waterproof': 'IP67'}),
    ('Sony Alpha a7 IV', 'Cameras', 2399.00, {
     'sensor': '33MP Full-Frame', 'type': 'Mirrorless', 'video': '4K 60p'}),
    ('Samsung Galaxy S24 Ultra', 'Smartphones & Laptops', 1249.00, {
     'storage': '256GB', 'color': 'Titanium Gray', 'feature': 'S Pen'}),
    ('Dell XPS 15 Laptop', 'Smartphones & Laptops', 1899.00, {
     'cpu': 'Intel Core i7', 'ram': '16GB', 'storage': '512GB SSD'}),
    ('Sony PlayStation 5', 'Gaming & Drones', 479.99, {
     'type': 'Disc Edition', 'storage': '825GB SSD'}),
    ('DJI Mini 4 Pro Drone', 'Gaming & Drones', 999.00, {
     'weight': '249g', 'video': '4K/60fps HDR', 'feature': 'Obstacle Sensing'}),
]


def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Makes it easier to work with results
    return conn


def populate_data():
    """Main function to populate all tables."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1. Populate Categories
        category_map = {}
        for name, desc in CATEGORIES.items():
            cursor.execute(
                "INSERT INTO product_categories (category_name, description) VALUES (?, ?)", (name, desc))
            category_map[name] = cursor.lastrowid
        print(f"Populated {len(category_map)} product categories.")

        # 2. Populate Products
        product_map = {}
        # Insert PDF-linked products
        for name, cat, price, specs in PDF_LINKED_PRODUCTS:
            cat_id = category_map[cat]
            specs_json = json.dumps(specs)
            release = fake.date_between(start_date='-3y', end_date='today')
            stock = random.randint(10, 200)
            cursor.execute(
                "INSERT INTO products (product_name, category_id, price, stock_quantity, specs, release_date) VALUES (?, ?, ?, ?, ?, ?)",
                (name, cat_id, price, stock, specs_json, release)
            )
            product_map[cursor.lastrowid] = price
        print(f"Populated {len(product_map)} PDF-linked products.")

        # 3. Populate Customers
        customers = []
        for _ in range(50):  # Create 50 mock customers
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1,99)}@{fake.free_email_domain()}"
            customers.append((
                first_name,
                last_name,
                email,
                fake.phone_number(),
                fake.date_between(start_date='-5y', end_date='today'),
                fake.address().replace('\n', ', ')
            ))
        cursor.executemany(
            "INSERT INTO customers (first_name, last_name, email, phone_number, join_date, address) VALUES (?, ?, ?, ?, ?, ?)",
            customers
        )
        print(f"Populated {len(customers)} customers.")
        customer_ids = [row[0] for row in cursor.execute(
            "SELECT customer_id FROM customers").fetchall()]

        # 4. Populate Orders and Order Items
        order_count = 0
        item_count = 0
        for _ in range(150):  # Create 150 orders
            customer_id = random.choice(customer_ids)
            order_date = fake.date_time_between(
                start_date='-2y', end_date='now')
            order_status = random.choice(
                ['Shipped', 'Processing', 'Delivered', 'Cancelled'])

            # Create order items first to calculate total
            num_items = random.randint(1, 4)
            order_items_data = []
            total_amount = 0

            # Ensure unique products per order
            products_in_order = random.sample(
                list(product_map.keys()), num_items)

            for product_id in products_in_order:
                quantity = random.randint(1, 3)
                price = product_map[product_id]
                order_items_data.append((product_id, quantity, price))
                total_amount += quantity * price
                item_count += 1

            # Insert the master order record
            cursor.execute(
                "INSERT INTO orders (customer_id, order_date, status, total_amount) VALUES (?, ?, ?, ?)",
                (customer_id, order_date, order_status, round(total_amount, 2))
            )
            order_id = cursor.lastrowid
            order_count += 1

            # Insert the associated order items
            for product_id, quantity, price in order_items_data:
                cursor.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES (?, ?, ?, ?)",
                    (order_id, product_id, quantity, price)
                )

        print(
            f"Populated {order_count} orders with a total of {item_count} items.")

        conn.commit()
        print("Mock data populated successfully.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()  # Roll back changes on error
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    populate_data()
