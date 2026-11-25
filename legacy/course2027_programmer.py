# -*- coding: utf-8 -*-
"""
Содержание курса под ДЭ-2027, квалификация «Программист» (09.02.07-2-2027),
профильный уровень: 5 заданий, 100 баллов, 4 часа.
Предметная область: «Чудо Обувь». Стек: Python + SQLite.

Файл подключается в конце trainer.py и заменяет данные 2026 года.
"""
from __future__ import annotations

MAX_SCORE = 100
EXAM_TITLE = "ДЭ 09.02.07-2-2027 «Программист» · профильный уровень"

# ---------------------------------------------------------------------------
# 1. БАЗА ДАННЫХ: 8 таблиц «Чудо Обувь»
# ---------------------------------------------------------------------------
ROLES = [
    (1, "Администратор"),
    (2, "Менеджер"),
    (3, "Авторизованный пользователь"),
]

CATEGORIES = [
    (1, "Детская обувь"),
    (2, "Женская"),
    (3, "Мужская"),
]

SIZES = [
    18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
    36, 36.5, 37, 37.5, 38, 38.5, 39, 39.5, 40, 40.5, 41, 41.5, 42, 42.5,
    43, 44, 45,
]

USERS = [
    (1, "Иванов", "Иван", "Иванович", "admin", 1),
    (2, "Петров", "Пётр", "Петрович", "manager", 2),
    (3, "Сидорова", "Анна", "Сергеевна", "asidorova", 3),
    (4, "Павлова", "Елена", "Викторовна", "epavlova", 3),
    (5, "Васильева", "Ольга", "Игоревна", "ovasileva", 3),
    (6, "Смирнов", "Алексей", "Дмитриевич", "asmirnov", 3),
    (7, "Кузнецова", "Мария", "Андреевна", "mkuznetsova", 3),
    (8, "Попов", "Денис", "Сергеевич", "dpopov", 3),
    (9, "Новикова", "Ирина", "Павловна", "inovikova", 3),
    (10, "Морозов", "Кирилл", "Олегович", "kmorozov", 3),
]

# product_id, category_id, subcategory, name, manufacturer, description,
# composition, image_path, price
PRODUCTS = [
    (1, 2, "Кроссовки", "Кроссовки City Run", "Азимут",
     "Кроссовки для города и прогулок. Дышащий верх, мягкая подошва.",
     "текстиль, резина", "img/01.png", 4590.00),
    (2, 2, "Ботинки", "Ботинки Classic", "Марко",
     "Классические женские ботинки на низком каблуке.",
     "натуральная кожа", "img/02.png", 7890.00),
    (3, 2, "Туфли", "Туфли Office", "Elegance",
     "Туфли для офиса и деловых встреч. Устойчивый каблук.",
     "эко-кожа", None, 6290.00),
    (4, 2, "Сандалии", "Сандалии Summer", "Азимут",
     "Лёгкие летние сандалии с регулируемыми ремешками.",
     "текстиль, ЭВА", "img/04.png", 2990.00),
    (5, 2, "Кеды", "Кеды White", "Марко",
     "Белые кеды на каждый день. Съёмная стелька.",
     "текстиль, резина", None, 3990.00),
    (6, 2, "Ботинки", "Ботинки Winter", "Nord",
     "Утеплённые ботинки с мембраной для холодной погоды.",
     "нубук, мех", "img/06.png", 9490.00),
    (7, 2, "Туфли", "Туфли Elegance", "Elegance",
     "Вечерние туфли с декоративной пряжкой.",
     "эко-кожа", "img/07.png", 7290.00),
    (8, 3, "Кроссовки", "Кроссовки Trail", "Азимут",
     "Кроссовки для пересечённой местности и лёгкого треккинга.",
     "текстиль, резина", "img/08.png", 6990.00),
    (9, 3, "Ботинки", "Ботинки Trekker", "Nord",
     "Туристические ботинки с усиленной подошвой.",
     "нубук, резина", None, 8990.00),
    (10, 3, "Кеды", "Кеды Retro", "Марко",
     "Кеды в ретро-стиле, подходят к джинсам.",
     "текстиль, резина", "img/10.png", 4490.00),
    (11, 3, "Туфли", "Туфли Business", "Elegance",
     "Мужские туфли для делового стиля.",
     "натуральная кожа", "img/11.png", 8290.00),
    (12, 3, "Сандалии", "Сандалии Beach", "Азимут",
     "Пляжные сандалии, быстро сохнут.",
     "ЭВА", None, 3190.00),
    (13, 3, "Кроссовки", "Кроссовки Marathon", "Азимут",
     "Беговые кроссовки с амортизацией.",
     "текстиль, резина", "img/13.png", 9990.00),
    (14, 1, "Кроссовки", "Кроссовки Sun Kids", "Азимут",
     "Детские кроссовки с липучками.",
     "текстиль, резина", "img/14.png", 2490.00),
    (15, 1, "Ботинки", "Ботинки First Step", "Nord",
     "Детские ботинки с тёплой подкладкой.",
     "нубук, мех", None, 3290.00),
    (16, 1, "Кеды", "Кеды School", "Марко",
     "Школьные кеды, легко моются.",
     "текстиль, резина", "img/16.png", 2790.00),
]

# Остатки: product_id -> [(размер, количество), ...]
STOCK = {
    1: [(36, 2), (37, 3), (38, 1), (39, 0), (40, 2), (41, 0)],
    2: [(36, 1), (37, 1), (38, 1), (39, 0)],
    3: [(36, 2), (37, 2), (38, 2), (39, 2)],
    4: [(36, 0), (37, 1), (38, 1)],
    5: [(36, 3), (37, 3), (38, 3)],
    6: [(36, 1), (37, 1), (38, 1), (39, 1), (40, 1)],
    7: [(36, 1), (37, 0)],
    8: [(40, 2), (41, 3), (42, 1), (43, 0)],
    9: [(40, 1), (41, 1), (42, 1)],
    10: [(40, 4), (41, 4), (42, 4)],
    11: [(40, 1), (41, 1), (42, 1), (43, 1)],
    12: [(40, 0), (41, 2), (42, 2)],
    13: [(40, 2), (41, 2), (42, 2), (43, 2), (44, 2)],
    14: [(22, 2), (23, 2), (24, 2), (25, 2)],
    15: [(22, 1), (23, 1), (24, 1), (25, 1)],
    16: [(22, 1), (23, 1), (24, 1)],
}

SIZE_ID = {value: idx for idx, value in enumerate(SIZES, start=1)}
PRICE = {p[0]: p[8] for p in PRODUCTS}

PRODUCT_ITEMS = []
ITEM_ID = {}
_item_id = 1
for _pid, _pairs in STOCK.items():
    for _size, _qty in _pairs:
        PRODUCT_ITEMS.append((_item_id, _pid, SIZE_ID[_size], _qty))
        ITEM_ID[(_pid, _size)] = _item_id
        _item_id += 1

# order_id, смещение месяца (-1 — прошлый, 0 — текущий, -2 — позапрошлый),
# день месяца, user_id, [(product_id, size, quantity), ...]
ORDERS = [
    (1, -1, 3, 4, [(1, 36, 1)]),
    (2, -1, 7, 5, [(3, 37, 2)]),
    (3, -1, 12, 6, [(5, 38, 1)]),
    (4, -1, 18, 7, [(8, 41, 1)]),
    (5, 0, 2, 4, [(10, 40, 1)]),
    (6, 0, 9, 5, [(13, 42, 2)]),
    (7, 0, 15, 6, [(2, 37, 1)]),
    (8, -2, 5, 7, [(6, 38, 1)]),
    (9, -2, 20, 8, [(14, 24, 2)]),
    (10, -2, 25, 8, []),          # заказ без позиций — для LEFT JOIN
]


def _date_expr(month_offset: int, day: int) -> str:
    return (f"date('now','start of month','{month_offset} months',"
            f"'+{day} days')")


def _values_sql(rows) -> str:
    out = []
    for row in rows:
        vals = []
        for value in row:
            if value is None:
                vals.append("NULL")
            elif isinstance(value, str) and value.startswith("date('now'"):
                vals.append(value)          # уже SQL-выражение
            elif isinstance(value, (int, float)):
                vals.append(str(value))
            else:
                vals.append("'" + str(value).replace("'", "''") + "'")
        out.append(" (" + ",".join(vals) + ")")
    return ",\n".join(out)


_DDL = """
CREATE TABLE roles (
    role_id   INTEGER PRIMARY KEY,
    role_name TEXT NOT NULL UNIQUE
);
CREATE TABLE categories (
    category_id   INTEGER PRIMARY KEY,
    category_name TEXT NOT NULL UNIQUE
);
CREATE TABLE sizes (
    size_id    INTEGER PRIMARY KEY,
    size_value REAL NOT NULL UNIQUE CHECK (size_value > 0)
);
CREATE TABLE users (
    user_id     INTEGER PRIMARY KEY,
    last_name   TEXT NOT NULL,
    first_name  TEXT NOT NULL,
    middle_name TEXT,
    login       TEXT NOT NULL UNIQUE,
    role_id     INTEGER NOT NULL REFERENCES roles(role_id)
);
CREATE TABLE products (
    product_id   INTEGER PRIMARY KEY,
    category_id  INTEGER NOT NULL REFERENCES categories(category_id),
    subcategory  TEXT,
    name         TEXT NOT NULL,
    manufacturer TEXT NOT NULL,
    description  TEXT,
    composition  TEXT,
    image_path   TEXT,
    price        REAL NOT NULL CHECK (price >= 0)
);
CREATE TABLE product_items (
    item_id   INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
    size_id   INTEGER NOT NULL REFERENCES sizes(size_id) ON DELETE RESTRICT,
    quantity  INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    UNIQUE (product_id, size_id)
);
CREATE TABLE orders (
    order_id   INTEGER PRIMARY KEY,
    order_date TEXT NOT NULL,
    user_id    INTEGER NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT
);
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id      INTEGER NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    item_id       INTEGER NOT NULL REFERENCES product_items(item_id) ON DELETE RESTRICT,
    quantity      INTEGER NOT NULL CHECK (quantity > 0),
    unit_price    REAL NOT NULL CHECK (unit_price >= 0)
);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_items_product ON product_items(product_id);
CREATE INDEX idx_order_items_order ON order_items(order_id);
"""

_sql_parts = [_DDL]
_sql_parts.append("INSERT INTO roles (role_id, role_name) VALUES\n"
                  + _values_sql(ROLES) + ";\n")
_sql_parts.append("INSERT INTO categories (category_id, category_name) VALUES\n"
                  + _values_sql(CATEGORIES) + ";\n")
_sql_parts.append("INSERT INTO sizes (size_id, size_value) VALUES\n"
                  + _values_sql([(i, v) for i, v in enumerate(SIZES, 1)]) + ";\n")
_sql_parts.append("INSERT INTO users (user_id, last_name, first_name, middle_name, "
                  "login, role_id) VALUES\n" + _values_sql(USERS) + ";\n")
_sql_parts.append("INSERT INTO products (product_id, category_id, subcategory, name, "
                  "manufacturer, description, composition, image_path, price) VALUES\n"
                  + _values_sql(PRODUCTS) + ";\n")
_sql_parts.append("INSERT INTO product_items (item_id, product_id, size_id, quantity) VALUES\n"
                  + _values_sql(PRODUCT_ITEMS) + ";\n")

_order_rows = []
for oid, month, day, uid, _ in ORDERS:
    _order_rows.append((oid, _date_expr(month, day), uid))
_sql_parts.append("INSERT INTO orders (order_id, order_date, user_id) VALUES\n"
                  + _values_sql(_order_rows) + ";\n")

_order_item_rows = []
_oi_id = 1
for oid, _m, _d, _u, positions in ORDERS:
    for pid, size, qty in positions:
        _order_item_rows.append(
            (_oi_id, oid, ITEM_ID[(pid, size)], qty, PRICE[pid]))
        _oi_id += 1
_sql_parts.append("INSERT INTO order_items (order_item_id, order_id, item_id, "
                  "quantity, unit_price) VALUES\n"
                  + _values_sql(_order_item_rows) + ";\n")

SCHEMA_SQL = "".join(_sql_parts)

# ---------------------------------------------------------------------------
# 2. ПЛАН НА 12 НЕДЕЛЬ (60 занятий, 60–90 минут)
# ---------------------------------------------------------------------------
WEEKS = [
    ("Неделя 1. Python с нуля: первые программы", [
        ("Установка и первая программа", "Python с python.org, галочка Add to PATH, IDLE/VS Code, print('Привет').", 60),
        ("Переменные и типы", "int, float, str, bool, type(), преобразование типов. Цена, скидка, количество.", 60),
        ("Ввод и вывод", "input(), f-строки, форматирование денег {price:.2f}. Калькулятор скидки 25%.", 70),
        ("Арифметика и ошибки", "+ - * / // % **, приоритет, чтение traceback. Не бояться красного текста.", 60),
        ("Закрепление", "Программа: цена и скидка → итоговая цена; проверка на 3 наборах данных.", 70),
    ]),
    ("Неделя 2. Управление и структуры данных", [
        ("Условия", "if/elif/else, and/or/not. «много», если больше 5, иначе «мало».", 70),
        ("Цикл for", "range(), перебор списка, enumerate(). Сумма остатков по размерам.", 70),
        ("Цикл while", "while, break, continue. Повтор ввода логина до успеха.", 70),
        ("Списки и словари", "append(), срезы, dict, items(). Каталог как список словарей.", 80),
        ("Функции", "def, параметры, return. final_price(price, has_orders_last_month).", 80),
    ]),
    ("Неделя 3. Файлы, исключения, алгоритмы", [
        ("Файлы и CSV", "open(), with, encoding='utf-8', csv.DictReader. Подготовка файлов import.", 70),
        ("Исключения", "try/except/else/finally, ValueError, sqlite3.Error. Понятные сообщения.", 70),
        ("Отладка", "traceback, print-отладка, пошаговое выполнение, проверка после каждого изменения.", 60),
        ("Блок-схема по ГОСТ 19.701-90", "Овал, процесс, ромб (Да/Нет), ввод/вывод. Алгоритм оформления заказа.", 90),
        ("Модули проекта", "Разделение db.py / ui.py / main.py, __main__, структура папки для сдачи.", 60),
    ]),
    ("Неделя 4. SQL, часть 1: выборка", [
        ("SELECT и WHERE", "Столбцы, условия, AND/OR. Задания 1–3 в «SQL-практике».", 80),
        ("ORDER BY и LIMIT", "Сортировка по цене ASC/DESC — как в Задании 3. Задание 7.", 70),
        ("LIKE и поиск", "Поиск по наименованию и описанию. lower() в SQLite не работает с кириллицей.", 70),
        ("NULL и COALESCE", "Картинка-заглушка: image_path IS NULL. COALESCE(image_path,'picture.png').", 60),
        ("Закрепление", "Задания 1, 2, 5, 6, 7 без подсказок.", 80),
    ]),
    ("Неделя 5. SQL, часть 2: связи, агрегаты, даты", [
        ("JOIN", "products + categories, users + orders. Задания 8, 13.", 90),
        ("GROUP BY и агрегаты", "SUM(quantity) по модели, COUNT, AVG. Задания 2, 11.", 90),
        ("CASE и «много/мало»", "CASE WHEN SUM(quantity)>5 THEN 'много' ELSE 'мало' END.", 80),
        ("Даты и 25% скидка", "date('now','start of month','-1 month'), NOT EXISTS, CASE. Задание 4.", 100),
        ("Повторение SQL", "Задания 1–14 на время (40 минут).", 80),
    ]),
    ("Неделя 6. Проектирование БД «Чудо Обувь»", [
        ("Предметная область", "Приложение 1: пользователи, товары, размеры, позиции, заказы, строки.", 70),
        ("Ключи и связи", "PK/FK, 1:M, UNIQUE(product_id,size_id), ON DELETE CASCADE/RESTRICT.", 80),
        ("1НФ/2НФ/3НФ", "Размеры отдельно, категории отдельно, позиция = модель + размер.", 90),
        ("ER-диаграмма 8 таблиц", "draw.io / SSMS / DBeaver, PDF: таблицы, атрибуты, связи, PK/FK.", 90),
        ("DDL и ограничения", "CREATE TABLE, CHECK, UNIQUE, FK actions. См. lab/schema.sql.", 80),
    ]),
    ("Неделя 7. Задание 1: БД в SQLite + импорт", [
        ("sqlite3 из Python", "connect, execute, executemany, fetchall, commit, close.", 80),
        ("Скрипт БД с данными", "schema.sql: DDL + INSERT + динамические даты date('now',...).", 80),
        ("Импорт CSV", "csv.DictReader → справочники → товары → позиции → пользователи → заказы.", 90),
        ("Проверка ссылочной целостности", "PRAGMA foreign_keys=ON, попытки нарушить FK, ON DELETE.", 70),
        ("Сдача Задания 1", "schema.sql, ER.pdf, данные, скриншоты. Чек-лист 15 баллов.", 90),
    ]),
    ("Неделя 8. tkinter: интерфейс", [
        ("Окно и виджеты", "Tk, Frame, Label, Entry, Button, pack/grid, заголовок окна.", 80),
        ("Treeview", "Таблица товаров: колонки, heading, tags для подсветки.", 90),
        ("События и переменные", "StringVar, trace_add('write') — поиск без кнопки «Найти».", 80),
        ("Сообщения и валидация", "showerror/showwarning/showinfo, askyesno, проверка чисел.", 70),
        ("Экраны и переходы", "Frame + tkraise(), «Назад», ФИО в правом верхнем углу.", 90),
    ]),
    ("Неделя 9. Задание 2: каталог и скидка", [
        ("Алгоритм и блок-схема", "Алгоритм оформления заказа + расчёт цены со скидкой → PDF.", 80),
        ("Стиль, логотип, иконка", "Приложение 3: цвета, шрифты, название компании, icon, logo.", 70),
        ("Каталог из БД", "Изображение, категория, наименование, производство, состав, цена.", 90),
        ("Много/мало и подсветка", "SUM(quantity)>5 → «много»; ≤3 → светло-красный фон.", 80),
        ("Скидка 25%", "Нет заказов в прошлом месяце → price*0.75; проверка на данных.", 100),
    ]),
    ("Неделя 10. Задание 3: авторизация и заказ", [
        ("Вход только по логину", "Список пользователей из БД, без пароля, «Без входа» для гостя.", 80),
        ("Роли и ФИО", "Гость / пользователь / менеджер / администратор, ФИО справа вверху, выход.", 80),
        ("Поиск, фильтр, сортировка", "Категория «Все категории», цена ↑↓, поиск по названию и описанию.", 100),
        ("Карточка товара", "Все поля, размерный ряд, доступные размеры, количество, «В корзину».", 100),
        ("Оформление заказа", "Корзина, подтверждение, дата, списание остатков, обновление каталога.", 120),
    ]),
    ("Неделя 11. Задания 4–5: заказы и статистика", [
        ("Список заказов", "Дата, ФИО клиента, итоговая сумма, кнопка «Состав».", 90),
        ("Состав заказа", "Товар + производство, размер, количество, цена за единицу, сумма.", 90),
        ("Добавление и удаление", "Выбор товара с поиском, размер, количество; удаление позиции.", 100),
        ("Администратор", "Изменение даты заказа, удаление позиций, обновление списков.", 90),
        ("Статистика и руководство", "Кнопка «Статистика», 3 показателя, Руководство_пользователя.docx 1–2 стр.", 110),
    ]),
    ("Неделя 12. Пробники и сдача на 5", [
        ("Пробник №1: Задания 1–2", "Таймер 1 ч 30 мин. БД + ER + импорт + каталог + скидка.", 110),
        ("Разбор ошибок №1", "Чек-лист на 100 баллов, слабые критерии, повтор теории.", 70),
        ("Пробник №2: Задания 1–3", "Таймер 2 ч 30 мин. Плюс авторизация, фильтры, заказ.", 150),
        ("Пробник №3: все 5 заданий", "Таймер 4 ч 00 мин. Цель ≥90% на «5».", 240),
        ("Экзаменационный день", "Артефакты, git, README, руководство, тайминг, запреты.", 80),
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

# ---------------------------------------------------------------------------
# 3. ТЕОРИЯ
# ---------------------------------------------------------------------------
LESSONS = [
    ("l01", "Экзамен", "ДЭ-2027: 5 заданий и 100 баллов", 10, """
Официальный проект КИМ: 09.02.07-2-2027, квалификация «Программист»,
профильный уровень. ФГОС СПО 09.02.07, приказ Минобрнауки от 09.12.2016 № 1547.

Структура (4 часа = 240 минут):
• Задание 1. База данных средствами СУБД — 50 мин, 15 баллов
• Задание 2. Алгоритм и приложение — 40 мин, 10 баллов
• Задание 3. Интерфейс и оформление заказа — 60 мин, 25 баллов
• Задание 4. Работа с заказами у Администратора и Менеджера — 60 мин, 25 баллов
• Задание 5. Статистика заказов + руководство пользователя — 30 мин, 25 баллов
  (вариативная часть; инвариант = 75, всего 100)

Предметная область: торговая компания «Чудо Обувь». 8 таблиц:
роли, категории, размеры, пользователи, товары, товарные позиции,
заказы, строки заказов.

Ключевые отличия от 2026 года:
• вход в систему ТОЛЬКО по логину, пароль не нужен;
• товарная позиция = модель + размер, остаток хранится по размерам;
• скидка 25% — товарам, по которым НЕ БЫЛО заказов в прошлом календарном месяце;
• «много» — больше 5 пар суммарно по размерам, «мало» — 5 и меньше;
• строки с остатком ≤ 3 подсвечиваются светло-красным;
• в Задании 5 — окно статистики и Руководство_пользователя.docx;
• в репозитории нужен README.md с описанием функциональности.

Артефакты: ER.pdf, блок-схема.pdf, schema.sql (с данными), исходники папкой
(не архив), исполняемые файлы, README.md, Руководство_пользователя.docx.
"""),
    ("l02", "Python", "Python за одну страницу", 10, """
name = input('Логин: ')                  # str
price = 4590.0                          # float
quantity = 2                            # int
has_orders = False                      # bool
print(f'{name}: {price:.2f} руб., {quantity} шт.')

if quantity > 5:
    label = 'много'
else:
    label = 'мало'

for size, qty in [(36, 2), (37, 3), (38, 1)]:
    print(size, qty)

products = []                           # список
products.append({'id': 1, 'name': 'Кроссовки', 'price': 4590.0})
first = products[0]                     # словарь
print(first['price'])

def final_price(price: float, no_orders_last_month: bool) -> float:
    '''Цена с учётом скидки 25% (Задание 2).'''
    return round(price * 0.75, 2) if no_orders_last_month else price

Главное: отступы 4 пробела, двоеточие после if/for/def, имена в snake_case,
одна команда в строке (требование КИМ).
"""),
    ("l03", "Python", "Управление, коллекции, функции", 10, """
# Условия
total = 4
if total > 5:
    label = 'много'
elif total <= 3:
    label = 'мало (подсветить)'
else:
    label = 'мало'

# Циклы
total = 0
for size, qty in stock:
    total += qty
while True:
    login = input('Логин: ')
    if login:
        break

# Списки и словари
items = [{'product_id': 1, 'qty': 2}, {'product_id': 2, 'qty': 1}]
by_id = {item['product_id']: item for item in items}
cart = []
cart.append({'item_id': 5, 'qty': 2, 'price': 4590.0})

# Функции
def order_total(rows):
    return round(sum(r['qty'] * r['price'] for r in rows), 2)

Для экзамена достаточно этих конструкций: условия, for, while, list, dict,
функции, try/except.
"""),
    ("l04", "Python", "Исключения, отладка, файлы", 8, """
try:
    price = float(entry_price.get())
    if price < 0:
        raise ValueError('Цена не может быть отрицательной')
except ValueError as err:
    messagebox.showerror('Ошибка ввода',
        f'{err}. Введите число >= 0 и повторите сохранение.')
except sqlite3.Error as err:
    messagebox.showerror('Ошибка базы данных',
        f'Не удалось сохранить данные: {err}')
finally:
    pass

CSV:
import csv
with open('products_import.csv', encoding='utf-8', newline='') as f:
    for row in csv.DictReader(f, delimiter=';'):
        print(row['name'], row['price'])

Отладка: читай traceback снизу вверх; проверяй путь к БД; после INSERT/UPDATE/
DELETE вызывай commit(); после изменения данных перезапрашивай SELECT и обновляй
таблицу на экране; делай скриншоты корректной работы.
"""),
    ("l05", "БД", "8 таблиц «Чудо Обувь»", 10, """
Таблицы и связи:
  roles 1—M users
  categories 1—M products
  products 1—M product_items M—1 sizes
  users 1—M orders
  orders 1—M order_items M—1 product_items

Почему так:
• размер — отдельная сущность (35 значений), а не столбцы 36,37,38;
• товарная позиция = сочетание модели и размера + количество на складе;
• в order_items хранится историческая цена за единицу (цена в каталоге может
  измениться, а сумма заказа — нет);
• итоговая сумма заказа НЕ хранится, она считается:
  SUM(order_items.quantity * order_items.unit_price).

Ограничения:
• UNIQUE(product_id, size_id) — одна позиция на пару «модель+размер»;
• CHECK(quantity >= 0), CHECK(price >= 0), CHECK(quantity > 0) в строках;
• ON DELETE CASCADE для order_items при удалении заказа;
• ON DELETE RESTRICT для товарной позиции, которая уже есть в заказе.

Вход только по логину: users.login, поле password НЕ нужно.
"""),
    ("l06", "БД", "3НФ, ключи и ER-диаграмма", 10, """
1НФ — атомарные значения, нет повторяющихся групп.
  Плохо: sizes = '36,37,38' в одной ячейке.
  Хорошо: таблица sizes + product_items.

2НФ — неключевой атрибут зависит от ВСЕГО ключа.
  В product_items ключ (product_id, size_id), количество зависит от пары.

3НФ — нет транзитивных зависимостей.
  Плохо: products(..., category_name, manufacturer_address).
  Хорошо: categories отдельно, производитель — атрибут товара, пока у него
  нет собственных сущностей.

ER-диаграмма (PDF) должна содержать:
• 8 таблиц и все атрибуты;
• PK и FK;
• связи 1:M со стороны «один»;
• согласованные имена (snake_case, *_id).

Инструменты: draw.io, DBeaver, SSMS, dbdiagram.io. На экзамене интернет
ограничен — ставь draw.io desktop заранее.
"""),
    ("l07", "Документы", "Блок-схема по ГОСТ 19.701-90", 8, """
Задание 2: «Сформировать алгоритм работы системы оформления заказа обуви.
Разработать алгоритм расчёта цены товара с учётом скидки. Алгоритмы
реализовать в виде кода».

Символы: овал — начало/конец; прямоугольник — процесс; ромб — решение
(выходы «Да»/«Нет»); параллелограмм — ввод/вывод; стрелки — поток.

Алгоритм оформления заказа:
Начало → Вход по логину → Проверить логин в БД
  → Нет: сообщение → вернуться ко входу
  → Да: каталог → Выбрать товар → Выбрать размер и количество
  → Добавить в корзину → Подтвердить заказ?
     Нет → вернуться в каталог
     Да → Проверить остаток → Создать заказ → Списать остаток
          → Обновить каталог → Конец

Алгоритм цены:
Начало → Взять цену → Есть заказы товара в прошлом месяце?
  → Да: цена без скидки
  → Нет: цена × 0,75
→ Округлить до 2 знаков → Конец

Ошибки: нет «Начало/Конец», ромб без «Да/Нет», не PDF, алгоритм не про скидку.
"""),
    ("l08", "SQL", "SELECT, WHERE, ORDER BY, LIKE", 9, """
SELECT p.product_id, p.name, c.category_name, p.price
FROM products p
JOIN categories c ON p.category_id = c.category_id
WHERE p.price > 3000
ORDER BY p.price DESC;

Поиск по наименованию И описанию (Задание 3):
WHERE p.name LIKE '%Кросс%' OR p.description LIKE '%Кросс%'

ВАЖНО: lower() в SQLite не понижает регистр кириллицы. Для поиска без учёта
регистра делайте это в Python: 'кросс' in text.lower().

NULL: image_path IS NULL → подставить 'picture.png' через COALESCE.

Сортировка по цене: ORDER BY price ASC / DESC — это выпадающий список
«По цене ↑ / По цене ↓» в Задании 3.
"""),
    ("l09", "SQL", "JOIN, GROUP BY, CASE, даты", 12, """
-- Остаток по модели и «много/мало» (Задание 2)
SELECT p.product_id, p.name, COALESCE(SUM(pi.quantity), 0) AS total,
       CASE WHEN COALESCE(SUM(pi.quantity), 0) > 5
            THEN 'много' ELSE 'мало' END AS label
FROM products p
LEFT JOIN product_items pi ON pi.product_id = p.product_id
GROUP BY p.product_id, p.name;

-- Подсветка: остаток ≤ 3
HAVING COALESCE(SUM(pi.quantity), 0) <= 3

-- Скидка 25% товарам без заказов в прошлом календарном месяце
CASE WHEN NOT EXISTS (
    SELECT 1
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    JOIN product_items pi ON pi.item_id = oi.item_id
    WHERE pi.product_id = p.product_id
      AND o.order_date >= date('now','start of month','-1 month')
      AND o.order_date <  date('now','start of month')
) THEN ROUND(p.price * 0.75, 2)
  ELSE p.price
END AS final_price

-- Итог заказа
SUM(oi.quantity * oi.unit_price)

-- Статистика (Задание 5)
SELECT COUNT(*) AS orders_count,
       COALESCE(SUM(total), 0) AS revenue,
       ROUND(COALESCE(SUM(total), 0) / COUNT(*), 2) AS avg_check
FROM (
    SELECT o.order_id, SUM(oi.quantity * oi.unit_price) AS total
    FROM orders o
    LEFT JOIN order_items oi ON oi.order_id = o.order_id
    GROUP BY o.order_id
);
"""),
    ("l10", "SQL", "DDL, INSERT/UPDATE/DELETE, скрипт БД", 9, """
CREATE TABLE product_items (
    item_id   INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
    size_id   INTEGER NOT NULL REFERENCES sizes(size_id) ON DELETE RESTRICT,
    quantity  INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    UNIQUE (product_id, size_id)
);

INSERT INTO users (last_name, first_name, middle_name, login, role_id)
VALUES ('Новиков', 'Олег', 'Игоревич', 'onovikov', 3);

UPDATE orders SET order_date = ? WHERE order_id = ?;

DELETE FROM order_items WHERE order_item_id = ?;

Правила:
• PRAGMA foreign_keys = ON — в SQLite по умолчанию ВЫКЛЮЧЕНО;
• после INSERT/UPDATE/DELETE — commit();
• скрипт БД сдаётся С ДАННЫМИ: DDL + INSERT + ограничения;
• ID новой записи: cursor.lastrowid (SQLite) / SCOPE_IDENTITY() (SQL Server).

Динамические даты для демо-данных:
INSERT INTO orders (order_date, user_id)
VALUES (date('now','start of month','-1 month','+3 days'), 4);
"""),
    ("l11", "Python", "Python + SQLite: рабочий каркас", 10, """
import sqlite3
from pathlib import Path

DB = Path(__file__).with_name('chudo_obuv.db')
conn = sqlite3.connect(DB)
conn.execute('PRAGMA foreign_keys = ON')
cur = conn.cursor()

cur.execute('''
    SELECT p.product_id, p.name, p.price, c.category_name
    FROM products p
    JOIN categories c ON p.category_id = c.category_id
    ORDER BY p.product_id
''')
for pid, name, price, category in cur.fetchall():
    print(pid, name, price, category)

# Параметризованный запрос — только так!
cur.execute('SELECT user_id, last_name, first_name, role_id FROM users WHERE login = ?',
            (login,))
user = cur.fetchone()

# Запись
cur.execute('INSERT INTO orders (order_date, user_id) VALUES (date("now"), ?)', (user[0],))
order_id = cur.lastrowid
cur.execute('INSERT INTO order_items (order_id, item_id, quantity, unit_price) '
            'VALUES (?, ?, ?, ?)', (order_id, item_id, qty, price))
cur.execute('UPDATE product_items SET quantity = quantity - ? WHERE item_id = ?',
            (qty, item_id))
conn.commit()

Транзакция важна: заказ, строки и списание остатка должны сохраниться вместе.
Если что-то упало — conn.rollback().
"""),
    ("l12", "UI", "tkinter: экраны, таблица, события", 10, """
root = tk.Tk()
root.title('Чудо Обувь — каталог')

search_var = tk.StringVar()
ttk.Entry(parent, textvariable=search_var).pack(fill='x')
search_var.trace_add('write', lambda *_: refresh())   # поиск в реальном времени

table = ttk.Treeview(parent, columns=('name', 'price', 'stock'), show='headings')
for col, title in zip(('name', 'price', 'stock'),
                      ('Наименование', 'Цена', 'Остаток')):
    table.heading(col, text=title)
table.pack(fill='both', expand=True)

table.tag_configure('low_stock', background='#FFB6B6')   # светло-красный
table.tag_configure('discount', foreground='#c0392b')

def refresh():
    table.delete(*table.get_children())
    for row in load_products(search_var.get(), category_var.get(), sort_var.get()):
        tag = 'low_stock' if row['total'] <= 3 else ''
        table.insert('', 'end',
                     values=(row['name'], row['final_price'], row['label']),
                     tags=(tag,))

Экраны: LoginFrame, CatalogFrame, ProductFrame, CartFrame, OrdersFrame,
OrderViewFrame, StatisticsFrame. Все лежат в одном контейнере grid и
переключаются через frame.tkraise(). У каждого — свой заголовок окна.
"""),
    ("l13", "Экзамен", "Задания 2–3: каталог, скидка, заказ", 12, """
ЗАДАНИЕ 2 (10 баллов, 40 мин)
• алгоритм оформления заказа + алгоритм цены со скидкой (блок-схема PDF);
• название приложения с названием компании, стиль, логотип, иконка;
• каталог: изображение (или picture.png), категория, наименование,
  производство, состав, цена со скидкой, «много/мало»;
• подсветка светло-красным при остатке ≤ 3;
• скидка 25% товарам без заказов в прошлом календарном месяце;
• отладка: нет аварийных завершений.

ЗАДАНИЕ 3 (25 баллов, 60 мин)
• вход ТОЛЬКО по логину (без пароля) + «Без входа» для гостя;
• ФИО в правом верхнем углу, выход;
• навигация, «Назад», заголовок каждого окна;
• обработка ошибок: заголовок, пиктограмма, что делать; валидация полей;
• сортировка по цене ↑↓ (выпадающий список);
• фильтр по категории, первый пункт «Все категории» (сбрасывает фильтр);
• поиск по наименованию и описанию;
• всё в реальном времени, поиск+фильтр+сортировка совместно;
• карточка товара: изображение, производство, наименование, категория,
  цена со скидкой, состав, описание, размерный ряд, доступные размеры;
• выбор размера и количества, добавление позиций, подтверждение заказа,
  дата заказа, списание остатка, обновление каталога.

Гость видит каталог без поиска/сортировки/фильтра.
"""),
    ("l14", "Экзамен", "Задания 4–5: заказы, статистика, документы", 12, """
ЗАДАНИЕ 4 (25 баллов, 60 мин)
• у Менеджера и Администратора — список заказов: дата, ФИО клиента;
• добавить заказ: выбрать товар из каталога с поиском по наименованию,
  выбрать размер и количество;
• состав заказа: товар (наименование + производство), размер, количество,
  цена за единицу, итоговая сумма;
• удалить позицию, добавить новую;
• Администратор: изменить дату заказа, удалить позиции;
• после изменений — обновить список;
• git-репозиторий + README.md с описанием функциональности.

ЗАДАНИЕ 5 (25 баллов, 30 мин)
• кнопка «Статистика» у Менеджера и Администратора;
• таблица всех заказов: номер, дата, ФИО клиента, итоговая сумма;
• 3 показателя: количество заказов, выручка, средний (или максимальный) чек;
• Руководство_пользователя.docx/.pdf, 1–2 страницы, 3+ скриншота:
  назначение и вход; каталог; заказы; статистика;
• загрузить код, скрипт БД и руководство в репозиторий.

Тайминг: 50 / 40 / 60 / 60 / 30 минут. За 5 минут до конца задания —
сохранить и загрузить файлы. Недосданный файл = 0 баллов за критерий.
"""),
    ("l15", "Экзамен", "Стратегия: с нуля до 5 из 5", 10, """
ЦЕЛЬ «5»: ≥90% (90+ из 100). Это значит, что нельзя «забыть» целое задание:
все 5 заданий должны быть сделаны, а мелочи — закрыты.

Порядок освоения:
1. Python-минимум (3 недели): переменные, условия, циклы, списки, словари,
   функции, файлы, исключения.
2. SQL (2 недели): SELECT, JOIN, GROUP BY, CASE, даты, подзапросы.
3. БД (1 неделя): 8 таблиц, 3НФ, ER, DDL, импорт.
4. tkinter (1 неделя): окна, Treeview, события, сообщения.
5. Задание 2 (1 неделя): каталог, «много/мало», подсветка, скидка 25%.
6. Задание 3 (1 неделя): вход по логину, фильтры, карточка, корзина, заказ.
7. Задания 4–5 (1 неделя): заказы, состав, статистика, руководство.
8. Пробники (1 неделя): три прогона с таймером и разбор ошибок.

Принципы:
• один рабочий каркас, доведённый до автоматизма, а не импровизация;
• сначала «дорогие» задания: 3 и 4 по 25 баллов, 5 — ещё 25;
• чек-лист на 100 баллов перед каждым пробником;
• сохранять и заливать в git каждые 10–15 минут;
• мелочи (ФИО, «Все категории», «Назад», заголовки, подсветка, скидка)
  стоят десятки баллов — их нельзя оставлять «на потом».
"""),
]

# ---------------------------------------------------------------------------
# 4. ТЕСТЫ
# ---------------------------------------------------------------------------
def q(text, opts, ans, expl, topic):
    return {"q": text, "opts": opts, "ans": ans, "explain": expl, "topic": topic}


QUIZ = [
    q("Сколько заданий и баллов на ДЭ-2027 (профильный уровень)?",
      ["4 задания / 75", "5 заданий / 100", "3 задания / 50", "5 заданий / 75"], 1,
      "5 заданий, 100 баллов: 15 + 10 + 25 + 25 + 25.", "Экзамен"),
    q("Сколько времени даётся на все задания?",
      ["3 ч", "4 ч", "5 ч", "1 ч 30 мин"], 1,
      "50 + 40 + 60 + 60 + 30 = 240 минут = 4 часа.", "Экзамен"),
    q("Сколько баллов даёт Задание 1 (БД)?",
      ["10", "15", "25", "30"], 1, "Задание 1 — 15 баллов, 50 минут.", "Экзамен"),
    q("Сколько таблиц должно быть в БД «Чудо Обувь»?",
      ["5", "6", "8", "11"], 2,
      "8: роли, категории, размеры, пользователи, товары, товарные позиции, заказы, строки заказов.", "БД"),
    q("Как входят в систему по КИМ-2027?",
      ["Логин и пароль", "Только по логину", "По email", "По номеру телефона"], 1,
      "«Вход в систему следует производить только по логину... Пароль при этом вводить не требуется».", "Экзамен"),
    q("Какой остаток считается «много»?",
      ["Больше 3", "Больше 5", "5 и меньше", "Ровно 5"], 1,
      "«много» — суммарно больше 5 пар по всем размерам, иначе «мало».", "Экзамен"),
    q("При каком остатке строку подсвечивают светло-красным?",
      ["≤ 3", "≤ 5", "= 0", "> 5"], 0, "«...количество которых суммарно по всем размерам меньше или равно трем».", "Экзамен"),
    q("Кому даётся скидка 25% в Задании 2?",
      ["Всем товарам", "Товарам без заказов в прошлом календарном месяце", "Товарам с остатком 0", "Товарам дороже 5000"], 1,
      "Скидка 25% — товарам, по которым отсутствуют заказы в предыдущем календарном месяце.", "Экзамен"),
    q("Что такое товарная позиция?",
      ["Модель", "Модель + размер", "Заказ", "Категория"], 1,
      "Товарная позиция — сочетание модели и размера, у неё свой остаток.", "БД"),
    q("Где хранится итоговая сумма заказа?",
      ["В orders.total", "В products.price", "Считается из строк заказа", "В users"], 2,
      "Сумма = SUM(order_items.quantity * order_items.unit_price), отдельно не хранится.", "БД"),
    q("Первый пункт фильтра по категории?",
      ["«Без фильтра»", "«Все категории»", "«Сбросить»", "Пусто"], 1,
      "«Все категории» — при выборе фильтр отключается.", "Экзамен"),
    q("По каким полям идёт поиск в Задании 3?",
      ["Только по названию", "По наименованию и описанию", "По цене", "По логину"], 1,
      "«Поиск должен осуществляться по наименованию и описанию товара».", "Экзамен"),
    q("Что должно быть в правом верхнем углу после входа?",
      ["Логин", "ФИО", "Роль", "Дата"], 1,
      "ФИО пользователя (фамилия, имя, отчество).", "Экзамен"),
    q("Кто может менять дату заказа и удалять позиции?",
      ["Гость", "Пользователь", "Менеджер", "Администратор"], 3,
      "Редактирование заказа (дата, удаление позиций) — только Администратор.", "Экзамен"),
    q("Что входит в Задание 5?",
      ["Только статистика", "Статистика + руководство пользователя", "Только ER", "Только тесты"], 1,
      "Окно «Статистика заказов» + Руководство_пользователя.docx (1–2 стр., 3+ скриншота).", "Экзамен"),
    q("Сколько показателей должно быть в окне статистики?",
      ["1", "2", "3", "4"], 2,
      "Количество заказов, общая выручка, средний (или максимальный) чек.", "Экзамен"),
    q("Что обязательно должно быть в git-репозитории?",
      ["Только архив", "Исходники папкой + скрипт БД + README.md", "Только exe", "Только скриншоты"], 1,
      "Исходный код структурой файлов (не архив), исполняемые файлы, скрипт БД, README.md, документы.", "Экзамен"),
    q("Стиль именования для Python?",
      ["CamelCase", "snake_case", "UPPER_CASE", "kebab-case"], 1,
      "CamelCase — C#/Java, snake_case — Python, стандарт ИТС — 1С.", "Экзамен"),
    q("Сколько команд допустимо в одной строке?",
      ["Сколько угодно", "Одну", "Две", "Три"], 1, "«Допустимо использование не более одной команды в строке».", "Экзамен"),
    q("Что означает 3НФ?",
      ["Атомарность полей", "Зависимость от всего ключа", "Отсутствие транзитивных зависимостей", "Наличие FK"], 2,
      "3НФ = 2НФ + неключевые атрибуты не зависят от других неключевых.", "БД"),
    q("Что обеспечивает внешний ключ?",
      ["Скорость", "Ссылочную целостность", "Уникальность", "Шифрование"], 1,
      "Нельзя сослаться на несуществующую запись. В SQLite включается PRAGMA foreign_keys=ON.", "БД"),
    q("Как в SQLite включить проверку внешних ключей?",
      ["Всегда включено", "PRAGMA foreign_keys = ON", "SET FK=1", "Невозможно"], 1,
      "По умолчанию выключено — частая потеря баллов.", "БД"),
    q("Как реализовать связь «заказ — товары»?",
      ["Столбцом в orders", "Через order_items", "Через строку с запятыми", "Через JSON"], 1,
      "Одна строка заказа = одна товарная позиция + количество + цена.", "БД"),
    q("Как получить суммарный остаток модели по размерам?",
      ["SUM(quantity) с GROUP BY product_id", "COUNT(*)", "MAX(price)", "AVG(quantity)"], 0,
      "LEFT JOIN product_items + SUM(quantity) + GROUP BY product_id.", "SQL"),
    q("Как посчитать «много/мало» в SQL?",
      ["IF()", "CASE WHEN SUM(quantity) > 5 THEN 'много' ELSE 'мало' END", "ROUND()", "LIKE"], 1,
      "CASE — стандартный способ условного значения.", "SQL"),
    q("Как проверить, что у товара не было заказов в прошлом месяце?",
      ["NOT EXISTS (SELECT 1 FROM orders ...)", "COUNT(*) = 0 в Python", "WHERE price = NULL", "LIKE '%нет%'"], 0,
      "NOT EXISTS + диапазон дат прошлого календарного месяца.", "SQL"),
    q("Как получить первый день прошлого месяца в SQLite?",
      ["date('now','-30 days')", "date('now','start of month','-1 month')", "date('now','-1 month')", "EOMONTH()"], 1,
      "Точная граница месяца — start of month, -1 month.", "SQL"),
    q("Как вычислить итог заказа?",
      ["SUM(quantity * unit_price)", "SUM(price)", "COUNT(*)", "MAX(unit_price)"], 0,
      "Сумма по строкам заказа: количество × цена за единицу.", "SQL"),
    q("Как посчитать средний чек?",
      ["SUM(total) / COUNT(*)", "AVG(price)", "SUM(quantity)", "MAX(total)"], 0,
      "Выручка ÷ количество заказов. Учитывайте деление на ноль.", "SQL"),
    q("Что вернёт lower('КРОССОВКИ') в SQLite?",
      ["'кроссовки'", "'КРОССОВКИ'", "Ошибку", "NULL"], 1,
      "lower() работает только с ASCII; для кириллицы регистр не меняется.", "SQL"),
    q("Как проверить отсутствие картинки?",
      ["image_path = NULL", "image_path IS NULL", "image_path == ''", "NOT image_path"], 1,
      "NULL сравнивается только через IS NULL.", "SQL"),
    q("Что делает LEFT JOIN в списке заказов?",
      ["Убирает заказы без позиций", "Оставляет заказы даже без позиций", "Сортирует", "Удаляет дубли"], 1,
      "LEFT JOIN сохраняет все заказы; у заказа без позиций сумма будет NULL/0.", "SQL"),
    q("Что делает commit()?",
      ["Закрывает окно", "Сохраняет изменения", "Создаёт таблицу", "Удаляет БД"], 1,
      "Без commit() INSERT/UPDATE/DELETE теряются.", "Python"),
    q("Как безопасно передать логин в SQL?",
      ["f-строка", "execute(sql, (login,))", "Конкатенация +", "format()"], 1,
      "Параметризованный запрос защищает от SQL-инъекций.", "Python"),
    q("Как получить id только что созданного заказа в SQLite?",
      ["cursor.lastrowid", "SELECT MAX(id) без условия", "rowcount", "fetchone()[1]"], 0,
      "lastrowid — корректный способ; MAX(id) ломается при параллельных вставках.", "Python"),
    q("Как реагировать на ввод в поле поиска без кнопки?",
      ["trace_add('write', callback)", "after(1000)", "bind('<Return>')", "Кнопка «Найти»"], 0,
      "StringVar.trace_add срабатывает на каждый символ — поиск в реальном времени.", "UI"),
    q("Как подсветить строку в Treeview?",
      ["tags + tag_configure", "font на всё окно", "Canvas", "Нельзя"], 0,
      "tag_configure('low_stock', background='#FFB6B6') и tags=(...).", "UI"),
    q("Как переключать экраны в tkinter?",
      ["Новый Tk() на каждый экран", "frame.tkraise()", "destroy()", "sys.exit()"], 1,
      "Все фреймы в одной ячейке grid, показываем нужный через tkraise().", "UI"),
    q("Как показать ошибку с заголовком и пиктограммой?",
      ["print()", "messagebox.showerror()", "label.config()", "log"], 1,
      "showerror/showwarning/showinfo + askyesno для подтверждений.", "UI"),
    q("Что делать после оформления заказа?",
      ["Ничего", "Списать остаток и обновить каталог", "Закрыть приложение", "Удалить заказ"], 1,
      "Остаток product_items.quantity уменьшается, каталог перезапрашивается.", "Экзамен"),
    q("Что должно быть в Руководстве пользователя?",
      ["Только скриншоты", "Назначение, вход, возможности, 3+ скриншота", "Код программы", "Только титульный лист"], 1,
      "1–2 страницы: назначение, авторизация, основные возможности + скриншоты каталога, заказов, статистики.", "Экзамен"),
    q("Что делать за 5 минут до конца задания?",
      ["Дописывать код", "Сохранить и загрузить файлы в git", "Перезапустить ПК", "Удалить лишнее"], 1,
      "Недосданный файл = 0 баллов за критерий.", "Экзамен"),
]

# ---------------------------------------------------------------------------
# 5. SQL-ПРАКТИКА (новая схема, 19 заданий)
# ---------------------------------------------------------------------------
_FIO = ("u.last_name || ' ' || u.first_name || ' ' || "
        "COALESCE(u.middle_name, '')")

SQL_TASKS = [
    {"id": "s01", "title": "1. Каталог товаров", "level": "лёгкое",
     "task": "Выведите product_id, наименование, категорию, производство и цену всех товаров. Сортировка по product_id.",
     "hint": "JOIN categories c ON p.category_id = c.category_id",
     "expected": "SELECT p.product_id, p.name, c.category_name, p.manufacturer, p.price "
                 "FROM products p JOIN categories c ON p.category_id = c.category_id "
                 "ORDER BY p.product_id;"},
    {"id": "s02", "title": "2. Остаток и «много/мало»", "level": "среднее",
     "task": "Для каждого товара выведите product_id, наименование, суммарный остаток по всем размерам и метку «много» (больше 5) или «мало». Сортировка по product_id.",
     "hint": "LEFT JOIN product_items + SUM(quantity) + CASE WHEN ... > 5",
     "expected": "SELECT p.product_id, p.name, COALESCE(SUM(pi.quantity), 0), "
                 "CASE WHEN COALESCE(SUM(pi.quantity), 0) > 5 THEN 'много' ELSE 'мало' END "
                 "FROM products p LEFT JOIN product_items pi ON pi.product_id = p.product_id "
                 "GROUP BY p.product_id, p.name ORDER BY p.product_id;"},
    {"id": "s03", "title": "3. Подсветка: остаток ≤ 3", "level": "среднее",
     "task": "Выведите product_id и наименование товаров, у которых суммарный остаток меньше или равен 3. Именно их подсвечивают светло-красным.",
     "hint": "GROUP BY + HAVING COALESCE(SUM(pi.quantity), 0) <= 3",
     "expected": "SELECT p.product_id, p.name FROM products p "
                 "LEFT JOIN product_items pi ON pi.product_id = p.product_id "
                 "GROUP BY p.product_id, p.name "
                 "HAVING COALESCE(SUM(pi.quantity), 0) <= 3 ORDER BY p.product_id;"},
    {"id": "s04", "title": "4. Скидка 25%", "level": "сложное",
     "task": "Выведите product_id, наименование и итоговую цену: 25% скидки товарам, по которым не было заказов в прошлом календарном месяце. Округлите до копеек.",
     "hint": "NOT EXISTS + диапазон прошлого месяца + ROUND(price*0.75, 2)",
     "expected": "SELECT p.product_id, p.name, "
                 "ROUND(p.price * CASE WHEN NOT EXISTS ("
                 "SELECT 1 FROM orders o JOIN order_items oi ON oi.order_id = o.order_id "
                 "JOIN product_items pi ON pi.item_id = oi.item_id "
                 "WHERE pi.product_id = p.product_id "
                 "AND o.order_date >= date('now','start of month','-1 month') "
                 "AND o.order_date < date('now','start of month')"
                 ") THEN 0.75 ELSE 1 END, 2) "
                 "FROM products p ORDER BY p.product_id;"},
    {"id": "s05", "title": "5. Поиск по названию и описанию", "level": "среднее",
     "task": "Найдите product_id и наименование товаров, где «Кросс» встречается в названии ИЛИ описании. Помните: lower() в SQLite не работает с кириллицей.",
     "hint": "name LIKE '%Кросс%' OR description LIKE '%Кросс%'",
     "expected": "SELECT p.product_id, p.name FROM products p "
                 "WHERE p.name LIKE '%Кросс%' OR p.description LIKE '%Кросс%' "
                 "ORDER BY p.product_id;"},
    {"id": "s06", "title": "6. Фильтр по категории", "level": "лёгкое",
     "task": "Выведите product_id, наименование и цену товаров категории «Женская». Сортировка по цене по убыванию.",
     "hint": "JOIN categories + WHERE category_name = 'Женская' + ORDER BY price DESC",
     "expected": "SELECT p.product_id, p.name, p.price FROM products p "
                 "JOIN categories c ON p.category_id = c.category_id "
                 "WHERE c.category_name = 'Женская' ORDER BY p.price DESC, p.product_id;"},
    {"id": "s07", "title": "7. Сортировка по цене ↑", "level": "лёгкое",
     "task": "Выведите наименование и цену всех товаров, отсортировав по цене по возрастанию (как пункт «По цене ↑»).",
     "hint": "ORDER BY price ASC, product_id",
     "expected": "SELECT p.name, p.price FROM products p ORDER BY p.price ASC, p.product_id;"},
    {"id": "s08", "title": "8. Список заказов", "level": "среднее",
     "task": "Выведите номер заказа, дату и ФИО клиента. Сортировка по номеру заказа.",
     "hint": "JOIN users u ON u.user_id = o.user_id; ФИО через ||",
     "expected": "SELECT o.order_id, o.order_date, " + _FIO + " FROM orders o "
                 "JOIN users u ON u.user_id = o.user_id ORDER BY o.order_id;"},
    {"id": "s09", "title": "9. Состав заказа №1", "level": "сложное",
     "task": "Для заказа №1 выведите наименование товара, производство, размер, количество, цену за единицу и сумму строки. Сортировка по order_item_id.",
     "hint": "order_items → product_items → products/sizes",
     "expected": "SELECT p.name, p.manufacturer, s.size_value, oi.quantity, oi.unit_price, "
                 "ROUND(oi.quantity * oi.unit_price, 2) FROM order_items oi "
                 "JOIN product_items pi ON pi.item_id = oi.item_id "
                 "JOIN products p ON p.product_id = pi.product_id "
                 "JOIN sizes s ON s.size_id = pi.size_id "
                 "WHERE oi.order_id = 1 ORDER BY oi.order_item_id;"},
    {"id": "s10", "title": "10. Итог по каждому заказу", "level": "сложное",
     "task": "Выведите номер заказа и его итоговую сумму (количество × цена за единицу, сумма по всем строкам). Округлите до копеек.",
     "hint": "SUM(oi.quantity * oi.unit_price) + GROUP BY o.order_id",
     "expected": "SELECT o.order_id, ROUND(COALESCE(SUM(oi.quantity * oi.unit_price), 0), 2) "
                 "FROM orders o LEFT JOIN order_items oi ON oi.order_id = o.order_id "
                 "GROUP BY o.order_id ORDER BY o.order_id;"},
    {"id": "s11", "title": "11. Статистика заказов", "level": "сложное",
     "task": "Выведите 3 показателя: количество заказов, общую выручку и средний чек, округлённый до копеек.",
     "hint": "Подзапрос с итогами по заказам + COUNT/SUM/AVG",
     "expected": "SELECT COUNT(*), COALESCE(SUM(total), 0), "
                 "ROUND(COALESCE(SUM(total), 0) / COUNT(*), 2) FROM ("
                 "SELECT o.order_id, SUM(oi.quantity * oi.unit_price) AS total "
                 "FROM orders o LEFT JOIN order_items oi ON oi.order_id = o.order_id "
                 "GROUP BY o.order_id);"},
    {"id": "s12", "title": "12. Самый дорогой заказ", "level": "среднее",
     "task": "Выведите номер самого дорогого заказа и его сумму. Округлите до копеек.",
     "hint": "ORDER BY total DESC LIMIT 1",
     "expected": "SELECT o.order_id, ROUND(COALESCE(SUM(oi.quantity * oi.unit_price), 0), 2) AS total "
                 "FROM orders o LEFT JOIN order_items oi ON oi.order_id = o.order_id "
                 "GROUP BY o.order_id ORDER BY total DESC, o.order_id LIMIT 1;"},
    {"id": "s13", "title": "13. Товары без заказов", "level": "сложное",
     "task": "Выведите product_id и наименование товаров, которые ни разу не входили ни в один заказ.",
     "hint": "NOT EXISTS (SELECT 1 FROM order_items oi JOIN product_items pi ...)",
     "expected": "SELECT p.product_id, p.name FROM products p WHERE NOT EXISTS ("
                 "SELECT 1 FROM order_items oi JOIN product_items pi ON pi.item_id = oi.item_id "
                 "WHERE pi.product_id = p.product_id) ORDER BY p.product_id;"},
    {"id": "s14", "title": "14. Доступные размеры товара", "level": "среднее",
     "task": "Для товара product_id = 1 выведите размер и количество на складе, только где количество больше 0. Сортировка по размеру.",
     "hint": "JOIN sizes + WHERE product_id = 1 AND quantity > 0",
     "expected": "SELECT s.size_value, pi.quantity FROM product_items pi "
                 "JOIN sizes s ON s.size_id = pi.size_id "
                 "WHERE pi.product_id = 1 AND pi.quantity > 0 ORDER BY s.size_value;"},
    {"id": "s15", "title": "15. Категории и количество товаров", "level": "среднее",
     "task": "Выведите название категории и количество товаров в ней, только для категорий, где товаров больше 3. Сортировка по названию.",
     "hint": "GROUP BY category_name HAVING COUNT(*) > 3",
     "expected": "SELECT c.category_name, COUNT(*) FROM products p "
                 "JOIN categories c ON p.category_id = c.category_id "
                 "GROUP BY c.category_name HAVING COUNT(*) > 3 ORDER BY c.category_name;"},
    {"id": "s16", "title": "16. INSERT: новый пользователь", "level": "среднее",
     "task": "Добавьте пользователя: Новиков Олег Игоревич, логин onovikov, роль «Авторизованный пользователь» (role_id = 3). Пароль не нужен.",
     "hint": "INSERT INTO users (last_name, first_name, middle_name, login, role_id) VALUES (...)",
     "mode": "script",
     "verify": "SELECT login, last_name, role_id FROM users ORDER BY user_id;",
     "expected": "INSERT INTO users (last_name, first_name, middle_name, login, role_id) "
                 "VALUES ('Новиков', 'Олег', 'Игоревич', 'onovikov', 3);"},
    {"id": "s17", "title": "17. INSERT: заказ + строка", "level": "сложное",
     "task": "Создайте заказ для user_id = 4 на текущую дату и добавьте в него 1 пару товарной позиции item_id = 1 по цене 4590.00. Используйте date('now').",
     "hint": "INSERT INTO orders ...; INSERT INTO order_items ...; два запроса через ;",
     "mode": "script",
     "verify": "SELECT o.user_id, oi.item_id, oi.quantity, oi.unit_price "
               "FROM orders o JOIN order_items oi ON oi.order_id = o.order_id "
               "WHERE o.order_id = (SELECT MAX(order_id) FROM orders);",
     "expected": "INSERT INTO orders (order_date, user_id) VALUES (date('now'), 4);\n"
                 "INSERT INTO order_items (order_id, item_id, quantity, unit_price) "
                 "VALUES ((SELECT MAX(order_id) FROM orders), 1, 1, 4590.00);"},
    {"id": "s18", "title": "18. UPDATE: дата заказа", "level": "среднее",
     "task": "Измените дату заказа №1 на 2026-05-15.",
     "hint": "UPDATE orders SET order_date = '2026-05-15' WHERE order_id = 1;",
     "mode": "script",
     "verify": "SELECT order_id, order_date FROM orders ORDER BY order_id;",
     "expected": "UPDATE orders SET order_date = '2026-05-15' WHERE order_id = 1;"},
    {"id": "s19", "title": "19. DELETE: строка заказа", "level": "среднее",
     "task": "Удалите строку заказа с order_item_id = 2.",
     "hint": "DELETE FROM order_items WHERE order_item_id = 2;",
     "mode": "script",
     "verify": "SELECT order_item_id FROM order_items ORDER BY order_item_id;",
     "expected": "DELETE FROM order_items WHERE order_item_id = 2;"},
]

# ---------------------------------------------------------------------------
# 6. КРИТЕРИИ 2027 (100 баллов)
# ---------------------------------------------------------------------------
CRITERIA = [
    ("Задание 1. База данных средствами СУБД — 15", [
        ("8 таблиц, 3НФ, согласованные имена", 5),
        ("PK, FK, CHECK, UNIQUE, ON DELETE", 3),
        ("ER-диаграмма в PDF: таблицы, связи, атрибуты, ключи", 3),
        ("Данные из файлов import загружены", 2),
        ("Скрипт БД с данными (schema.sql) или .dt", 2),
    ]),
    ("Задание 2. Алгоритм и приложение — 10", [
        ("Блок-схема оформления заказа по ГОСТ 19.701-90 (PDF)", 2),
        ("Алгоритм расчёта цены со скидкой 25%", 1),
        ("Название компании, стиль, логотип, иконка, заголовки окон", 2),
        ("Каталог: изображение/заглушка, категория, наименование, производство, состав, цена", 2),
        ("«Много/мало» по суммарному остатку и подсветка ≤3", 1),
        ("Скидка 25% товарам без заказов в прошлом месяце", 1),
        ("Отладка: нет аварийных завершений", 1),
    ]),
    ("Задание 3. Интерфейс и оформление заказа — 25", [
        ("Вход только по логину, гость «Без входа»", 3),
        ("ФИО в правом верхнем углу, выход", 1),
        ("Навигация, «Назад», заголовок каждого окна", 2),
        ("Обработка ошибок, валидация, полезные сообщения, комментарии", 3),
        ("Сортировка по цене ↑↓ через выпадающий список", 2),
        ("Фильтр по категории, «Все категории» первым", 2),
        ("Поиск по наименованию и описанию", 2),
        ("Поиск + фильтр + сортировка в реальном времени совместно", 3),
        ("Карточка товара: все поля, размерный ряд, доступные размеры", 2),
        ("Выбор размера и количества, корзина, подтверждение, дата заказа", 3),
        ("Списание остатка и обновление каталога", 2),
    ]),
    ("Задание 4. Заказы у Администратора и Менеджера — 25", [
        ("Список заказов: дата, ФИО клиента", 4),
        ("Добавление и удаление позиций заказа", 4),
        ("Выбор товара из каталога с поиском по наименованию", 3),
        ("Состав заказа: товар+производство, размер, количество, цена, сумма", 4),
        ("Администратор: изменение даты заказа", 3),
        ("Администратор: удаление позиций", 3),
        ("Обновление списка после изменений", 2),
        ("git-репозиторий и README.md", 2),
    ]),
    ("Задание 5. Статистика и руководство пользователя — 25", [
        ("Кнопка «Статистика» у Менеджера и Администратора", 3),
        ("Таблица всех заказов: номер, дата, ФИО, сумма", 4),
        ("Показатель «количество заказов»", 2),
        ("Показатель «общая выручка»", 2),
        ("Показатель «средний (или максимальный) чек»", 2),
        ("Руководство_пользователя.docx/.pdf: 1–2 стр., 3+ скриншота", 7),
        ("Код, скрипт БД и руководство загружены в git", 5),
    ]),
]

# ---------------------------------------------------------------------------
# 7. ШПАРГАЛКИ
# ---------------------------------------------------------------------------
SNIPPETS = [
    ("Схема БД: 8 таблиц", """CREATE TABLE product_items (
    item_id    INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
    size_id    INTEGER NOT NULL REFERENCES sizes(size_id) ON DELETE RESTRICT,
    quantity   INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    UNIQUE (product_id, size_id)
);
CREATE TABLE orders (
    order_id   INTEGER PRIMARY KEY,
    order_date TEXT NOT NULL,
    user_id    INTEGER NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT
);
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id      INTEGER NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    item_id       INTEGER NOT NULL REFERENCES product_items(item_id) ON DELETE RESTRICT,
    quantity      INTEGER NOT NULL CHECK (quantity > 0),
    unit_price    REAL NOT NULL CHECK (unit_price >= 0)
);
"""),
    ("Вход только по логину", """def find_user(conn, login):
    return conn.execute(
        "SELECT u.user_id, u.last_name, u.first_name, u.middle_name, r.role_name "
        "FROM users u JOIN roles r ON u.role_id = r.role_id "
        "WHERE u.login = ?", (login,)).fetchone()

user = find_user(conn, login_var.get().strip())
if user is None:
    messagebox.showerror("Ошибка авторизации",
        "Пользователь с таким логином не найден. Проверьте раскладку "
        "и выберите логин из списка пользователей.")
else:
    session.user = user
    show_catalog()

# Гость
session.user = None
show_catalog()
"""),
    ("Каталог: остаток, «много/мало», скидка", """SELECT p.product_id, p.name, c.category_name, p.manufacturer,
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
       ) THEN ROUND(p.price * 0.75, 2) ELSE p.price END AS final_price
FROM products p
JOIN categories c ON p.category_id = c.category_id
LEFT JOIN product_items pi ON pi.product_id = p.product_id
WHERE 1 = 1
GROUP BY p.product_id, p.name, c.category_name, p.manufacturer,
         p.composition, p.price, p.image_path
ORDER BY p.price ASC;
"""),
    ("Поиск, фильтр и сортировка вместе", """def load_products(pattern="", category="Все категории", sort="По цене ↑"):
    sql = ("SELECT p.product_id, p.name, c.category_name, p.manufacturer, "
           "p.composition, p.price, p.image_path, "
           "COALESCE(SUM(pi.quantity), 0) AS total_qty "
           "FROM products p "
           "JOIN categories c ON p.category_id = c.category_id "
           "LEFT JOIN product_items pi ON pi.product_id = p.product_id "
           "WHERE 1 = 1")
    params = []
    if pattern:
        sql += " AND (p.name LIKE ? OR p.description LIKE ?)"
        params += [f"%{pattern}%", f"%{pattern}%"]
    if category != "Все категории":
        sql += " AND c.category_name = ?"
        params.append(category)
    sql += " GROUP BY p.product_id, p.name, c.category_name, p.manufacturer, "
    sql += "p.composition, p.price, p.image_path"
    sql += " ORDER BY p.price " + ("DESC" if "↓" in sort else "ASC")
    return conn.execute(sql, params).fetchall()

for var in (search_var, category_var, sort_var):
    var.trace_add("write", lambda *_: refresh())
"""),
    ("Подсветка строк и «много/мало»", """table.tag_configure("low_stock", background="#FFB6B6")
table.tag_configure("discount", foreground="#c0392b")

for row in rows:
    product_id, name, category, manufacturer, composition, price, image, total_qty = row
    tag = "low_stock" if total_qty <= 3 else ""
    label = "много" if total_qty > 5 else "мало"
    price_text = f"{price:.2f}"
    if discount_applies(product_id):
        price_text = f"{price * 0.75:.2f}"
    table.insert("", "end",
                 values=(name, category, manufacturer, composition, price_text, label),
                 tags=(tag,))
"""),
    ("Оформление заказа (транзакция)", """def confirm_order(user_id, cart):
    if not cart:
        messagebox.showwarning("Корзина пуста", "Добавьте хотя бы одну позицию.")
        return
    try:
        conn.execute("BEGIN")
        cur = conn.execute(
            "INSERT INTO orders (order_date, user_id) VALUES (date('now'), ?)",
            (user_id,))
        order_id = cur.lastrowid
        for row in cart:
            # Проверяем остаток ещё раз перед списанием
            left = conn.execute(
                "SELECT quantity FROM product_items WHERE item_id = ?",
                (row["item_id"],)).fetchone()[0]
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
    except Exception as err:
        conn.rollback()
        messagebox.showerror("Заказ не создан",
            f"{err}\\n\\nИсправьте количество и подтвердите заказ снова.")
        return
    messagebox.showinfo("Готово", f"Заказ №{order_id} оформлен.")
"""),
    ("Состав заказа", """SELECT oi.order_id, p.name, p.manufacturer, s.size_value,
       oi.quantity, oi.unit_price,
       ROUND(oi.quantity * oi.unit_price, 2) AS line_total
FROM order_items oi
JOIN product_items pi ON pi.item_id = oi.item_id
JOIN products p ON p.product_id = pi.product_id
JOIN sizes s ON s.size_id = pi.size_id
WHERE oi.order_id = ?
ORDER BY oi.order_item_id;
"""),
    ("Статистика заказов", """SELECT o.order_id, o.order_date,
       u.last_name || ' ' || u.first_name || ' ' || COALESCE(u.middle_name, '') AS client,
       ROUND(COALESCE(SUM(oi.quantity * oi.unit_price), 0), 2) AS total
FROM orders o
JOIN users u ON u.user_id = o.user_id
LEFT JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY o.order_id, o.order_date, u.last_name, u.first_name, u.middle_name
ORDER BY o.order_id;

-- Три показателя
SELECT COUNT(*) AS orders_count,
       COALESCE(SUM(total), 0) AS revenue,
       ROUND(COALESCE(SUM(total), 0) / COUNT(*), 2) AS avg_check
FROM (SELECT o.order_id, SUM(oi.quantity * oi.unit_price) AS total
      FROM orders o LEFT JOIN order_items oi ON oi.order_id = o.order_id
      GROUP BY o.order_id);
"""),
    ("Импорт CSV", """import csv

with open("products.csv", encoding="utf-8", newline="") as f:
    for row in csv.DictReader(f, delimiter=";"):
        category_id = get_or_create_category(row["category_name"])
        conn.execute(
            "INSERT INTO products (category_id, subcategory, name, manufacturer, "
            "description, composition, image_path, price) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (category_id, row["subcategory"], row["name"], row["manufacturer"],
             row["description"], row["composition"],
             row["image_path"] or None, float(row["price"])))
conn.commit()
"""),
    ("Руководство пользователя: структура", """# Руководство пользователя «Чудо Обувь»

## 1. Назначение программы
Система оформления заказов обуви: каталог, корзина, заказы, статистика.

## 2. Вход в систему
Введите логин из списка пользователей (пароль не требуется).
Для просмотра каталога без входа нажмите «Без входа».

## 3. Каталог
Поиск по наименованию и описанию, фильтр по категории,
сортировка по цене, скидка 25%, подсветка низкого остатка.
[Скриншот 1: каталог]

## 4. Оформление заказа
Выберите товар → размер → количество → «В корзину» → «Оформить заказ».
[Скриншот 2: карточка/корзина]

## 5. Работа с заказами (менеджер/администратор)
Список заказов, состав, добавление и удаление позиций.
[Скриншот 3: заказы]

## 6. Статистика
Количество заказов, выручка, средний чек.
[Скриншот 4: статистика]
"""),
]
