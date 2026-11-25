# Python + SQLite под КИМ-2027

`sqlite3` и `tkinter` уже встроены в Python — ставить ничего не нужно.

## Каркас

```python
import sqlite3
from pathlib import Path

DB = Path(__file__).with_name("chudo_obuv.db")
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
conn.execute("PRAGMA foreign_keys = ON")

# Создать БД из скрипта (он же сдаётся как артефакт)
conn.executescript(Path(__file__).with_name("schema.sql").read_text(encoding="utf-8"))
conn.commit()
```

## Вход только по логину (Задание 3)

```python
user = conn.execute(
    "SELECT u.user_id, u.last_name, u.first_name, u.middle_name, r.role_name "
    "FROM users u JOIN roles r ON u.role_id = r.role_id "
    "WHERE u.login = ?", (login,)).fetchone()
if user is None:
    messagebox.showerror(
        "Ошибка авторизации",
        "Пользователь с таким логином не найден. Выберите логин из списка "
        "или войдите как гость.")
else:
    session.user = user
    show_catalog()
```

Пароль **не нужен** — так в КИМ-2027. Гость — `session.user = None`.

## Каталог: остаток, «много/мало», скидка

```sql
SELECT p.product_id, p.name, c.category_name, p.manufacturer,
       p.composition, p.price, p.image_path,
       COALESCE(SUM(pi.quantity), 0) AS total_qty,
       CASE WHEN COALESCE(SUM(pi.quantity), 0) > 5
            THEN 'много' ELSE 'мало' END AS stock_label,
       CASE WHEN NOT EXISTS (
           SELECT 1 FROM orders o
           JOIN order_items oi ON oi.order_id = o.order_id
           JOIN product_items x ON x.item_id = oi.item_id
           WHERE x.product_id = p.product_id
             AND o.order_date >= date('now','start of month','-1 month')
             AND o.order_date <  date('now','start of month')
       ) THEN 1 ELSE 0 END AS has_discount
FROM products p
JOIN categories c ON p.category_id = c.category_id
LEFT JOIN product_items pi ON pi.product_id = p.product_id
GROUP BY p.product_id, p.name, c.category_name, p.manufacturer,
         p.composition, p.price, p.image_path;
```

`final_price = round(price * 0.75, 2) if has_discount else price`.

## Заказ: транзакция

```python
def create_order(user_id, cart):
    try:
        conn.execute("BEGIN")
        cur = conn.execute(
            "INSERT INTO orders (order_date, user_id) VALUES (date('now'), ?)",
            (user_id,))
        order_id = cur.lastrowid
        for row in cart:
            left = conn.execute(
                "SELECT quantity FROM product_items WHERE item_id = ?",
                (row["item_id"],)).fetchone()["quantity"]
            if row["qty"] > left:
                raise ValueError(
                    f"На складе осталось {left} пар. Уменьшите количество.")
            conn.execute(
                "INSERT INTO order_items (order_id, item_id, quantity, unit_price) "
                "VALUES (?, ?, ?, ?)",
                (order_id, row["item_id"], row["qty"], row["price"]))
            conn.execute(
                "UPDATE product_items SET quantity = quantity - ? WHERE item_id = ?",
                (row["qty"], row["item_id"]))
        conn.commit()
        return order_id
    except Exception:
        conn.rollback()
        raise
```

Проверка остатка **внутри** транзакции — иначе можно уйти в минус.

## Статистика (Задание 5)

```python
stats = conn.execute(
    "SELECT COUNT(*) AS orders_count, "
    "COALESCE(SUM(total), 0) AS revenue, "
    "CASE WHEN COUNT(*) = 0 THEN 0 "
    "     ELSE ROUND(SUM(total) / COUNT(*), 2) END AS avg_check "
    "FROM (SELECT o.order_id, SUM(oi.quantity * oi.unit_price) AS total "
    "      FROM orders o LEFT JOIN order_items oi ON oi.order_id = o.order_id "
    "      GROUP BY o.order_id)").fetchone()
```

## Импорт CSV (Задание 1)

```python
import csv

with open("data/products_import.csv", encoding="utf-8", newline="") as f:
    for row in csv.DictReader(f, delimiter=";"):
        conn.execute(
            "INSERT INTO products (category_id, subcategory, name, manufacturer, "
            "description, composition, image_path, price) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (category_id, row["subcategory"], row["name"], row["manufacturer"],
             row["description"], row["composition"],
             row["image_path"] or None, float(row["price"])))
conn.commit()
```

Порядок: справочники → товары → позиции → пользователи → заказы → строки.

## Частые ошибки

| Ошибка | Лечение |
|---|---|
| `no such table` | БД не создана / не тот путь |
| `FOREIGN KEY constraint failed` | Ссылка на несуществующую строку или удаление используемой |
| Изменения не сохранились | Забыли `commit()` |
| `Incorrect number of bindings` | Число `?` не совпало с кортежем |
| Кириллица не ищется | `lower()` не работает с кириллицей |
| Остаток ушёл в минус | Нет проверки остатка в транзакции |
