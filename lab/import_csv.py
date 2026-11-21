# -*- coding: utf-8 -*-
"""
Задание 1: импорт данных из файлов с пометкой «import».

Порядок важен: справочники → товары → товарные позиции → пользователи → заказы.
Скрипт идемпотентен: повторный запуск не создаёт дубликаты.

Запуск:  python import_csv.py
"""
import csv
import sqlite3
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
DB_PATH = BASE / "chudo_obuv.db"
SCHEMA = BASE / "schema.sql"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def rows(filename):
    with open(DATA / filename, encoding="utf-8", newline="") as f:
        yield from csv.DictReader(f, delimiter=";")


def main():
    if not DB_PATH.exists():
        conn = get_conn()
        conn.executescript(SCHEMA.read_text(encoding="utf-8"))
        conn.commit()
        conn.close()
        print("База создана из schema.sql")

    conn = get_conn()
    try:
        # --- 1. Товары и категории -------------------------------------
        for row in rows("products_import.csv"):
            category = conn.execute(
                "SELECT category_id FROM categories WHERE category_name = ?",
                (row["category_name"],)).fetchone()
            if category is None:
                category = conn.execute(
                    "INSERT INTO categories (category_name) VALUES (?)",
                    (row["category_name"],))
                category_id = category.lastrowid
            else:
                category_id = category["category_id"]
            exists = conn.execute(
                "SELECT 1 FROM products WHERE name = ?", (row["name"],)).fetchone()
            if exists:
                continue          # повторный импорт не создаёт дубликаты
            conn.execute(
                "INSERT INTO products "
                "(category_id, subcategory, name, manufacturer, description, "
                " composition, image_path, price) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (category_id, row["subcategory"], row["name"], row["manufacturer"],
                 row["description"], row["composition"],
                 row["image_path"].strip() or None, float(row["price"])))
        print("Товары импортированы")

        # --- 2. Размеры и остатки --------------------------------------
        for row in rows("stock_import.csv"):
            product = conn.execute(
                "SELECT product_id FROM products WHERE name = ?",
                (row["product_name"],)).fetchone()
            if product is None:
                print("  ! товар не найден:", row["product_name"])
                continue
            size_value = float(row["size"])
            size = conn.execute(
                "SELECT size_id FROM sizes WHERE size_value = ?",
                (size_value,)).fetchone()
            if size is None:
                size = conn.execute(
                    "INSERT INTO sizes (size_value) VALUES (?)", (size_value,))
                size_id = size.lastrowid
            else:
                size_id = size["size_id"]
            conn.execute(
                "INSERT INTO product_items (product_id, size_id, quantity) "
                "VALUES (?, ?, ?) "
                "ON CONFLICT(product_id, size_id) DO UPDATE SET quantity = excluded.quantity",
                (product["product_id"], size_id, int(row["quantity"])))
        print("Остатки импортированы")

        # --- 3. Пользователи и роли ------------------------------------
        for row in rows("users_import.csv"):
            role = conn.execute(
                "SELECT role_id FROM roles WHERE role_name = ?",
                (row["role_name"],)).fetchone()
            if role is None:
                print("  ! роль не найдена:", row["role_name"])
                continue
            conn.execute(
                "INSERT OR IGNORE INTO users "
                "(last_name, first_name, middle_name, login, role_id) "
                "VALUES (?, ?, ?, ?, ?)",
                (row["last_name"], row["first_name"], row["middle_name"],
                 row["login"], role["role_id"]))
        print("Пользователи импортированы")

        # --- 4. Заказы и строки заказов --------------------------------
        order_ids = {}
        for row in rows("orders_import.csv"):
            key = row["order_key"]
            order_date = date.today().isoformat() if row["order_date"] == "today" \
                else row["order_date"]
            user = conn.execute(
                "SELECT user_id FROM users WHERE login = ?",
                (row["login"],)).fetchone()
            product = conn.execute(
                "SELECT product_id FROM products WHERE name = ?",
                (row["product_name"],)).fetchone()
            if user is None or product is None:
                print("  ! пропущена строка заказа:", key)
                continue
            size = conn.execute(
                "SELECT pi.item_id FROM product_items pi "
                "JOIN sizes s ON s.size_id = pi.size_id "
                "WHERE pi.product_id = ? AND s.size_value = ?",
                (product["product_id"], float(row["size"]))).fetchone()
            if size is None:
                print("  ! нет товарной позиции:", row["product_name"], row["size"])
                continue
            if key not in order_ids:
                exists = conn.execute(
                    "SELECT order_id FROM orders WHERE order_date = ? AND user_id = ?",
                    (order_date, user["user_id"])).fetchone()
                order_ids[key] = exists["order_id"] if exists else conn.execute(
                    "INSERT INTO orders (order_date, user_id) VALUES (?, ?)",
                    (order_date, user["user_id"])).lastrowid
            order_id = order_ids[key]
            duplicate = conn.execute(
                "SELECT 1 FROM order_items WHERE order_id = ? AND item_id = ? "
                "AND quantity = ? AND unit_price = ?",
                (order_id, size["item_id"], int(row["quantity"]),
                 float(row["unit_price"]))).fetchone()
            if duplicate:
                continue
            conn.execute(
                "INSERT INTO order_items (order_id, item_id, quantity, unit_price) "
                "VALUES (?, ?, ?, ?)",
                (order_id, size["item_id"], int(row["quantity"]),
                 float(row["unit_price"])))
        print("Заказы импортированы")

        conn.commit()
        counts = {}
        for table in ("products", "product_items", "users", "orders", "order_items"):
            counts[table] = conn.execute(
                f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print("Итог:", counts)
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
