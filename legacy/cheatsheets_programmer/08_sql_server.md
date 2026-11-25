# Если на площадке MS SQL Server (а не SQLite)

КИМ говорит «в выбранной СУБД», но в примерах 2027 года используется
**MS SQL Server / LocalDB**. Уточни у куратора. Если SQL Server — вот отличия.

## Подключение из Python

```python
import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=(LocalDB)\\MSSQLLocalDB;"
    "DATABASE=ChudoObuv;"
    "Trusted_Connection=yes;")
cur = conn.cursor()
cur.execute("SELECT product_id, name FROM products")
for row in cur.fetchall():
    print(row)
```

Или строка подключения к файлу `.mdf`:

```
SERVER=(LocalDB)\MSSQLLocalDB;
AttachDbFilename=C:\project\Chudo_Obuv.mdf;
Integrated Security=True;
```

## Отличия синтаксиса

| SQLite | MS SQL Server |
|---|---|
| `INTEGER PRIMARY KEY` | `INT PRIMARY KEY IDENTITY(1,1)` |
| `TEXT` | `NVARCHAR(255)` / `NVARCHAR(MAX)` |
| `REAL` | `DECIMAL(10,2)` / `FLOAT` |
| `AUTOINCREMENT` | `IDENTITY(1,1)` |
| `LIMIT 10` | `SELECT TOP 10 ...` |
| `date('now')` | `CAST(GETDATE() AS date)` / `SYSDATETIME()` |
| `date('now','start of month','-1 month')` | `DATEADD(month, -1, DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1))` |
| `COALESCE(x, y)` | `COALESCE(x, y)` или `ISNULL(x, y)` |
| `a || b` | `a + b` |
| `cursor.lastrowid` | `SELECT SCOPE_IDENTITY()` |
| `PRAGMA foreign_keys=ON` | всегда включено (ограничения в схеме) |
| `INSERT OR IGNORE` | `IF NOT EXISTS (...) INSERT ...` / `MERGE` |

## Схема (фрагмент)

```sql
CREATE TABLE product_items (
    item_id    INT IDENTITY(1,1) PRIMARY KEY,
    product_id INT NOT NULL,
    size_id    INT NOT NULL,
    quantity   INT NOT NULL DEFAULT 0
        CONSTRAINT ck_items_qty CHECK (quantity >= 0),
    CONSTRAINT uq_item UNIQUE (product_id, size_id),
    CONSTRAINT fk_item_product FOREIGN KEY (product_id)
        REFERENCES products(product_id) ON DELETE CASCADE,
    CONSTRAINT fk_item_size FOREIGN KEY (size_id)
        REFERENCES sizes(size_id) ON DELETE NO ACTION
);

CREATE TABLE order_items (
    order_item_id INT IDENTITY(1,1) PRIMARY KEY,
    order_id      INT NOT NULL,
    item_id       INT NOT NULL,
    quantity      INT NOT NULL CONSTRAINT ck_oi_qty CHECK (quantity > 0),
    unit_price    DECIMAL(10,2) NOT NULL
        CONSTRAINT ck_oi_price CHECK (unit_price >= 0),
    CONSTRAINT fk_oi_order FOREIGN KEY (order_id)
        REFERENCES orders(order_id) ON DELETE CASCADE,
    CONSTRAINT fk_oi_item FOREIGN KEY (item_id)
        REFERENCES product_items(item_id) ON DELETE NO ACTION
);
```

## Скидка 25% в T-SQL

```sql
SELECT p.product_id, p.name,
       ROUND(p.price * CASE WHEN NOT EXISTS (
           SELECT 1
           FROM orders o
           JOIN order_items oi ON oi.order_id = o.order_id
           JOIN product_items pi ON pi.item_id = oi.item_id
           WHERE pi.product_id = p.product_id
             AND o.order_date >= DATEADD(month, -1,
                    DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1))
             AND o.order_date <  DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1)
       ) THEN 0.75 ELSE 1 END, 2) AS final_price
FROM products p;
```

## Статистика в T-SQL

```sql
SELECT COUNT(*) AS orders_count,
       ISNULL(SUM(total), 0) AS revenue,
       CASE WHEN COUNT(*) = 0 THEN 0
            ELSE ROUND(SUM(total) / COUNT(*), 2) END AS avg_check
FROM (
    SELECT o.order_id, SUM(oi.quantity * oi.unit_price) AS total
    FROM orders o
    LEFT JOIN order_items oi ON oi.order_id = o.order_id
    GROUP BY o.order_id
) t;
```

## Что сделать в SSMS/Visual Studio

1. Создать базу `Чудо_Обувь` (LocalDB).
2. Выполнить `schema.sql` (в SSMS: открыть файл → Execute).
3. ER-диаграмма: SSMS → «Диаграммы баз данных» → создать → PDF.
4. Скрипт БД: ПКМ по базе → «Задачи» → «Создать скрипты» → «Данные и схема».
5. Импорт: «Изменить все строки» + вставка из Excel или `pyodbc`/`bcp`.
6. Приложение: Python (`pyodbc`) или C# WinForms (`SqlConnection`).
