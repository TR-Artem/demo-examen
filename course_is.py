# -*- coding: utf-8 -*-
"""
Курс «Специалист по информационным системам» (09.02.07-5-2027).
Основа: КИМ 09.02.07-5-2027, профильный уровень: 6 заданий,
3 ч 30 мин инвариант, 75 + 25 баллов.
"""
from __future__ import annotations

MAX_SCORE = 100
COURSE_ID = "is"
COURSE_TITLE = "Информационные системы (09.02.07-5)"
COURSE_SUBTITLE = "ER, SQL, ИС, API · 6 заданий"
EXAM_TITLE = ("ДЭ 09.02.07-5-2027 «Специалист по информационным "
              "системам» · профильный уровень")

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE roles (
    role_id   INTEGER PRIMARY KEY,
    role_name TEXT NOT NULL UNIQUE
);

CREATE TABLE users (
    user_id        INTEGER PRIMARY KEY,
    login          TEXT NOT NULL UNIQUE,
    password       TEXT NOT NULL,
    full_name      TEXT NOT NULL,
    role_id        INTEGER NOT NULL REFERENCES roles(role_id),
    is_blocked     INTEGER NOT NULL DEFAULT 0 CHECK (is_blocked IN (0, 1)),
    failed_attempts INTEGER NOT NULL DEFAULT 0 CHECK (failed_attempts >= 0)
);

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    inn         TEXT NOT NULL UNIQUE,
    address     TEXT NOT NULL,
    phone       TEXT NOT NULL,
    email       TEXT NOT NULL
);

CREATE TABLE specifications (
    spec_id   INTEGER PRIMARY KEY,
    spec_name TEXT NOT NULL UNIQUE
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name       TEXT NOT NULL UNIQUE,
    spec_id    INTEGER NOT NULL REFERENCES specifications(spec_id),
    unit       TEXT NOT NULL DEFAULT 'шт'
);

CREATE TABLE materials (
    material_id INTEGER PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    unit        TEXT NOT NULL,
    price       REAL NOT NULL CHECK (price >= 0)
);

CREATE TABLE product_materials (
    product_id  INTEGER NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
    material_id INTEGER NOT NULL REFERENCES materials(material_id),
    norm_qty    REAL NOT NULL CHECK (norm_qty > 0),
    PRIMARY KEY (product_id, material_id)
);

CREATE TABLE operations (
    operation_id INTEGER PRIMARY KEY,
    name         TEXT NOT NULL UNIQUE,
    price        REAL NOT NULL CHECK (price >= 0)
);

CREATE TABLE product_operations (
    product_id   INTEGER NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
    operation_id INTEGER NOT NULL REFERENCES operations(operation_id),
    norm_hours   REAL NOT NULL CHECK (norm_hours > 0),
    PRIMARY KEY (product_id, operation_id)
);

CREATE TABLE orders (
    order_id    INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date  TEXT NOT NULL,
    status      TEXT NOT NULL CHECK (status IN ('Новый', 'В работе', 'Выполнен', 'Отменён'))
);

CREATE TABLE order_items (
    order_id   INTEGER NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity   INTEGER NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (order_id, product_id)
);

INSERT INTO roles (role_id, role_name) VALUES (1, 'Администратор'), (2, 'Пользователь');

INSERT INTO users (user_id, login, password, full_name, role_id, is_blocked, failed_attempts) VALUES
    (1, 'admin', 'admin123', 'Иванов Иван Иванович', 1, 0, 0),
    (2, 'user1', 'user123', 'Петров Пётр Петрович', 2, 0, 0),
    (3, 'user2', 'user123', 'Сидорова Анна Сергеевна', 2, 1, 3),
    (4, 'user3', 'user123', 'Павлова Елена Викторовна', 2, 0, 1);

INSERT INTO customers (customer_id, name, inn, address, phone, email) VALUES
    (1, 'ООО «Мебель Плюс»', '7701234567', 'Москва, ул. Ленина, 1', '+7(495)111-11-11', 'info@mebelplus.ru'),
    (2, 'ИП Смирнов', '770234567890', 'СПб, пр. Мира, 2', '+7(812)222-22-22', 'smirnov@mail.ru'),
    (3, 'ООО «Офис-Стиль»', '7703456789', 'Казань, ул. Садовая, 3', '+7(843)333-33-33', 'office@style.ru'),
    (4, 'ООО «Дом»', '7704567890', 'Москва, ул. Новая, 4', '+7(495)444-44-44', 'dom@mail.ru'),
    (5, 'ИП Кузнецова', '770567890123', 'СПб, ул. Речная, 5', '+7(812)555-55-55', 'kuz@mail.ru');

INSERT INTO specifications (spec_id, spec_name) VALUES
    (1, 'Спецификация «Корпусная мебель»'),
    (2, 'Спецификация «Мягкая мебель»'),
    (3, 'Спецификация «Столы и стулья»');

INSERT INTO products (product_id, name, spec_id, unit) VALUES
    (1, 'Стол письменный', 3, 'шт'),
    (2, 'Стул офисный', 3, 'шт'),
    (3, 'Шкаф книжный', 1, 'шт'),
    (4, 'Полка настенная', 1, 'шт'),
    (5, 'Кровать двуспальная', 2, 'шт'),
    (6, 'Тумба прикроватная', 1, 'шт'),
    (7, 'Диван прямой', 2, 'шт'),
    (8, 'Кресло мягкое', 2, 'шт'),
    (9, 'Стол журнальный', 3, 'шт');

INSERT INTO materials (material_id, name, unit, price) VALUES
    (1, 'Доска дубовая', 'м2', 1200),
    (2, 'Металл листовой', 'кг', 450),
    (3, 'Лак мебельный', 'л', 300),
    (4, 'Ткань мебельная', 'м2', 800),
    (5, 'Поролон', 'м2', 500),
    (6, 'Клей столярный', 'кг', 250),
    (7, 'Фурнитура', 'компл', 350),
    (8, 'Краска', 'л', 400);

INSERT INTO product_materials (product_id, material_id, norm_qty) VALUES
    (1, 1, 1.2), (1, 3, 0.2), (1, 7, 1),
    (2, 1, 0.4), (2, 2, 0.8), (2, 7, 1),
    (3, 1, 2.5), (3, 3, 0.5), (3, 7, 2),
    (4, 1, 0.8), (4, 7, 1),
    (5, 1, 3.0), (5, 4, 2.0), (5, 5, 1.5),
    (6, 1, 0.9), (6, 7, 1),
    (7, 1, 2.0), (7, 4, 4.0), (7, 5, 3.0),
    (8, 1, 1.0), (8, 4, 2.5), (8, 5, 2.0),
    (9, 1, 0.6), (9, 3, 0.1), (9, 7, 1);

INSERT INTO operations (operation_id, name, price) VALUES
    (1, 'Раскрой', 500),
    (2, 'Сборка', 800),
    (3, 'Покраска', 400),
    (4, 'Обшивка', 700),
    (5, 'Упаковка', 200);

INSERT INTO product_operations (product_id, operation_id, norm_hours) VALUES
    (1, 1, 0.5), (1, 2, 1.0), (1, 3, 0.5), (1, 5, 0.2),
    (2, 1, 0.3), (2, 2, 0.7), (2, 5, 0.1),
    (3, 1, 1.0), (3, 2, 1.5), (3, 3, 1.0),
    (4, 1, 0.4), (4, 3, 0.3), (4, 5, 0.1),
    (5, 1, 1.2), (5, 2, 2.0), (5, 4, 1.5), (5, 5, 0.3),
    (6, 1, 0.4), (6, 2, 0.8), (6, 5, 0.1),
    (7, 1, 1.0), (7, 2, 1.5), (7, 4, 2.0), (7, 5, 0.4),
    (8, 1, 0.6), (8, 2, 1.0), (8, 4, 1.2), (8, 5, 0.2),
    (9, 1, 0.3), (9, 2, 0.5), (9, 5, 0.1);

INSERT INTO orders (order_id, customer_id, order_date, status) VALUES
    (1, 1, date('now','-40 days'), 'Выполнен'),
    (2, 2, date('now','-30 days'), 'В работе'),
    (3, 3, date('now','-20 days'), 'Новый'),
    (4, 1, date('now','-10 days'), 'Выполнен'),
    (5, 4, date('now','-5 days'), 'Отменён'),
    (6, 5, date('now','-2 days'), 'Новый'),
    (7, 2, date('now','-1 days'), 'В работе'),
    (8, 3, date('now'), 'Новый');

INSERT INTO order_items (order_id, product_id, quantity) VALUES
    (1, 1, 2), (1, 2, 4),
    (2, 3, 1), (2, 4, 2),
    (3, 5, 1),
    (4, 1, 1), (4, 6, 2),
    (5, 7, 1),
    (6, 2, 6),
    (7, 8, 2), (7, 6, 1),
    (8, 3, 1), (8, 4, 3);
"""

WEEKS = [
    ("Неделя 1. Введение и предметная область", [
        ("Структура КИМ 09.02.07-5", "6 заданий, 3:30, 75 + 25 баллов, платформы.", 60),
        ("Предприятие и заказы", "Продукция, спецификации, материалы, нормы расхода, операции.", 70),
        ("ER-модель: сущности", "Заказчик, заказ, продукция, материал, операция, пользователь.", 70),
        ("ER-модель: связи", "1:M, M:N через product_materials и order_items.", 80),
        ("Мини-схема", "Нарисуй 11 таблиц и связи, проверь кардинальности.", 90),
    ]),
    ("Неделя 2. 3НФ и DDL", [
        ("1НФ/2НФ/3НФ", "Атомарность, зависимости, справочники.", 80),
        ("Ключи и ограничения", "PK/FK, UNIQUE, CHECK, ON DELETE.", 80),
        ("CREATE TABLE", "products, materials, product_materials, orders.", 90),
        ("ER в PDF", "draw.io/СУБД, таблицы, атрибуты, ключи, связи.", 90),
        ("Скрипт БД", "DDL + данные, PRAGMA foreign_keys=ON.", 90),
    ]),
    ("Неделя 3. SQL: выборки", [
        ("SELECT/WHERE/ORDER", "Каталог продукции, материалы, заказы.", 80),
        ("JOIN", "Продукция + спецификация, заказ + заказчик.", 90),
        ("GROUP BY", "Заказы по клиентам, материалы по продуктам.", 90),
        ("Подзапросы", "Стоимость продукции по материалам и операциям.", 100),
        ("SQL-практика 1–7", "Задачи s01–s07.", 90),
    ]),
    ("Неделя 4. SQL: стоимость", [
        ("Нормы расхода", "material.price × norm_qty.", 90),
        ("Операции", "operation.price × norm_hours.", 80),
        ("Себестоимость продукции", "SUM материалов + SUM операций.", 100),
        ("Стоимость заказа", "SUM(quantity × product_cost).", 100),
        ("SQL-практика 8–15", "Задачи s08–s15.", 100),
    ]),
    ("Неделя 5. Импорт и платформа", [
        ("JSON «Заказчики.json»", "Чтение JSON, проверка полей, INSERT.", 90),
        ("Python + SQLite", "Подключение, параметры, commit.", 80),
        ("Альтернативы", "C#, 1С, MS SQL — что меняется.", 70),
        ("Обработка ошибок", "try/except, rollback, сообщения.", 80),
        ("Импорт на практике", "Загрузи 5 заказчиков в БД.", 90),
    ]),
    ("Неделя 6. Задание 4: авторизация", [
        ("Таблица пользователей", "login, password, role, blocked, failed_attempts.", 80),
        ("Форма входа", "Логин, пароль, кнопка «Войти», обязательные поля.", 90),
        ("Роли", "Администратор и Пользователь.", 80),
        ("Сообщения", "«Вы успешно авторизовались», ошибка входа.", 80),
        ("Блокировка", "3 ошибки — блокировка, сообщение.", 100),
    ]),
    ("Неделя 7. Капча и админка", [
        ("Капча-пазл", "Сборка изображения из фрагментов, проверка.", 100),
        ("Админ: пользователи", "Добавление, редактирование, снятие блокировки.", 100),
        ("Проверка дублей", "Логин уже exists — сообщение.", 80),
        ("Интерфейс", "Единый стиль, заголовки, навигация.", 90),
        ("Пробник задания 4", "Таймер 1:00, авторизация + админка.", 60),
    ]),
    ("Неделя 8. Задание 5: API", [
        ("HTTP и JSON", "GET, статусы, структура ответа.", 80),
        ("API заказчиков", "GET /api/customers из БД.", 100),
        ("Обработка данных", "Маскирование телефона/email, преобразование.", 100),
        ("Ошибки API", "400/401/404/500, JSON-ошибки.", 80),
        ("Пробник API", "Таймер 1:00, endpoint + ответ.", 60),
    ]),
    ("Неделя 9. Postman и тесты", [
        ("Postman: коллекция", "Запросы, окружение, переменные.", 90),
        ("Тесты Postman", "pm.test, статус, поля, типы.", 100),
        ("Негативные тесты", "Неверный id, пустой ответ.", 90),
        ("Отладка", "Console, логи, повтор запроса.", 80),
        ("Пробник задания 5", "Коллекция + тесты.", 60),
    ]),
    ("Неделя 10. Документация", [
        ("Шаблон API", "Методы, параметры, примеры.", 90),
        ("Примеры запросов", "Request/response, коды.", 80),
        ("README проекта", "Запуск, стек, структура.", 80),
        ("ТестКейс.docx", "Действие, ожидаемый результат, результат.", 90),
        ("Пробник задания 6", "Таймер 0:20, документация.", 30),
    ]),
    ("Неделя 11. Интеграция", [
        ("Сборка модулей", "БД + авторизация + API.", 100),
        ("Отладка", "Ошибки, логи, граничные случаи.", 90),
        ("Производительность", "Индексы, лишние запросы.", 80),
        ("Git", "README, коммиты, структура.", 80),
        ("Полный сценарий", "Вход → API → тесты → docs.", 90),
    ]),
    ("Неделя 12. Пробники", [
        ("Пробник 1: задания 1–3", "Таймер 1:10.", 70),
        ("Разбор", "Критерии 75 баллов.", 70),
        ("Пробник 2: 1–4", "Таймер 2:10.", 130),
        ("Пробник 3: все 6", "Таймер 3:30.", 210),
        ("День экзамена", "Тайминг, git, документы.", 80),
    ]),
]

PLAN = []
for _w, (_theme, _days) in enumerate(WEEKS, start=1):
    for _d, (_title, _task, _minutes) in enumerate(_days, start=1):
        PLAN.append({
            "id": f"d{(_w - 1) * 5 + _d}",
            "n": (_w - 1) * 5 + _d,
            "week": _w,
            "theme": _theme,
            "title": _title,
            "task": _task,
            "minutes": _minutes,
        })

LESSONS = [
    ("l01", "Экзамен", "КИМ 09.02.07-5: 6 заданий и 100 баллов", 12, """
Официальный документ: КИМ 09.02.07-5-2027, квалификация
«Специалист по информационным системам», профильный уровень.

ВРЕМЯ (инвариант — 3 ч 30 мин)
• Задание 1. ER-диаграмма — 0:20.
• Задание 2. База данных по ER + импорт JSON — 0:30.
• Задание 3. SQL-запрос стоимости заказа — 0:20.
• Задание 4. Информационная система: вход, роли, капча, блокировка, админка — 1:00.
• Задание 5. API + Postman-тесты — 1:00.
• Задание 6. Проектная документация API — 0:20.

БАЛЛЫ
• Инвариант — 75: администрирование БД 17, проектирование и разработка ИС 33,
  интеграция 25.
• Вариативная часть — 25 (определяет колледж).

ПРЕДМЕТНАЯ ОБЛАСТЬ
Предприятие производит продукцию по спецификациям, использует материалы
с нормами расхода и технологические операции, принимает заказы покупателей.
Стоимость продукции = материалы + операции.

ЧТО СДАЁТСЯ
ER.pdf, schema.sql/скрипт БД, SQL-запрос, приложение с авторизацией и
админкой, API, коллекция Postman, документация, ТестКейс.docx.
"""),
    ("l02", "БД", "ER-диаграмма и 3НФ", 12, """
ER-диаграмма для предметной области «производство и заказы».

Сущности:
• customers — заказчики;
• orders — заказы;
• order_items — строки заказа;
• products — продукция;
• specifications — спецификации;
• materials — материалы;
• product_materials — нормы расхода материалов;
• operations — технологические операции;
• product_operations — нормы операций;
• users, roles — пользователи.

Связи:
customers 1—M orders
orders 1—M order_items
products 1—M order_items
specifications 1—M products
products M—N materials (product_materials)
products M—N operations (product_operations)

3НФ:
• материалы и операции — отдельные справочники;
• нормы расхода — в связующих таблицах;
• цена материала хранится в materials, а не в каждой строке;
• стоимость продукции не хранится, а вычисляется.

ER.pdf: 11 таблиц, атрибуты, PK/FK, связи 1:M и M:N, подписи.
"""),
    ("l03", "БД", "Таблицы, ключи и ограничения", 10, """
CREATE TABLE materials (
    material_id INTEGER PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    unit        TEXT NOT NULL,
    price       REAL NOT NULL CHECK (price >= 0)
);

CREATE TABLE product_materials (
    product_id  INTEGER NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
    material_id INTEGER NOT NULL REFERENCES materials(material_id),
    norm_qty    REAL NOT NULL CHECK (norm_qty > 0),
    PRIMARY KEY (product_id, material_id)
);

CREATE TABLE orders (
    order_id    INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date  TEXT NOT NULL,
    status      TEXT NOT NULL CHECK (status IN ('Новый','В работе','Выполнен','Отменён'))
);

CREATE TABLE order_items (
    order_id   INTEGER NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity   INTEGER NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (order_id, product_id)
);

Правила:
• PRAGMA foreign_keys = ON;
• UNIQUE на логины, ИНН, названия;
• CHECK на цену, количество, норму;
• ON DELETE CASCADE для строк заказа и норм продукции.
"""),
    ("l04", "SQL", "SELECT, JOIN и заказы", 10, """
SELECT p.product_id, p.name, s.spec_name
FROM products p
JOIN specifications s ON s.spec_id = p.spec_id
ORDER BY p.product_id;

SELECT o.order_id, c.name AS customer, o.order_date, o.status
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
ORDER BY o.order_id;

SELECT oi.order_id, p.name, oi.quantity
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
ORDER BY oi.order_id, p.name;

Группировка:
SELECT c.name, COUNT(o.order_id) AS orders_count
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name;

NULL: LEFT JOIN + COALESCE.
"""),
    ("l05", "SQL", "Себестоимость: материалы и операции", 12, """
Материалы:
SELECT pm.product_id, SUM(m.price * pm.norm_qty) AS material_cost
FROM product_materials pm
JOIN materials m ON m.material_id = pm.material_id
GROUP BY pm.product_id;

Операции:
SELECT po.product_id, SUM(o.price * po.norm_hours) AS operation_cost
FROM product_operations po
JOIN operations o ON o.operation_id = po.operation_id
GROUP BY po.product_id;

Себестоимость продукции:
SELECT p.product_id, p.name,
       ROUND(COALESCE(mc.material_cost, 0) + COALESCE(oc.operation_cost, 0), 2) AS cost
FROM products p
LEFT JOIN (SELECT product_id, SUM(m.price * pm.norm_qty) AS material_cost
           FROM product_materials pm
           JOIN materials m ON m.material_id = pm.material_id
           GROUP BY product_id) mc ON mc.product_id = p.product_id
LEFT JOIN (SELECT product_id, SUM(o.price * po.norm_hours) AS operation_cost
           FROM product_operations po
           JOIN operations o ON o.operation_id = po.operation_id
           GROUP BY product_id) oc ON oc.product_id = p.product_id;
"""),
    ("l06", "SQL", "Стоимость заказа и аналитика", 12, """
Стоимость заказа:
SELECT o.order_id, c.name,
       ROUND(SUM(oi.quantity * (
           COALESCE(mc.material_cost, 0) + COALESCE(oc.operation_cost, 0)
       )), 2) AS total
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
LEFT JOIN (...) mc ON mc.product_id = p.product_id
LEFT JOIN (...) oc ON oc.product_id = p.product_id
GROUP BY o.order_id, c.name;

Средний чек:
SELECT ROUND(AVG(total), 2) FROM (SELECT ... total ...);

Самый дорогой заказ:
SELECT ... ORDER BY total DESC LIMIT 1;

Товары без заказов:
SELECT p.product_id, p.name FROM products p
WHERE NOT EXISTS (SELECT 1 FROM order_items oi WHERE oi.product_id = p.product_id);
"""),
    ("l07", "Python", "Импорт JSON и SQLite", 10, """
import json, sqlite3

with open('Заказчики.json', encoding='utf-8') as f:
    data = json.load(f)

conn = sqlite3.connect('production.db')
conn.execute('PRAGMA foreign_keys = ON')
for item in data:
    conn.execute(
        'INSERT OR IGNORE INTO customers (name, inn, address, phone, email) '
        'VALUES (?, ?, ?, ?, ?)',
        (item['name'], item['inn'], item['address'], item['phone'], item['email']))
conn.commit()
conn.close()

Проверь:
• все поля обязательны;
• ИНН уникален;
• после импорта COUNT(customers) совпадает;
• ошибки не ломают транзакцию.
"""),
    ("l08", "ИС", "Авторизация и роли", 12, """
Таблица users:
user_id, login, password, full_name, role_id, is_blocked, failed_attempts.

Форма:
• поля «Логин» и «Пароль»;
• кнопка «Войти»;
• пустые поля — ошибка;
• неверная пара — «Вы ввели неверный логин или пароль...»;
• успех — «Вы успешно авторизовались».

Роли:
• Администратор — управление пользователями;
• Пользователь — работа с системой.

SQL входа:
SELECT user_id, full_name, role_id, is_blocked, failed_attempts
FROM users WHERE login = ? AND password = ?;

Если is_blocked = 1 — «Вы заблокированы. Обратитесь к администратору».
"""),
    ("l09", "ИС", "Капча-пазл и блокировка", 12, """
Капча:
• изображение разрезано на 4–9 фрагментов;
• пользователь собирает пазл;
• при верной сборке — доступ к входу;
• при неверной — попытка не засчитывается.

Блокировка:
• 3 неверных пароля или 3 неверных пазла подряд;
• is_blocked = 1;
• сообщение «Вы заблокированы. Обратитесь к администратору»;
• счётчик failed_attempts сбрасывается после успеха.

Админ:
• добавить пользователя;
• изменить данные;
• снять блокировку (is_blocked = 0, failed_attempts = 0);
• проверить уникальность логина.
"""),
    ("l10", "API", "API и обработка данных", 12, """
GET /api/customers — список заказчиков.

Требование: не отдавать данные в исходном виде. Перед ответом:
• телефон маскируется: +7(495)***-**-11;
• email маскируется: i***@mebelplus.ru;
• ИНН — только последние 4 цифры;
• адрес можно сократить.

Пример:
{
  "id": 1,
  "name": "ООО «Мебель Плюс»",
  "phone": "+7(495)***-**-11",
  "email": "i***@mebelplus.ru"
}

Коды: 200, 400, 404, 500. Ошибки — JSON.
"""),
    ("l11", "Postman", "Коллекция и тесты", 12, """
Коллекция:
• GET /api/customers;
• GET /api/customers/1;
• GET /api/customers/999 (404).

Тесты:
pm.test('status 200', () => pm.response.to.have.status(200));
pm.test('JSON', () => pm.response.to.be.json);
pm.test('masked phone', () => {
  pm.expect(pm.response.json()[0].phone).to.include('***');
});

Негативные:
• несуществующий id — 404;
• пустой список — 200 и [].
"""),
    ("l12", "Документы", "Проектная документация API", 10, """
Документация по шаблону:
• назначение API;
• базовый URL;
• авторизация (если есть);
• методы: путь, параметры, тело, ответ;
• примеры request/response;
• коды ошибок;
• ограничения.

Дополнительно:
• README: запуск, стек, структура;
• ER-диаграмма;
• ТестКейс.docx: действие, ожидаемый результат, результат.
"""),
    ("l13", "Интеграция", "Сборка и отладка", 10, """
Сценарий:
1. БД создана и заполнена.
2. Вход с ролью.
3. Админ добавляет пользователя.
4. API отдаёт заказчиков с маскированием.
5. Postman-тесты проходят.
6. Документация совпадает с API.

Отладка:
• логи;
• коды ответов;
• пустые и неверные данные;
• блокировка и разблокировка;
• повторный запуск.
"""),
    ("l14", "Экзамен", "Стратегия и тайминг", 10, """
Тайминг:
0:00–0:20 — ER.pdf;
0:20–0:50 — БД + импорт JSON;
0:50–1:10 — SQL-запрос стоимости;
1:10–2:10 — приложение: вход, капча, блокировка, админка;
2:10–3:10 — API + Postman;
3:10–3:30 — документация.

Порядок:
1. Сначала БД и ER — без них не работает остальное.
2. Затем авторизация и админка.
3. API и тесты.
4. Документация в конце, но по шаблону.

Частые потери:
• нет 3НФ/ключей;
• стоимость считается без норм расхода;
• нет капчи или блокировки;
• API отдаёт данные без маскирования;
• нет Postman-тестов;
• документация не по шаблону.
"""),
    ("l15", "Экзамен", "Чек-лист на 100 баллов", 10, """
• ER.pdf: 11 таблиц, связи, PK/FK.
• schema.sql: DDL + данные, PRAGMA foreign_keys.
• SQL: стоимость заказа с материалами и операциями.
• Вход: логин/пароль, роли, сообщения.
• Капча-пазл.
• Блокировка после 3 ошибок, снятие админом.
• Админ: добавление/редактирование пользователей.
• API: GET, JSON, маскирование.
• Postman: коллекция и тесты.
• Документация API по шаблону.
• README, ER, ТестКейс.docx.
• Git-репозиторий, коммиты.
"""),
]

def q(text, opts, ans, expl, topic):
    return {"q": text, "opts": opts, "ans": ans, "explain": expl, "topic": topic}

QUIZ = [
    q("Сколько заданий в КИМ 09.02.07-5-2027?", ["4", "5", "6", "7"], 2,
      "Шесть заданий: ER, БД, SQL, ИС, API, документация.", "Экзамен"),
    q("Сколько времени на инвариант профильного уровня?", ["2:30", "3:30", "4:00", "4:30"], 1,
      "3 ч 30 мин; вариативная часть увеличивает время.", "Экзамен"),
    q("Сколько баллов в инварианте?", ["50", "75", "80", "100"], 1,
      "75 инвариант + 25 вариатив = 100.", "Экзамен"),
    q("Что делается в задании 1?", ["API", "ER-диаграмма", "Авторизация", "Документация"], 1,
      "Задание 1 — ER-диаграмма в PDF.", "Экзамен"),
    q("Что импортируется в задании 2?", ["CSV", "JSON «Заказчики.json»", "Excel", "XML"], 1,
      "После создания БД импортируется JSON заказчиков.", "Экзамен"),
    q("Что считает SQL-запрос задания 3?", ["Количество товаров", "Полную стоимость заказа", "Средний возраст", "Рейтинг"], 1,
      "Стоимость с учётом количества, материалов и норм расхода.", "Экзамен"),
    q("Что обязательно в задании 4?", ["Чат", "Капча-пазл", "Видео", "Карта"], 1,
      "Интерактивная капча-пазл на странице авторизации.", "Экзамен"),
    q("Через сколько ошибок блокируется учётная запись?", ["1", "2", "3", "5"], 2,
      "После 3 неверных попыток подряд.", "Экзамен"),
    q("Что делает администратор?", ["Только смотрит", "Добавляет и редактирует пользователей, снимает блокировку", "Удаляет БД", "Пишет API"], 1,
      "Админ управляет пользователями и блокировками.", "Экзамен"),
    q("Что требуется от API в задании 5?", ["Отдавать данные как есть", "Маскировать/обрабатывать данные перед ответом", "Только HTML", "Только файлы"], 1,
      "Данные не должны выдаваться в исходном виде.", "Экзамен"),
    q("Чем тестируется API?", ["Postman", "Excel", "Word", "Paint"], 0,
      "Коллекция запросов и тесты в Postman.", "Экзамен"),
    q("Что в задании 6?", ["ER", "Документация API", "Капча", "SQL"], 1,
      "Проектная документация API по шаблону.", "Экзамен"),

    q("Что такое 3НФ?", ["Атомарность", "Зависимость от ключа", "Отсутствие транзитивных зависимостей", "Индексы"], 2,
      "3НФ = 2НФ + отсутствие транзитивных зависимостей.", "БД"),
    q("Что обеспечивает внешний ключ?", ["Скорость", "Ссылочную целостность", "Уникальность", "Шифрование"], 1,
      "Нельзя сослаться на несуществующую запись.", "БД"),
    q("Как включить FK в SQLite?", ["SET FK=1", "PRAGMA foreign_keys=ON", "FOREIGN=ON", "Никак"], 1,
      "По умолчанию выключено.", "БД"),
    q("Где хранится цена материала?", ["В product_materials", "В materials", "В orders", "В users"], 1,
      "Цена — атрибут материала, норма — в связующей таблице.", "БД"),
    q("Что такое norm_qty?", ["Цена", "Норма расхода материала", "Количество заказов", "Скидка"], 1,
      "Сколько материала нужно на единицу продукции.", "БД"),
    q("Что такое norm_hours?", ["Норма времени операции", "Цена материала", "Количество", "Статус"], 0,
      "Норма времени на операцию.", "БД"),

    q("Как выбрать заказы с заказчиками?", ["JOIN customers", "GROUP BY", "ORDER BY", "LIKE"], 0,
      "JOIN orders и customers по customer_id.", "SQL"),
    q("Как посчитать стоимость материалов продукции?", ["SUM(price * norm_qty)", "COUNT(*)", "AVG(price)", "MAX(quantity)"], 0,
      "Цена материала × норма расхода, затем SUM.", "SQL"),
    q("Как посчитать стоимость операций?", ["SUM(price * norm_hours)", "SUM(quantity)", "COUNT(*)", "AVG(norm_qty)"], 0,
      "Цена операции × норма времени.", "SQL"),
    q("Как получить себестоимость продукции?", ["Материалы + операции", "Только материалы", "Только операции", "Цена заказа"], 0,
      "Сумма стоимостей материалов и операций.", "SQL"),
    q("Как посчитать стоимость заказа?", ["SUM(quantity * product_cost)", "SUM(quantity)", "COUNT(*)", "AVG(price)"], 0,
      "Количество × себестоимость продукции.", "SQL"),
    q("Как найти товары без заказов?", ["NOT EXISTS", "JOIN", "GROUP BY", "ORDER BY"], 0,
      "NOT EXISTS по order_items.", "SQL"),
    q("Как найти самый дорогой заказ?", ["ORDER BY total DESC LIMIT 1", "ORDER BY total", "GROUP BY", "WHERE total"], 0,
      "Сортировка по стоимости и LIMIT 1.", "SQL"),
    q("Как посчитать средний чек?", ["AVG(total)", "SUM(total)", "COUNT(*)", "MAX(total)"], 0,
      "Среднее по стоимостям заказов.", "SQL"),
    q("Что делает LEFT JOIN?", ["Только совпадения", "Все строки левой таблицы", "Удаляет дубли", "Сортирует"], 1,
      "Сохраняет все строки левой таблицы.", "SQL"),

    q("Что должно быть в форме входа?", ["Только логин", "Логин, пароль и кнопка «Войти»", "Email", "Телефон"], 1,
      "Логин и пароль обязательны.", "ИС"),
    q("Какие роли нужны?", ["Гость и админ", "Администратор и Пользователь", "Только админ", "Менеджер"], 1,
      "Две роли: Администратор и Пользователь.", "ИС"),
    q("Что при неверном пароле?", ["Молчание", "Сообщение об ошибке", "Выход", "Удаление"], 1,
      "«Вы ввели неверный логин или пароль...».", "ИС"),
    q("Что при 3 ошибках?", ["Ничего", "Блокировка учётной записи", "Смена пароля", "Удаление"], 1,
      "Учётная запись блокируется.", "ИС"),
    q("Что видит заблокированный?", ["Форму", "«Вы заблокированы. Обратитесь к администратору»", "API", "ER"], 1,
      "Сообщение о блокировке.", "ИС"),
    q("Как снять блокировку?", ["Пользователь сам", "Администратор", "Перезагрузка", "Удаление БД"], 1,
      "Админ сбрасывает is_blocked и failed_attempts.", "ИС"),
    q("Что проверяется при добавлении пользователя?", ["Цвет", "Уникальность логина", "Размер файла", "API"], 1,
      "Логин не должен повторяться.", "ИС"),

    q("Что должно быть в API-ответе?", ["Исходные данные", "Обработанные/маскированные данные", "HTML", "Файл"], 1,
      "Данные не отдаются в исходном виде.", "API"),
    q("Как маскировать телефон?", ["Оставить", "Скрыть часть цифр", "Удалить", "Увеличить"], 1,
      "Например, +7(495)***-**-11.", "API"),
    q("Что проверяет Postman-тест?", ["Статус и JSON", "Цвет", "Шрифт", "Картинку"], 0,
      "Статус-код, формат, поля.", "API"),
    q("Что делать при несуществующем id?", ["200", "404", "500", "302"], 1,
      "404 Not Found.", "API"),
    q("Что должно быть в документации?", ["Только скриншот", "Методы, параметры, примеры", "Только код", "Только ER"], 1,
      "Полное описание API.", "Документы"),
]

SQL_TASKS = [
    {"id": "s01", "title": "1. Продукция и спецификации", "level": "лёгкое",
     "task": "Выведите product_id, наименование и спецификацию продукции. Сортировка по product_id.",
     "hint": "JOIN specifications",
     "expected": "SELECT p.product_id, p.name, s.spec_name FROM products p "
                 "JOIN specifications s ON s.spec_id = p.spec_id ORDER BY p.product_id;"},
    {"id": "s02", "title": "2. Материалы и цены", "level": "лёгкое",
     "task": "Выведите material_id, наименование, единицу и цену материалов. Сортировка по material_id.",
     "hint": "SELECT ... FROM materials ORDER BY material_id",
     "expected": "SELECT material_id, name, unit, price FROM materials ORDER BY material_id;"},
    {"id": "s03", "title": "3. Нормы расхода", "level": "среднее",
     "task": "Выведите product_id, наименование продукции, материал и норму расхода. Сортировка по product_id, material_id.",
     "hint": "product_materials JOIN products/materials",
     "expected": "SELECT pm.product_id, p.name, m.name, pm.norm_qty "
                 "FROM product_materials pm JOIN products p ON p.product_id = pm.product_id "
                 "JOIN materials m ON m.material_id = pm.material_id "
                 "ORDER BY pm.product_id, pm.material_id;"},
    {"id": "s04", "title": "4. Операции", "level": "лёгкое",
     "task": "Выведите operation_id, наименование и цену операций. Сортировка по operation_id.",
     "hint": "SELECT ... FROM operations",
     "expected": "SELECT operation_id, name, price FROM operations ORDER BY operation_id;"},
    {"id": "s05", "title": "5. Нормы операций", "level": "среднее",
     "task": "Выведите product_id, продукцию, операцию и норму времени. Сортировка по product_id, operation_id.",
     "hint": "product_operations JOIN products/operations",
     "expected": "SELECT po.product_id, p.name, o.name, po.norm_hours "
                 "FROM product_operations po JOIN products p ON p.product_id = po.product_id "
                 "JOIN operations o ON o.operation_id = po.operation_id "
                 "ORDER BY po.product_id, po.operation_id;"},
    {"id": "s06", "title": "6. Заказы и заказчики", "level": "среднее",
     "task": "Выведите order_id, заказчика, дату и статус заказов. Сортировка по order_id.",
     "hint": "JOIN orders/customers",
     "expected": "SELECT o.order_id, c.name, o.order_date, o.status "
                 "FROM orders o JOIN customers c ON c.customer_id = o.customer_id "
                 "ORDER BY o.order_id;"},
    {"id": "s07", "title": "7. Состав заказов", "level": "среднее",
     "task": "Выведите order_id, продукцию и количество по всем строкам заказов. Сортировка по order_id, product_id.",
     "hint": "order_items JOIN products",
     "expected": "SELECT oi.order_id, p.name, oi.quantity FROM order_items oi "
                 "JOIN products p ON p.product_id = oi.product_id "
                 "ORDER BY oi.order_id, oi.product_id;"},
    {"id": "s08", "title": "8. Стоимость материалов продукции", "level": "сложное",
     "task": "Для каждой продукции выведите product_id, наименование и стоимость материалов (цена × норма, сумма). Округлите до копеек.",
     "hint": "SUM(m.price * pm.norm_qty) + GROUP BY",
     "expected": "SELECT p.product_id, p.name, ROUND(SUM(m.price * pm.norm_qty), 2) "
                 "FROM products p JOIN product_materials pm ON pm.product_id = p.product_id "
                 "JOIN materials m ON m.material_id = pm.material_id "
                 "GROUP BY p.product_id, p.name ORDER BY p.product_id;"},
    {"id": "s09", "title": "9. Стоимость операций продукции", "level": "сложное",
     "task": "Для каждой продукции выведите product_id, наименование и стоимость операций (цена × норма времени). Округлите до копеек.",
     "hint": "SUM(o.price * po.norm_hours) + GROUP BY",
     "expected": "SELECT p.product_id, p.name, ROUND(SUM(o.price * po.norm_hours), 2) "
                 "FROM products p JOIN product_operations po ON po.product_id = p.product_id "
                 "JOIN operations o ON o.operation_id = po.operation_id "
                 "GROUP BY p.product_id, p.name ORDER BY p.product_id;"},
    {"id": "s10", "title": "10. Себестоимость продукции", "level": "сложное",
     "task": "Для каждой продукции выведите product_id, наименование и себестоимость = материалы + операции. Округлите до копеек.",
     "hint": "Два подзапроса: material_cost и operation_cost",
     "expected": "SELECT p.product_id, p.name, "
                 "ROUND(COALESCE((SELECT SUM(m.price * pm.norm_qty) FROM product_materials pm "
                 "JOIN materials m ON m.material_id = pm.material_id WHERE pm.product_id = p.product_id), 0) "
                 "+ COALESCE((SELECT SUM(o.price * po.norm_hours) FROM product_operations po "
                 "JOIN operations o ON o.operation_id = po.operation_id WHERE po.product_id = p.product_id), 0), 2) "
                 "FROM products p ORDER BY p.product_id;"},
    {"id": "s11", "title": "11. Стоимость заказов", "level": "сложное",
     "task": "Выведите order_id, заказчика и полную стоимость заказа (количество × себестоимость). Округлите до копеек. Сортировка по order_id.",
     "hint": "order_items + себестоимость продукции",
     "expected": "SELECT o.order_id, c.name, ROUND(SUM(oi.quantity * "
                 "(COALESCE((SELECT SUM(m.price * pm.norm_qty) FROM product_materials pm "
                 "JOIN materials m ON m.material_id = pm.material_id WHERE pm.product_id = p.product_id), 0) "
                 "+ COALESCE((SELECT SUM(op.price * po.norm_hours) FROM product_operations po "
                 "JOIN operations op ON op.operation_id = po.operation_id WHERE po.product_id = p.product_id), 0))), 2) "
                 "FROM orders o JOIN customers c ON c.customer_id = o.customer_id "
                 "JOIN order_items oi ON oi.order_id = o.order_id "
                 "JOIN products p ON p.product_id = oi.product_id "
                 "GROUP BY o.order_id, c.name ORDER BY o.order_id;"},
    {"id": "s12", "title": "12. Заказы по заказчикам", "level": "среднее",
     "task": "Выведите имя заказчика и количество его заказов. Сортировка по количеству по убыванию, затем по имени.",
     "hint": "LEFT JOIN orders + GROUP BY",
     "expected": "SELECT c.name, COUNT(o.order_id) AS cnt FROM customers c "
                 "LEFT JOIN orders o ON o.customer_id = c.customer_id "
                 "GROUP BY c.customer_id, c.name ORDER BY cnt DESC, c.name;"},
    {"id": "s13", "title": "13. Сумма по заказчикам", "level": "сложное",
     "task": "Выведите имя заказчика и сумму всех его заказов. Округлите до копеек. Сортировка по сумме по убыванию.",
     "hint": "Стоимость заказов + GROUP BY customer",
     "expected": "SELECT c.name, ROUND(SUM(oi.quantity * "
                 "(COALESCE((SELECT SUM(m.price * pm.norm_qty) FROM product_materials pm "
                 "JOIN materials m ON m.material_id = pm.material_id WHERE pm.product_id = p.product_id), 0) "
                 "+ COALESCE((SELECT SUM(op.price * po.norm_hours) FROM product_operations po "
                 "JOIN operations op ON op.operation_id = po.operation_id WHERE po.product_id = p.product_id), 0))), 2) AS total "
                 "FROM customers c JOIN orders o ON o.customer_id = c.customer_id "
                 "JOIN order_items oi ON oi.order_id = o.order_id "
                 "JOIN products p ON p.product_id = oi.product_id "
                 "GROUP BY c.customer_id, c.name ORDER BY total DESC, c.name;"},
    {"id": "s14", "title": "14. Продукция без заказов", "level": "среднее",
     "task": "Выведите product_id и наименование продукции, которая не входит ни в один заказ. Сортировка по product_id.",
     "hint": "NOT EXISTS (SELECT 1 FROM order_items ...)",
     "expected": "SELECT p.product_id, p.name FROM products p WHERE NOT EXISTS "
                 "(SELECT 1 FROM order_items oi WHERE oi.product_id = p.product_id) "
                 "ORDER BY p.product_id;"},
    {"id": "s15", "title": "15. Самый дорогой заказ", "level": "сложное",
     "task": "Выведите order_id и стоимость самого дорогого заказа. Округлите до копеек.",
     "hint": "ORDER BY total DESC LIMIT 1",
     "expected": "SELECT o.order_id, ROUND(SUM(oi.quantity * "
                 "(COALESCE((SELECT SUM(m.price * pm.norm_qty) FROM product_materials pm "
                 "JOIN materials m ON m.material_id = pm.material_id WHERE pm.product_id = p.product_id), 0) "
                 "+ COALESCE((SELECT SUM(op.price * po.norm_hours) FROM product_operations po "
                 "JOIN operations op ON op.operation_id = po.operation_id WHERE po.product_id = p.product_id), 0))), 2) AS total "
                 "FROM orders o JOIN order_items oi ON oi.order_id = o.order_id "
                 "JOIN products p ON p.product_id = oi.product_id "
                 "GROUP BY o.order_id ORDER BY total DESC, o.order_id LIMIT 1;"},
    {"id": "s16", "title": "16. Средний чек", "level": "сложное",
     "task": "Выведите среднюю стоимость заказа, округлённую до копеек.",
     "hint": "AVG(total) по подзапросу стоимости заказов",
     "expected": "SELECT ROUND(AVG(total), 2) FROM (SELECT o.order_id, "
                 "SUM(oi.quantity * (COALESCE((SELECT SUM(m.price * pm.norm_qty) FROM product_materials pm "
                 "JOIN materials m ON m.material_id = pm.material_id WHERE pm.product_id = p.product_id), 0) "
                 "+ COALESCE((SELECT SUM(op.price * po.norm_hours) FROM product_operations po "
                 "JOIN operations op ON op.operation_id = po.operation_id WHERE po.product_id = p.product_id), 0))) AS total "
                 "FROM orders o JOIN order_items oi ON oi.order_id = o.order_id "
                 "JOIN products p ON p.product_id = oi.product_id GROUP BY o.order_id);"},
    {"id": "s17", "title": "17. Пользователи и роли", "level": "лёгкое",
     "task": "Выведите user_id, логин, ФИО и роль пользователей. Сортировка по user_id.",
     "hint": "JOIN roles",
     "expected": "SELECT u.user_id, u.login, u.full_name, r.role_name "
                 "FROM users u JOIN roles r ON r.role_id = u.role_id ORDER BY u.user_id;"},
    {"id": "s18", "title": "18. Заблокированные пользователи", "level": "лёгкое",
     "task": "Выведите user_id, логин и количество неудачных попыток для заблокированных пользователей. Сортировка по user_id.",
     "hint": "WHERE is_blocked = 1",
     "expected": "SELECT user_id, login, failed_attempts FROM users "
                 "WHERE is_blocked = 1 ORDER BY user_id;"},
    {"id": "s19", "title": "19. INSERT: новый заказчик", "level": "среднее",
     "task": "Добавьте заказчика: ООО «Новый дом», ИНН 7706789012, Москва, ул. Лесная, 6, +7(495)666-66-66, new@dom.ru.",
     "hint": "INSERT INTO customers (name, inn, address, phone, email) VALUES (...)",
     "mode": "script",
     "verify": "SELECT customer_id, name, inn FROM customers ORDER BY customer_id;",
     "expected": "INSERT INTO customers (name, inn, address, phone, email) VALUES "
                 "('ООО «Новый дом»', '7706789012', 'Москва, ул. Лесная, 6', "
                 "'+7(495)666-66-66', 'new@dom.ru');"},
]

CRITERIA = [
    ("Соадминистрирование БД: администрирование компонент серверов — 6", [
        ("Создание БД, таблиц, ограничений", 3),
        ("Импорт JSON и проверка данных", 2),
        ("Работа с сервером БД", 1),
    ]),
    ("Соадминистрирование БД: выявление технических проблем — 11", [
        ("Связи и целостность", 4),
        ("SQL-запрос стоимости заказа", 5),
        ("Исправление ошибок запроса", 2),
    ]),
    ("Проектирование ИС: сбор исходных данных — 6", [
        ("Анализ предметной области", 3),
        ("ER-диаграмма в PDF", 3),
    ]),
    ("Проектирование ИС: разработка модулей ИС — 10", [
        ("Авторизация и роли", 3),
        ("Капча-пазл", 3),
        ("Админка пользователей", 4),
    ]),
    ("Проектирование ИС: подсистемы безопасности — 8", [
        ("Блокировка после 3 ошибок", 3),
        ("Снятие блокировки админом", 2),
        ("Проверка дублей логина", 1),
        ("Сообщения об ошибках", 2),
    ]),
    ("Проектирование ИС: проектная документация — 6", [
        ("Документация API по шаблону", 4),
        ("README и ER", 2),
    ]),
    ("Проектирование ИС: современные средства — 3", [
        ("Инструменты анализа и документации", 2),
        ("Git-репозиторий", 1),
    ]),
    ("Интеграция: тестовые наборы и сценарии — 9", [
        ("Коллекция Postman", 3),
        ("Позитивные тесты", 3),
        ("Негативные тесты", 3),
    ]),
    ("Интеграция: интеграция модулей — 15", [
        ("API отдаёт данные из БД", 5),
        ("Маскирование/обработка данных", 5),
        ("Коды ответов и JSON-ошибки", 3),
        ("Связка БД + API", 2),
    ]),
    ("Интеграция: отладка — 1", [
        ("Отладка и логи", 1),
    ]),
    ("Вариативная часть (определяет колледж) — 25", [
        ("Дополнительный API/отчёт", 5),
        ("Автотесты", 5),
        ("Документация пользователя", 5),
        ("Развёртывание", 5),
        ("Оптимизация", 5),
    ]),
]

SNIPPETS = [
    ("Схема БД: 11 таблиц", """CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    inn TEXT NOT NULL UNIQUE,
    address TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL
);
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    spec_id INTEGER NOT NULL REFERENCES specifications(spec_id),
    unit TEXT NOT NULL DEFAULT 'шт'
);
CREATE TABLE materials (
    material_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    unit TEXT NOT NULL,
    price REAL NOT NULL CHECK (price >= 0)
);
CREATE TABLE product_materials (
    product_id INTEGER NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
    material_id INTEGER NOT NULL REFERENCES materials(material_id),
    norm_qty REAL NOT NULL CHECK (norm_qty > 0),
    PRIMARY KEY (product_id, material_id)
);"""),
    ("Стоимость продукции", """SELECT p.product_id, p.name,
       ROUND(
         COALESCE((SELECT SUM(m.price * pm.norm_qty)
                   FROM product_materials pm
                   JOIN materials m ON m.material_id = pm.material_id
                   WHERE pm.product_id = p.product_id), 0)
         +
         COALESCE((SELECT SUM(o.price * po.norm_hours)
                   FROM product_operations po
                   JOIN operations o ON o.operation_id = po.operation_id
                   WHERE po.product_id = p.product_id), 0)
       , 2) AS cost
FROM products p
ORDER BY p.product_id;"""),
    ("Стоимость заказа", """SELECT o.order_id, c.name,
       ROUND(SUM(oi.quantity * (
         COALESCE((SELECT SUM(m.price * pm.norm_qty)
                   FROM product_materials pm
                   JOIN materials m ON m.material_id = pm.material_id
                   WHERE pm.product_id = p.product_id), 0)
         +
         COALESCE((SELECT SUM(op.price * po.norm_hours)
                   FROM product_operations po
                   JOIN operations op ON op.operation_id = po.operation_id
                   WHERE po.product_id = p.product_id), 0)
       )), 2) AS total
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
GROUP BY o.order_id, c.name
ORDER BY o.order_id;"""),
    ("Импорт JSON", """import json, sqlite3

with open('Заказчики.json', encoding='utf-8') as f:
    customers = json.load(f)

conn = sqlite3.connect('production.db')
conn.execute('PRAGMA foreign_keys = ON')
conn.executemany(
    'INSERT OR IGNORE INTO customers (name, inn, address, phone, email) '
    'VALUES (?, ?, ?, ?, ?)',
    [(c['name'], c['inn'], c['address'], c['phone'], c['email'])
     for c in customers])
conn.commit()
conn.close()"""),
    ("Авторизация и блокировка", """user = conn.execute(
    'SELECT user_id, role_id, is_blocked, failed_attempts '
    'FROM users WHERE login = ? AND password = ?',
    (login, password)).fetchone()

if user is None:
    show_error('Вы ввели неверный логин или пароль. Пожалуйста проверьте ещё раз введенные данные')
    return
if user['is_blocked']:
    show_error('Вы заблокированы. Обратитесь к администратору')
    return
show_info('Вы успешно авторизовались')"""),
    ("Капча-пазл", """# 3×3: правильные позиции фрагментов
correct = [0, 1, 2, 3, 4, 5, 6, 7, 8]
user_order = [4, 3, 5, 1, 0, 2, 7, 6, 8]  # то, что собрал пользователь

if user_order == correct:
    captcha_passed = True
else:
    failed_attempts += 1
    if failed_attempts >= 3:
        conn.execute('UPDATE users SET is_blocked = 1 WHERE user_id = ?', (user_id,))
        conn.commit()
        show_error('Вы заблокированы. Обратитесь к администратору')"""),
    ("Админ: снятие блокировки", """UPDATE users
SET is_blocked = 0, failed_attempts = 0
WHERE user_id = ?;

SELECT user_id, login, full_name, role_id, is_blocked
FROM users ORDER BY user_id;"""),
    ("API: заказчики с маскированием", """from flask import Flask, jsonify
app = Flask(__name__)

def mask_phone(phone):
    return phone[:8] + '***-**-' + phone[-2:]

def mask_email(email):
    name, domain = email.split('@')
    return name[0] + '***@' + domain

@app.get('/api/customers')
def customers():
    rows = db.execute('SELECT * FROM customers').fetchall()
    return jsonify([{
        'id': r['customer_id'],
        'name': r['name'],
        'phone': mask_phone(r['phone']),
        'email': mask_email(r['email']),
    } for r in rows])"""),
    ("Postman: тесты", """pm.test('status 200', () => {
  pm.response.to.have.status(200);
});
pm.test('JSON', () => {
  pm.response.to.be.json;
});
pm.test('phone masked', () => {
  pm.expect(pm.response.json()[0].phone).to.include('***');
});
pm.test('404 for unknown', () => {
  pm.expect(pm.response.code).to.eql(404);
});"""),
    ("Документация API", """# API заказчиков

## GET /api/customers
Возвращает список заказчиков с маскированными данными.

Ответ 200:
[
  {"id": 1, "name": "ООО «Мебель Плюс»",
   "phone": "+7(495)***-**-11", "email": "i***@mebelplus.ru"}
]

Ошибки:
- 404 — заказчик не найден;
- 500 — внутренняя ошибка."""),
    ("Git", """git init
git add .
git commit -m "feat: ER, БД и импорт JSON"
git branch -M main
git remote add origin <url>
git push -u origin main"""),
]
