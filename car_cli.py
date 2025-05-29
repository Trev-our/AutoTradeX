import sqlite3
import argparse
from typing import List, Dict

# Initialize SQLite DB
def init_db():
    conn = sqlite3.connect("cars.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            make TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER,
            price REAL
        )
    """)
    conn.commit()
    conn.close()

# Add a new car
def add_car(make: str, model: str, year: int, price: float):
    conn = sqlite3.connect("cars.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cars (make, model, year, price) VALUES (?, ?, ?, ?)", 
                   (make, model, year, price))
    conn.commit()
    conn.close()
    print(f"✅ Added {make} {model} (${price})")

# List all cars
def list_cars():
    conn = sqlite3.connect("cars.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars")
    cars = cursor.fetchall()
    conn.close()

    if not cars:
        print("🚗 No cars found. Add some first!")
        return

    print("\n📋 Car Inventory:")
    for car in cars:
        print(f"ID: {car[0]} | {car[1]} {car[2]} ({car[3]}) - ${car[4]}")

# Search cars by make/model
def search_cars(query: str):
    conn = sqlite3.connect("cars.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars WHERE make LIKE ? OR model LIKE ?", 
                   (f"%{query}%", f"%{query}%"))
    cars = cursor.fetchall()
    conn.close()

    if not cars:
        print(f"🔍 No cars matching '{query}'")
        return

    print(f"\n🔎 Search Results for '{query}':")
    for car in cars:
        print(f"ID: {car[0]} | {car[1]} {car[2]}")

# Delete a car by ID
def delete_car(car_id: int):
    conn = sqlite3.connect("cars.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cars WHERE id = ?", (car_id,))
    conn.commit()
    conn.close()
    print(f"🗑️ Deleted car ID {car_id}")

# CLI Argument Parser
def main():
    init_db()
    parser = argparse.ArgumentParser(description="🚗 Car Management CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Add Car
    add_parser = subparsers.add_parser("add", help="Add a new car")
    add_parser.add_argument("--make", required=True, help="Car make (e.g., Toyota)")

    add_parser.add_argument("--model", required=True, help="Car model (e.g., Camry)")

    add_parser.add_argument("--year", type=int, help="Manufacturing year")
    add_parser.add_argument("--price", type=float, required=True, help="Price ($)")

    # List Cars
    subparsers.add_parser("list", help="List all cars")

    # Search Cars
    search_parser = subparsers.add_parser("search", help="Search cars by make/model")
    search_parser.add_argument("query", help="Search term (e.g., 'Toyota')")

    # Delete Car
    delete_parser = subparsers.add_parser("delete", help="Delete a car by ID")
    delete_parser.add_argument("car_id", type=int, help="ID of the car to delete")

    args = parser.parse_args()

    if args.command == "add":
        add_car(args.make, args.model, args.year, args.price)
    elif args.command == "list":
        list_cars()
    elif args.command == "search":
        search_cars(args.query)
    elif args.command == "delete":
        delete_car(args.car_id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()