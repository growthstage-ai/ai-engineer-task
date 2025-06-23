import sqlite3
import os

DB_FILE = "ecommerce.db"


def create_database():
    """
    Creates an SQLite database with the specified e-commerce schema.
    Deletes the old database file if it exists.
    """
    # Delete the old database file if it exists to start fresh
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Removed old database file: {DB_FILE}")

    try:
        # Connect to the SQLite database (this will create the file)
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        print(f"Successfully connected to {DB_FILE}")

        # --- Create Tables ---

        # Customer Table
        cursor.execute("""
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone_number VARCHAR(20),
            join_date DATE NOT NULL,
            address VARCHAR(255) NOT NULL
        );
        """)
        print("Created 'customers' table.")

        # Product Categories Table
        cursor.execute("""
        CREATE TABLE product_categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name VARCHAR(50) UNIQUE NOT NULL,
            description TEXT
        );
        """)
        print("Created 'product_categories' table.")

        # Products Table
        cursor.execute("""
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name VARCHAR(100) NOT NULL,
            category_id INTEGER NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            stock_quantity INTEGER NOT NULL,
            specs TEXT, -- Storing as JSON string
            release_date DATE,
            FOREIGN KEY (category_id) REFERENCES product_categories (category_id)
        );
        """)
        print("Created 'products' table.")

        # Orders Table
        cursor.execute("""
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            order_date TIMESTAMP NOT NULL,
            status VARCHAR(20) NOT NULL,
            total_amount DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        );
        """)
        print("Created 'orders' table.")

        # Order Items Table
        cursor.execute("""
        CREATE TABLE order_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price_at_purchase DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (order_id),
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        );
        """)
        print("Created 'order_items' table.")

        # Commit the changes and close the connection
        conn.commit()
        print("Database schema created successfully.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    create_database()
