# SQL для ДЭ-2027 «Чудо Обувь» (8 таблиц)

> Все примеры проверяются в тренажёре на вкладке «SQL-практика» — там реальная SQLite-база.

## Таблицы

```
roles (role_id, role_name)
categories (category_id, category_name)
sizes (size_id, size_value)
users (user_id, last_name, first_name, middle_name, login, role_id)
products (product_id, category_id, subcategory, name, manufacturer,
          description, composition, image_path, price)
product_items (item_id, product_id, size_id, quantity)
orders (order_id, order_date, user_id)
order_items (order_item_id, order_id, item_id, quantity, unit_price)
```

`product_items` — это товарная позиция: **модель + размер**. В `order_items`
хранится количество и **цена за единицу на момент заказа**.

## Порядок предложений

```sql
SELECT ... FROM ... JOIN ... ON ... WHERE ... GROUP BY ... HAVING ...
ORDER BY ... ASC|DESC LIMIT ...;
```

## Каталог и остаток

```sql
-- каталог с категорией
SELECT p.product_id, p.name, c.category_name, p.manufacturer,
       p.composition, p.price
FROM products p
JOIN categories c ON p.category_id = c.category_id;

-- суммарный остаток по модели + «много/мало»
SELECT p.product_id, p.name,
       COALESCE(SUM(pi.quantity), 0) AS total_qty,
       CASE WHEN COALESCE(SUM(pi.quantity), 0) > 5
            THEN 'много' ELSE 'мало' END AS stock_label
FROM products p
LEFT JOIN product_items pi ON pi.product_id = p.product_id
GROUP BY p.product_id, p.name;

-- подсветка: остаток ≤ 3
SELECT p.product_id, p.name
FROM products p
LEFT JOIN product_items pi ON pi.product_id = p.product_id
GROUP BY p.product_id, p.name
HAVING COALESCE(SUM(pi.quantity), 0) <= 3;
```

## Скидка 25% (главная «ловушка»)

Скидка даётся товарам, по которым **не было заказов в прошлом календарном
месяце**:

```sql
SELECT p.product_id, p.name,
       ROUND(p.price * CASE WHEN NOT EXISTS (
           SELECT 1
           FROM orders o
           JOIN order_items oi ON oi.order_id = o.order_id
           JOIN product_items pi ON pi.item_id = oi.item_id
           WHERE pi.product_id = p.product_id
             AND o.order_date >= date('now','start of month','-1 month')
             AND o.order_date <  date('now','start of month')
       ) THEN 0.75 ELSE 1 END, 2) AS final_price
FROM products p;
```

Границы месяца — именно `start of month` и `-1 month`, а не «30 дней назад».

## Заказы и состав

```sql
-- список заказов: дата + ФИО клиента
SELECT o.order_id, o.order_date,
       u.last_name || ' ' || u.first_name || ' ' || COALESCE(u.middle_name, '') AS client
FROM orders o
JOIN users u ON u.user_id = o.user_id;

-- состав заказа
SELECT p.name, p.manufacturer, s.size_value, oi.quantity, oi.unit_price,
       ROUND(oi.quantity * oi.unit_price, 2) AS line_total
FROM order_items oi
JOIN product_items pi ON pi.item_id = oi.item_id
JOIN products p ON p.product_id = pi.product_id
JOIN sizes s ON s.size_id = pi.size_id
WHERE oi.order_id = 1;

-- итог заказа
SELECT o.order_id,
       ROUND(COALESCE(SUM(oi.quantity * oi.unit_price), 0), 2) AS total
FROM orders o
LEFT JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY o.order_id;
```

`LEFT JOIN` нужен, чтобы заказ без позиций не исчез из списка.

## Статистика (Задание 5)

```sql
SELECT COUNT(*) AS orders_count,
       COALESCE(SUM(total), 0) AS revenue,
       ROUND(COALESCE(SUM(total), 0) / COUNT(*), 2) AS avg_check
FROM (
    SELECT o.order_id, SUM(oi.quantity * oi.unit_price) AS total
    FROM orders o
    LEFT JOIN order_items oi ON oi.order_id = o.order_id
    GROUP BY o.order_id
);
```

## Поиск, фильтр, сортировка (Задание 3)

```sql
WHERE (p.name LIKE ? OR p.description LIKE ?)
  AND c.category_name = ?          -- если выбрана не «Все категории»
ORDER BY p.price ASC               -- или DESC
```

**Ловушка:** `lower()` в SQLite не понижает регистр кириллицы.
Для поиска без учёта регистра используй Python: `"кросс" in text.lower()`.

## DDL и изменения

```sql
CREATE TABLE product_items (
    item_id    INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
    size_id    INTEGER NOT NULL REFERENCES sizes(size_id) ON DELETE RESTRICT,
    quantity   INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    UNIQUE (product_id, size_id)
);

INSERT INTO users (last_name, first_name, middle_name, login, role_id)
VALUES ('Новиков', 'Олег', 'Игоревич', 'onovikov', 3);

UPDATE orders SET order_date = '2026-05-15' WHERE order_id = 1;

DELETE FROM order_items WHERE order_item_id = 2;
```

* `PRAGMA foreign_keys = ON` — в SQLite по умолчанию **выключено**;
* после `INSERT/UPDATE/DELETE` — `commit()`;
* скрипт БД сдаётся **с данными** (DDL + INSERT).

## Частые ошибки

| Симптом | Причина |
|---|---|
| `no such column` | Опечатка или забыт JOIN |
| Цена без копеек | `/ 100` вместо `/ 100.0` |
| Скидка не у всех / у всех | Неверные границы прошлого месяца или `EXISTS` вместо `NOT EXISTS` |
| Заказ без позиций исчез | `JOIN` вместо `LEFT JOIN` |
| Кириллица не ищется | `lower()` не работает с кириллицей |
| Удалили товар из заказа | Нет проверки/`RESTRICT` |
