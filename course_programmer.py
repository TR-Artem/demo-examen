# -*- coding: utf-8 -*-
"""
Содержание курса под ДЭ, квалификация «Программист» (09.02.07-2),
профильный уровень по КОД 09.02.07-2-2026: 4 модуля, 100 баллов (75 + 25), 4 часа.
Учебная предметная область: продажа обуви (как в образце КОД 2026).
Стек: Python + SQLite + tkinter.

Файл подключается в конце trainer.py и заменяет данные 2026 года.
"""
from __future__ import annotations

MAX_SCORE = 100
COURSE_ID = "programmer"
COURSE_TITLE = "Программист (09.02.07-2)"
COURSE_SUBTITLE = "Python + SQLite + tkinter · 4 модуля"
EXAM_TITLE = "ДЭ 09.02.07-2-2027 «Программист» · профильный уровень"

# ---------------------------------------------------------------------------
# 1. БАЗА ДАННЫХ ПО КОД 09.02.07-2-2026: товары и заказы
# ---------------------------------------------------------------------------
SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE roles (
    role_id   INTEGER PRIMARY KEY,
    role_name TEXT NOT NULL UNIQUE
);

CREATE TABLE users (
    user_id   INTEGER PRIMARY KEY,
    login     TEXT NOT NULL UNIQUE,
    password  TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role_id   INTEGER NOT NULL REFERENCES roles(role_id)
);

CREATE TABLE categories (
    category_id   INTEGER PRIMARY KEY,
    category_name TEXT NOT NULL UNIQUE
);

CREATE TABLE manufacturers (
    manufacturer_id   INTEGER PRIMARY KEY,
    manufacturer_name TEXT NOT NULL UNIQUE
);

CREATE TABLE suppliers (
    supplier_id   INTEGER PRIMARY KEY,
    supplier_name TEXT NOT NULL UNIQUE
);

CREATE TABLE units (
    unit_id   INTEGER PRIMARY KEY,
    unit_name TEXT NOT NULL UNIQUE
);

CREATE TABLE pickup_points (
    point_id INTEGER PRIMARY KEY,
    address  TEXT NOT NULL UNIQUE
);

CREATE TABLE order_statuses (
    status_id   INTEGER PRIMARY KEY,
    status_name TEXT NOT NULL UNIQUE
);

CREATE TABLE products (
    product_id      INTEGER PRIMARY KEY,
    article         TEXT NOT NULL UNIQUE,
    name            TEXT NOT NULL,
    category_id     INTEGER NOT NULL REFERENCES categories(category_id),
    description     TEXT,
    manufacturer_id INTEGER NOT NULL REFERENCES manufacturers(manufacturer_id),
    supplier_id     INTEGER NOT NULL REFERENCES suppliers(supplier_id),
    price           REAL NOT NULL CHECK (price >= 0),
    unit_id         INTEGER NOT NULL REFERENCES units(unit_id),
    quantity        INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    discount        REAL NOT NULL DEFAULT 0 CHECK (discount >= 0 AND discount <= 1),
    image_path      TEXT
);

CREATE TABLE orders (
    order_id   INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    status_id  INTEGER NOT NULL REFERENCES order_statuses(status_id),
    point_id   INTEGER NOT NULL REFERENCES pickup_points(point_id),
    order_date TEXT NOT NULL,
    issue_date TEXT NOT NULL
);

CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_supplier ON products(supplier_id);
CREATE INDEX idx_orders_status ON orders(status_id);

INSERT INTO roles (role_id, role_name) VALUES
    (1, 'Администратор'), (2, 'Менеджер'), (3, 'Авторизованный клиент');

INSERT INTO users (user_id, login, password, full_name, role_id) VALUES
    (1, 'admin', 'admin123', 'Иванов Иван Иванович', 1),
    (2, 'manager', 'manager123', 'Петров Пётр Петрович', 2),
    (3, 'client', 'client123', 'Сидорова Анна Сергеевна', 3),
    (4, 'pavlova', 'pavlova123', 'Павлова Елена Викторовна', 3),
    (5, 'vasileva', 'vasileva123', 'Васильева Ольга Игоревна', 3),
    (6, 'smirnov', 'smirnov123', 'Смирнов Алексей Дмитриевич', 3);

INSERT INTO categories (category_id, category_name) VALUES
    (1, 'Детская обувь'), (2, 'Женская'), (3, 'Мужская');

INSERT INTO manufacturers (manufacturer_id, manufacturer_name) VALUES
    (1, 'Азимут'), (2, 'Марко'), (3, 'Elegance'), (4, 'Nord');

INSERT INTO suppliers (supplier_id, supplier_name) VALUES
    (1, 'ООО «Обувьторг»'), (2, 'ИП Смирнов'), (3, 'ООО «СпортОпт»');

INSERT INTO units (unit_id, unit_name) VALUES
    (1, 'пара'), (2, 'шт');

INSERT INTO pickup_points (point_id, address) VALUES
    (1, 'ул. Ленина, 10'), (2, 'пр. Мира, 25'), (3, 'ул. Садовая, 7');

INSERT INTO order_statuses (status_id, status_name) VALUES
    (1, 'Новая'), (2, 'В обработке'), (3, 'Выполнен'), (4, 'Отменён');

INSERT INTO products
    (product_id, article, name, category_id, description, manufacturer_id,
     supplier_id, price, unit_id, quantity, discount, image_path)
VALUES
    (1, 'SKU-001', 'Кроссовки City Run', 2, 'Кроссовки для города и прогулок.', 1, 1, 4590.0, 1, 7, 0.00, 'img/01.png'),
    (2, 'SKU-002', 'Ботинки Classic', 2, 'Классические женские ботинки.', 2, 1, 7890.0, 1, 2, 0.10, 'img/02.png'),
    (3, 'SKU-003', 'Туфли Office', 2, 'Туфли для офиса и деловых встреч.', 3, 2, 6290.0, 1, 12, 0.20, NULL),
    (4, 'SKU-004', 'Сандалии Summer', 2, 'Лёгкие летние сандалии.', 1, 3, 2990.0, 1, 0, 0.25, 'img/04.png'),
    (5, 'SKU-005', 'Кеды White', 2, 'Белые кеды на каждый день.', 2, 1, 3990.0, 1, 4, 0.00, NULL),
    (6, 'SKU-006', 'Ботинки Winter', 2, 'Утеплённые ботинки с мембраной.', 4, 2, 9490.0, 1, 1, 0.15, 'img/06.png'),
    (7, 'SKU-007', 'Туфли Elegance', 2, 'Вечерние туфли с пряжкой.', 3, 3, 7290.0, 1, 6, 0.20, 'img/07.png'),
    (8, 'SKU-008', 'Кроссовки Trail', 3, 'Кроссовки для треккинга.', 1, 1, 6990.0, 1, 9, 0.25, 'img/08.png'),
    (9, 'SKU-009', 'Ботинки Trekker', 3, 'Туристические ботинки.', 4, 2, 8990.0, 1, 0, 0.00, NULL),
    (10, 'SKU-010', 'Кеды Retro', 3, 'Кеды в ретро-стиле.', 2, 3, 4490.0, 1, 15, 0.00, 'img/10.png'),
    (11, 'SKU-011', 'Туфли Business', 3, 'Мужские туфли для делового стиля.', 3, 1, 8290.0, 1, 3, 0.10, 'img/11.png'),
    (12, 'SKU-012', 'Сандалии Beach', 3, 'Пляжные сандалии.', 1, 2, 3190.0, 1, 8, 0.00, NULL),
    (13, 'SKU-013', 'Кроссовки Marathon', 3, 'Беговые кроссовки с амортизацией.', 1, 3, 9990.0, 1, 5, 0.25, 'img/13.png'),
    (14, 'SKU-014', 'Кроссовки Sun Kids', 1, 'Детские кроссовки с липучками.', 1, 1, 2490.0, 1, 10, 0.00, 'img/14.png'),
    (15, 'SKU-015', 'Ботинки First Step', 1, 'Детские ботинки с тёплой подкладкой.', 4, 2, 3290.0, 1, 2, 0.15, NULL),
    (16, 'SKU-016', 'Кеды School', 1, 'Школьные кеды, легко моются.', 2, 3, 2790.0, 1, 0, 0.00, 'img/16.png');

INSERT INTO orders (order_id, product_id, status_id, point_id, order_date, issue_date) VALUES
    (1, 1, 3, 1, date('now','-40 days'), date('now','-30 days')),
    (2, 2, 2, 2, date('now','-35 days'), date('now','-20 days')),
    (3, 3, 4, 3, date('now','-30 days'), date('now','-25 days')),
    (4, 8, 3, 1, date('now','-25 days'), date('now','-15 days')),
    (5, 10, 1, 2, date('now','-10 days'), date('now','+5 days')),
    (6, 13, 2, 3, date('now','-5 days'), date('now','+10 days')),
    (7, 14, 3, 1, date('now','-20 days'), date('now','-10 days')),
    (8, 5, 4, 2, date('now','-15 days'), date('now','-5 days'));
"""

# ---------------------------------------------------------------------------
# 2. ПЛАН НА 12 НЕДЕЛЬ (60 занятий, 60–90 минут)
# ---------------------------------------------------------------------------
WEEKS = [
    ("Неделя 1. Python и SQLite: база", [
        ("Python: типы и условия", "int/float/str/bool, if/elif/else, ввод и вывод, f-строки.", 70),
        ("Циклы и коллекции", "for/while, list, dict, enumerate, сортировка.", 70),
        ("Функции и исключения", "def, return, try/except, понятные сообщения об ошибках.", 70),
        ("SQLite с Python", "connect, execute, параметры ?, fetchall, commit, lastrowid.", 80),
        ("Мини-каталог", "SELECT товаров из БД и вывод в консоль/таблицу.", 80),
    ]),
    ("Неделя 2. SQL для товаров", [
        ("SELECT, WHERE, ORDER BY", "Выборки, условия, LIKE, NULL, COALESCE, сортировка по остатку.", 80),
        ("JOIN справочников", "categories, manufacturers, suppliers, units — 4 JOIN.", 90),
        ("GROUP BY и агрегаты", "COUNT, SUM, AVG, HAVING, количество по категориям.", 90),
        ("CASE и даты", "CASE, ROUND, date('now'), просроченные заказы.", 90),
        ("SQL-практика 1–8", "Задачи на каталог, скидку, остаток, поиск и фильтр.", 90),
    ]),
    ("Неделя 3. Проектирование БД по КОД 2026", [
        ("Сущности и связи", "Товар, заказ, категория, производитель, поставщик, единица, пункт выдачи.", 80),
        ("Ключи и ограничения", "PK/FK, UNIQUE article, CHECK price/quantity/discount.", 80),
        ("1НФ/2НФ/3НФ", "Справочники отдельно, no транзитивных зависимостей.", 90),
        ("ER-диаграмма 10 таблиц", "draw.io/DBMS, PDF: таблицы, связи, атрибуты, ключи.", 90),
        ("DDL и schema.sql", "CREATE TABLE + INSERT с данными, PRAGMA foreign_keys=ON.", 90),
    ]),
    ("Неделя 4. tkinter: интерфейс", [
        ("Окно и виджеты", "Tk, Frame, Label, Entry, Button, pack/grid, заголовки.", 80),
        ("Treeview", "Таблица товаров: колонки, heading, tags.", 90),
        ("События и поиск", "StringVar, trace_add('write'), поиск в реальном времени.", 90),
        ("Сообщения и валидация", "showerror/showwarning/showinfo, проверка чисел.", 80),
        ("Экраны и роли", "LoginFrame → CatalogFrame → ProductFrame → OrdersFrame.", 90),
    ]),
    ("Неделя 5. Модуль 1: БД", [
        ("Пользователи и роли", "users, roles, вход по логину и паролю.", 80),
        ("Товары и справочники", "products + category/manufacturer/supplier/unit.", 90),
        ("Заказы", "orders: product_id, status, point, order_date, issue_date.", 90),
        ("ER и schema.sql", "10 таблиц, 3НФ, данные import, PDF-диаграмма.", 100),
        ("Пробник Модуля 1", "Таймер 0:50. БД + ER + импорт + скрипт.", 60),
    ]),
    ("Неделя 6. Модуль 2: алгоритм и каталог", [
        ("Блок-схема ГОСТ", "Алгоритм добавления/редактирования товара, PDF.", 80),
        ("Вход и гость", "Логин/пароль из БД или гость; выход на окно входа.", 90),
        ("Список товаров", "Фото/заглушка, все поля, ФИО в правом верхнем углу.", 100),
        ("Цвета строк", "Скидка >15% — #2E8B57; нет на складе — голубой; цена зачёркнута.", 100),
        ("Пробник Модуля 2", "Таймер 0:40. Каталог + docx со скриншотами.", 50),
    ]),
    ("Неделя 7. Модуль 3: поиск и фильтры", [
        ("Поиск по всем полям", "name/description/manufacturer/supplier, регистр в Python.", 90),
        ("Сортировка по остатку", "Выпадающий список: по возрастанию/убыванию.", 80),
        ("Фильтр по поставщику", "«Все поставщики» первым, сброс фильтра.", 90),
        ("Всё вместе в реальном времени", "Поиск + сортировка + фильтр одновременно.", 100),
        ("Валидация и сообщения", "Ошибки с заголовком, пиктограммой и порядком действий.", 80),
    ]),
    ("Неделя 8. Модуль 3: CRUD товара", [
        ("Форма товара", "Все поля, выпадающие списки категории/производителя.", 100),
        ("Добавление и ID", "ID = максимальный + 1, при редактировании только чтение.", 80),
        ("Фото 300×200", "Загрузка, замена, удаление старого файла, путь в БД.", 100),
        ("Удаление товара", "Нельзя удалить товар из заказа; одно окно редактирования.", 90),
        ("Пробник Модуля 3", "Таймер 1:30. Поиск/фильтр + CRUD товара.", 90),
    ]),
    ("Неделя 9. Модуль 4: заказы", [
        ("Список заказов", "Кнопка «Заказы» у менеджера и администратора.", 90),
        ("Форма заказа", "Артикул, статус, пункт выдачи, даты заказа и выдачи.", 100),
        ("CRUD заказа", "Добавление/редактирование/удаление — только администратор.", 100),
        ("Статусы и пункты", "Справочники, выпадающие списки, обновление списка.", 80),
        ("Пробник Модуля 4", "Таймер 1:00. Заказы и форма заказа.", 60),
    ]),
    ("Неделя 10. Интеграция и документы", [
        ("Роли и доступ", "Гость/клиент/менеджер/администратор, проверки прав.", 90),
        ("Git-репозиторий", "Исходники папкой, README, коммиты по модулям.", 80),
        ("Документация", "ER, README, docx со скриншотами корректной работы.", 90),
        ("Полный сценарий", "Вход → каталог → товар → заказ → выход.", 100),
        ("Разбор ошибок", "Чек-лист 100 баллов, слабые места.", 70),
    ]),
    ("Неделя 11. Оптимизация и вариатив", [
        ("Индексы и запросы", "Индексы по category/supplier/status, без N+1.", 90),
        ("Обработка ошибок", "try/except, логирование, rollback.", 80),
        ("Тесты", "unittest: БД, CRUD, проверки.", 90),
        ("Резервная копия", "Копия файла БД, импорт/экспорт CSV.", 80),
        ("Вариативная часть", "Что добавляет колледж: API, отчёты, тесты.", 80),
    ]),
    ("Неделя 12. Пробники и экзамен", [
        ("Пробник №1: Модули 1–2", "Таймер 1:30. БД, ER, импорт, каталог, цвета.", 90),
        ("Разбор ошибок", "Критерии 100 баллов, повтор слабых тем.", 70),
        ("Пробник №2: Модули 1–3", "Таймер 3:00. Плюс поиск, фильтр, CRUD товара.", 180),
        ("Пробник №3: все 4 модуля", "Таймер 4:00. Полный экзамен.", 240),
        ("День экзамена", "Тайминг, git, docx, типичные потери баллов.", 80),
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
    ("l01", "Экзамен", "ДЭ 09.02.07-2: 4 модуля и 100 баллов", 12, """
Ориентир — последний завершённый экзамен: КОД 09.02.07-2-2026 («Программист»),
профильный уровень. Проверено по файлу bom.firpo.ru/file/public/117428 (23.11.2026).

ВРЕМЯ (инвариант ПУ — 4 ч 00 мин)
• Модуль 1. Разработка, администрирование и защита БД — 0 ч 50 мин, 10 баллов.
• Модуль 2. Разработка модулей ПО — 0 ч 40 мин, 15 баллов.
• Модуль 3. Сопровождение и обслуживание ПО — 1 ч 30 мин, 25 баллов.
• Модуль 4. Интеграция программных модулей — 1 ч 00 мин, 25 баллов.
• Вариативная часть — 25 баллов, содержание определяет колледж.

ЧТО ПРОВЕРЯЕТ ОБРАЗЕЦ 2026
• окно входа: логин и пароль из БД или «Гость» (только просмотр товаров);
• роли: гость, авторизованный клиент, менеджер, администратор;
• список товаров: фото (заглушка picture.png), наименование, категория, описание,
  производитель, поставщик, цена, единица измерения, остаток, действующая скидка;
• подсветка: скидка больше 15% — фон #2E8B57; нет на складе — голубой;
  при скидке старая цена зачёркнута красным, итоговая — чёрным;
• поиск по всем текстовым полям, сортировка по остатку ↑↓, фильтр по поставщику
  («Все поставщики» первым) — работают вместе, в реальном времени;
• товар: добавляет и редактирует только администратор; ID = максимальный + 1;
  фото 300×200; нельзя удалить товар, который есть в заказе; одновременно открыто
  не более одного окна редактирования;
• заказы (менеджер видит, администратор добавляет и редактирует): артикул, статус
  (выпадающий список), адрес пункта выдачи, дата заказа, дата выдачи.

ДОКУМЕНТЫ
• Модуль 1 — ER-диаграмма в PDF и скрипт БД;
• Модуль 2 — блок-схема по ГОСТ 19.701-90 и документ docx со скриншотами.

Учебная предметная область — магазин обуви, как в образце КОД 2026.
Образец 2025 года («партнёры», скидка от объёма продаж, расчёт материала) —
другой вариант; в тренажёре не покрыт.
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

def final_price(price: float, discount: float) -> float:
    '''Итоговая цена с учётом действующей скидки товара (Модуль 2).'''
    return round(price * (1 - discount), 2)

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
    ("l05", "БД", "10 таблиц по КОД 09.02.07-2-2026", 12, """
Справочники:
  roles, categories, manufacturers, suppliers, units,
  pickup_points, order_statuses
Основные:
  users (логин, пароль, ФИО, роль)
  products (артикул, наименование, категория, описание, производитель,
            поставщик, цена, единица измерения, количество, скидка, фото)
  orders (товар, статус, пункт выдачи, дата заказа, дата выдачи)

Связи:
  categories 1—M products
  manufacturers 1—M products
  suppliers 1—M products
  units 1—M products
  products 1—M orders
  order_statuses 1—M orders
  pickup_points 1—M orders

Почему так:
• справочники вынесены отдельно — это 3НФ;
• артикул уникален (UNIQUE), ID товара — PK;
• скидка хранится числом 0..1, а не текстом «20%»;
• фото хранится путём, а не BLOB;
• количество — целое неотрицательное.

Вход: users.login + users.password, роль — users.role_id.
"""),
    ("l06", "БД", "3НФ, ключи и ER-диаграмма", 10, """
1НФ — атомарные значения, нет повторяющихся групп.
  Плохо: suppliers = 'ООО 1, ИП 2' в одной ячейке.
  Хорошо: таблица suppliers + supplier_id в products.

2НФ — неключевой атрибут зависит от всего ключа.
  В orders ключ order_id, остальные поля зависят только от него.

3НФ — нет транзитивных зависимостей.
  Плохо: products(..., category_name, manufacturer_name, supplier_name).
  Хорошо: category_id, manufacturer_id, supplier_id + справочники.

ER-диаграмма (PDF):
• 10 таблиц и все атрибуты;
• PK и FK;
• связи 1:M со стороны «один»;
• согласованные имена (snake_case, *_id);
• отдельно подписаны справочники.

Ограничения:
• products.article UNIQUE;
• CHECK(price >= 0), CHECK(quantity >= 0);
• CHECK(discount BETWEEN 0 AND 1);
• FK на справочники.

Инструменты: draw.io, DBeaver, dbdiagram.io, SSMS. Интернет на экзамене
ограничен — ставь draw.io desktop заранее.
"""),
    ("l07", "Документы", "Блок-схема по ГОСТ 19.701-90", 10, """
Модуль 2: «Сформировать алгоритм разработки приложения, оформить в виде
блок-схемы по ГОСТ 19.701-90, PDF».

Символы: овал — начало/конец; прямоугольник — процесс; ромб — решение
(«Да»/«Нет»); параллелограмм — ввод/вывод; стрелки — поток.

Алгоритм добавления/редактирования товара:
Начало → Открыть форму товара
  → Ввод полей (наименование, категория, производитель, поставщик,
     цена, единица, количество, скидка, фото)
  → Проверить обязательные поля?
     Нет → Сообщение об ошибке → вернуться к вводу
     Да → Проверить цену ≥ 0 и количество ≥ 0?
        Нет → Сообщение → вернуться к вводу
        Да → Редактирование или добавление?
           Редактирование → UPDATE products
           Добавление → ID = MAX(product_id)+1 → INSERT products
  → Сохранить фото 300×200 (если выбрано)
  → Обновить список товаров → Конец

Алгоритм входа:
Начало → Ввод логина и пароля → Найти в users
  → Не найден: сообщение → повтор
  → Найден: открыть каталог по роли
  → «Гость»: каталог без фильтров → Конец

Ошибки: нет «Начало/Конец», ромб без «Да/Нет», не PDF, алгоритм не про
товар или вход.
"""),
    ("l08", "SQL", "SELECT, WHERE, ORDER BY, LIKE", 10, """
SELECT p.product_id, p.article, p.name, c.category_name, p.price, p.quantity
FROM products p
JOIN categories c ON c.category_id = p.category_id
WHERE p.price > 3000
ORDER BY p.quantity ASC, p.product_id;

Поиск по всем текстовым полям:
SELECT p.product_id, p.name
FROM products p
JOIN manufacturers m ON m.manufacturer_id = p.manufacturer_id
JOIN suppliers s ON s.supplier_id = p.supplier_id
WHERE p.name LIKE '%Кросс%'
   OR p.description LIKE '%Кросс%'
   OR m.manufacturer_name LIKE '%Кросс%'
   OR s.supplier_name LIKE '%Кросс%';

Скидка больше 15%:
SELECT product_id, name, discount FROM products WHERE discount > 0.15;

Нет на складе:
SELECT product_id, name FROM products WHERE quantity = 0;

NULL: image_path IS NULL → в приложении показать picture.png.

Сортировка по остатку: ORDER BY quantity ASC / DESC — выпадающий список.
Фильтр по поставщику: WHERE s.supplier_name = ? (первый пункт «Все поставщики»).

lower() в SQLite не понижает регистр кириллицы — поиск без учёта регистра
делайте в Python: 'кросс' in text.lower().
"""),
    ("l09", "SQL", "JOIN, GROUP BY, CASE, даты", 12, """
-- Заказы с расшифровкой
SELECT o.order_id, p.article, st.status_name, pp.address,
       o.order_date, o.issue_date
FROM orders o
JOIN products p ON p.product_id = o.product_id
JOIN order_statuses st ON st.status_id = o.status_id
JOIN pickup_points pp ON pp.point_id = o.point_id
ORDER BY o.order_id;

-- Количество заказов по статусам
SELECT st.status_name, COUNT(o.order_id)
FROM order_statuses st
LEFT JOIN orders o ON o.status_id = st.status_id
GROUP BY st.status_id, st.status_name;

-- Средняя цена по категориям
SELECT c.category_name, ROUND(AVG(p.price), 2)
FROM products p
JOIN categories c ON c.category_id = p.category_id
GROUP BY c.category_name;

-- CASE: размер скидки
SELECT product_id, name,
       CASE WHEN discount > 0.15 THEN 'большая скидка' ELSE 'обычная' END
FROM products;

-- Просроченные заказы
SELECT o.order_id, p.article
FROM orders o
JOIN products p ON p.product_id = o.product_id
JOIN order_statuses st ON st.status_id = o.status_id
WHERE o.issue_date < date('now') AND st.status_name <> 'Выполнен';

-- Итоговая цена
SELECT product_id, name, price, ROUND(price * (1 - discount), 2)
FROM products;
"""),
    ("l10", "SQL", "DDL, INSERT/UPDATE/DELETE, скрипт БД", 10, """
CREATE TABLE products (
    product_id      INTEGER PRIMARY KEY,
    article         TEXT NOT NULL UNIQUE,
    name            TEXT NOT NULL,
    category_id     INTEGER NOT NULL REFERENCES categories(category_id),
    description     TEXT,
    manufacturer_id INTEGER NOT NULL REFERENCES manufacturers(manufacturer_id),
    supplier_id     INTEGER NOT NULL REFERENCES suppliers(supplier_id),
    price           REAL NOT NULL CHECK (price >= 0),
    unit_id         INTEGER NOT NULL REFERENCES units(unit_id),
    quantity        INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    discount        REAL NOT NULL DEFAULT 0 CHECK (discount >= 0 AND discount <= 1),
    image_path      TEXT
);

INSERT INTO products (article, name, category_id, description,
    manufacturer_id, supplier_id, price, unit_id, quantity, discount, image_path)
VALUES ('SKU-017', 'Кроссовки New', 2, 'Новая модель', 1, 1, 5990, 1, 5, 0, NULL);

UPDATE products SET price = price + 500 WHERE product_id = 1;

DELETE FROM products WHERE product_id = 4;

Правила:
• PRAGMA foreign_keys = ON — в SQLite по умолчанию ВЫКЛЮЧЕНО;
• после INSERT/UPDATE/DELETE — commit();
• скрипт БД сдаётся С ДАННЫМИ: DDL + INSERT + ограничения;
• ID нового товара: MAX(product_id) + 1 (по КОД 2026);
• удалять товар, который есть в заказе, нельзя.

Динамические даты:
INSERT INTO orders (product_id, status_id, point_id, order_date, issue_date)
VALUES (1, 1, 1, date('now'), date('now', '+7 days'));
"""),
    ("l11", "Python", "Python + SQLite: рабочий каркас", 12, """
import sqlite3
from pathlib import Path

DB = Path(__file__).with_name('shop.db')
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
conn.execute('PRAGMA foreign_keys = ON')

# Список товаров
rows = conn.execute('''
    SELECT p.product_id, p.article, p.name, c.category_name,
           p.price, p.quantity, p.discount
    FROM products p
    JOIN categories c ON c.category_id = p.category_id
    ORDER BY p.product_id
''').fetchall()
for row in rows:
    print(row['article'], row['name'], row['price'])

# Вход
user = conn.execute(
    'SELECT user_id, full_name FROM users WHERE login = ? AND password = ?',
    (login, password)).fetchone()
if user is None:
    print('Неверный логин или пароль')

# Добавление товара с ID = max + 1
next_id = conn.execute(
    'SELECT COALESCE(MAX(product_id), 0) + 1 FROM products').fetchone()[0]
conn.execute(
    'INSERT INTO products (product_id, article, name, category_id, description, '
    'manufacturer_id, supplier_id, price, unit_id, quantity, discount, image_path) '
    'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
    (next_id, 'SKU-017', 'Кроссовки New', 2, 'Новая модель', 1, 1,
     5990, 1, 5, 0, None))
conn.commit()

# Заказ
conn.execute(
    'INSERT INTO orders (product_id, status_id, point_id, order_date, issue_date) '
    'VALUES (?, ?, ?, date("now"), date("now", "+7 days"))',
    (product_id, status_id, point_id))
conn.commit()

Ошибки — try/except sqlite3.Error, затем rollback(). После изменений
перезапрашивайте SELECT и обновляйте таблицу.
"""),
    ("l12", "UI", "tkinter: каталог, поиск, цвета", 12, """
root = tk.Tk()
root.title('Магазин обуви — каталог')

search_var = tk.StringVar()
supplier_var = tk.StringVar(value='Все поставщики')
sort_var = tk.StringVar(value='По остатку ↑')
ttk.Entry(parent, textvariable=search_var).pack(fill='x')
search_var.trace_add('write', lambda *_: refresh())

table = ttk.Treeview(parent,
    columns=('article', 'name', 'supplier', 'price', 'stock', 'discount'),
    show='headings')
for col, title in zip(('article', 'name', 'supplier', 'price', 'stock', 'discount'),
                      ('Артикул', 'Наименование', 'Поставщик',
                       'Цена', 'Остаток', 'Скидка')):
    table.heading(col, text=title)
table.pack(fill='both', expand=True)

table.tag_configure('out_of_stock', background='#B3E5FC')   # голубой
table.tag_configure('big_discount', background='#2E8B57')   # > 15%
table.tag_configure('old_price', foreground='#c0392b')

def refresh():
    table.delete(*table.get_children())
    for row in load_products(search_var.get(), supplier_var.get(), sort_var.get()):
        tag = 'out_of_stock' if row['quantity'] == 0 else (
              'big_discount' if row['discount'] > 0.15 else '')
        final = row['price'] * (1 - row['discount'])
        price_text = (f"{row['price']:.2f}" if row['discount'] == 0
                      else f"{row['price']:.2f} → {final:.2f}")
        table.insert('', 'end', values=(row['article'], row['name'],
            row['supplier'], price_text, row['quantity'],
            f"{row['discount']*100:.0f}%"), tags=(tag,))

Экраны: LoginFrame, CatalogFrame, ProductFrame, OrdersFrame.
ФИО — в правом верхнем углу. «Назад» — на каждом экране.
"""),
    ("l13", "Экзамен", "Модули 1–2: БД, алгоритм, список товаров", 12, """
МОДУЛЬ 1 (0 ч 50 мин, 10 баллов)
• 3НФ, PK/FK, согласованные имена, ссылочная целостность;
• ER-диаграмма в PDF: таблицы, связи, атрибуты, ключи;
• скрипт БД (schema.sql) и данные из файлов с пометкой import;
• база подключена к приложению.

МОДУЛЬ 2 (0 ч 40 мин, 15 баллов)
• блок-схема алгоритма по ГОСТ 19.701-90 (PDF);
• окно входа: логин и пароль из БД или «Гость»; выход на окно входа;
• ФИО пользователя в правом верхнем углу;
• список товаров из БД: все поля, заглушка picture.png;
• подсветка: скидка больше 15% — #2E8B57; нет на складе — голубой;
  зачёркнутая цена красным и итоговая чёрным;
• отладка без аварийных завершений; docx со скриншотами.
"""),

    ("l14", "Экзамен", "Модули 3–4: CRUD, поиск, заказы", 12, """
МОДУЛЬ 3 (1 ч 30 мин, 25 баллов)
• кнопка «Назад» и заголовок каждого окна;
• сообщения об ошибках: заголовок, пиктограмма, что сделать дальше;
• поиск по всем текстовым полям, сортировка по остатку ↑↓, фильтр по поставщику —
  в реальном времени и вместе;
• форма товара: открывается по нажатию элемента (редактирование) и по «Добавить товар»;
• цена и остаток не отрицательные, сотые допустимы; фото 300×200;
• удаление товара; запрет удаления товара из заказа; один открытый редактор;
• после изменений список обновляется.

МОДУЛЬ 4 (1 ч 00 мин, 25 баллов)
• кнопка «Заказы» у менеджера и администратора; список заказов;
• форма заказа: артикул, статус (список), адрес пункта выдачи, даты заказа и выдачи;
• добавление и редактирование заказа — только администратор;
• удаление заказа администратором; список обновляется.

ГИТ: исходники папкой, README, коммиты в начале и конце каждого модуля.
"""),

    ("l15", "Экзамен", "Стратегия: 4 модуля и 90+ баллов", 10, """
ЦЕЛЬ «5»: 90+ из 100. Нельзя потерять модуль: 25 баллов у модулей 3 и 4.

ПОРЯДОК РАБОТЫ
1. Коммит «start» в первые 2 минуты.
2. Модуль 1: схема, ER (PDF), импорт, подключение БД — 0 ч 50 мин.
3. Модуль 2: вход/гость, список товаров с подсветкой — 0 ч 40 мин.
4. Модуль 3: поиск + сортировка + фильтр, форма товара, удаление — 1 ч 30 мин.
5. Модуль 4: заказы и форма заказа — 1 ч 00 мин.
6. Коммит и push в конце каждого модуля.

ЧАСТЫЕ ПОТЕРИ БАЛЛОВ
• цвета не по образцу (#2E8B57 при скидке больше 15%, голубой без остатка);
• фильтр по поставщику без пункта «Все поставщики» первым;
• поиск по одному полю вместо всех текстовых;
• можно открыть два окна редактирования товара;
• удаление товара, который есть в заказе;
• нет docx со скриншотами (Модуль 2);
• ID товара при добавлении не +1 к максимальному.
"""),
]

# ---------------------------------------------------------------------------
# 4. ТЕСТЫ
# ---------------------------------------------------------------------------
def q(text, opts, ans, expl, topic):
    return {"q": text, "opts": opts, "ans": ans, "explain": expl, "topic": topic}


QUIZ = [
    q("Сколько модулей на ДЭ профильного уровня по КОД 2026?",
      ["3", "4", "5", "6"], 1,
      "Четыре модуля: БД, разработка модулей, сопровождение, интеграция.", "Экзамен"),
    q("Сколько времени на инвариантную часть ПУ по КОД 2026?",
      ["3 ч", "4 ч", "5 ч", "1 ч 30 мин"], 1,
      "50 + 40 + 90 + 60 минут = 240 минут = 4 часа.", "Экзамен"),
    q("Сколько баллов даёт Модуль 1 (БД) в инварианте?",
      ["10", "15", "25", "30"], 0,
      "Модуль 1: 6 баллов (разработка объектов БД) + 4 (реализация в СУБД) = 10.", "Экзамен"),
    q("Какое требование к БД обязательно по КОД 2026?",
      ["Только одна таблица", "3 нормальная форма и ссылочная целостность", "Без ключей", "Только CSV-файлы"], 1,
      "В образце: «Обязательна 3 нормальная форма с обеспечением ссылочной целостности».", "Экзамен"),
    q("Что видит пользователь при запуске приложения по КОД 2026?",
      ["Главный экран", "Окно входа: логин и пароль из БД или переход в роли гостя", "Список заказов", "Статистику"], 1,
      "Первое окно — вход; гость видит только список товаров без фильтров.", "Экзамен"),
    q("Что такое «действующая скидка» товара по КОД 2026?",
      ["Скидка за количество заказов", "Поле товара: процент скидки, влияющий на цвет строки и итоговую цену", "Скидка на весь заказ", "Действующая скидка без заказов"], 1,
      "Поле «действующая скидка» есть в списке товаров и в форме товара.", "Экзамен"),
    q("Какой фон у строки товара при скидке больше 15%?",
      ["#2E8B57", "#FFB6B6", "#0000FF", "#FFFFFF"], 0,
      "По образцу КОД 2026: #2E8B57. Нет на складе — голубой цвет.", "Экзамен"),
    q("Каким цветом выделяется товар, которого нет на складе?",
      ["Зелёным", "Красным", "Голубым", "Жёлтым"], 2,
      "По образцу КОД 2026: голубой.", "Экзамен"),
    q("Какие поля обязательны в форме товара по КОД 2026?",
      ["Только наименование и цена", "Артикул, наименование, категория, описание, производитель, поставщик, цена, единица измерения, количество, скидка", "Только фото и остаток", "Только артикул"], 1,
      "Форма товара содержит все перечисленные поля, плюс фото (или заглушка).", "Экзамен"),
    q("Какие поля обязательны в форме заказа по КОД 2026?",
      ["Только артикул", "Артикул, статус, адрес пункта выдачи, дата заказа, дата выдачи", "Товар, размер, количество, цена", "Только даты"], 1,
      "Форма заказа: артикул, статус (список), пункт выдачи, дата заказа, дата выдачи.", "Экзамен"),
    q("По каким полям ведётся поиск товаров (менеджер и администратор)?",
      ["Только по наименованию", "По всем текстовым полям одновременно", "Только по цене", "Только по ID"], 1,
      "Образец: «Поиск должен осуществляться по всем доступным данным с текстовым типом данных».", "Экзамен"),
    q("Что должно быть в правом верхнем углу после входа?",
      ["Логин", "ФИО", "Роль", "Дата"], 1,
      "ФИО пользователя (фамилия, имя, отчество).", "Экзамен"),
    q("Кто может добавлять, редактировать и удалять заказы?",
      ["Гость", "Авторизованный клиент", "Менеджер", "Администратор"], 3,
      "Добавлять и редактировать заказы может только администратор.", "Экзамен"),
    q("Что нужно сдать по Модулю 2 (кроме кода)?",
      ["Ничего", "Документ docx со скриншотами корректной работы системы", "Видео", "Только блок-схему"], 1,
      "Модуль 2 образца: «Создайте документ docx и вложите туда скриншоты».", "Экзамен"),
    q("Кто может добавлять и редактировать товары по КОД 2026?",
      ["Гость", "Авторизованный клиент", "Менеджер", "Администратор"], 3,
      "Добавлять и редактировать товары может только администратор.", "Экзамен"),
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
    q("Какое поле связывает заказ с товаром в образце КОД 2026?",
      ["Артикул", "Размер", "Строка заказа order_items", "Категория"], 0,
      "В форме заказа указывается артикул товара; отдельной таблицы строк заказа в образце нет.", "БД"),
    q("Как вывести товары, которых нет на складе?",
      ["WHERE quantity = 0", "WHERE discount > 0.15", "HAVING COUNT(*) = 0", "WHERE price IS NULL"], 0,
      "Остаток хранится в products.quantity; нет на складе — quantity = 0.", "SQL"),
    q("Что должно быть первым пунктом фильтра по поставщику?",
      ["Первый поставщик по алфавиту", "«Все поставщики»", "Пустая строка", "«Сбросить»"], 1,
      "Первым идёт «Все поставщики»: при выборе фильтр сбрасывается.", "Экзамен"),
    q("Как вычисляется ID нового товара по КОД 2026?",
      ["Вручную", "Максимальный ID в БД + 1", "Случайное число", "UUID"], 1,
      "ID при добавлении не отображается и вычисляется как +1 к имеющемуся в БД.", "Экзамен"),
    q("Как вычислить итоговую цену при скидке 20%?",
      ["price * 0.2", "price * (1 - 0.2)", "price - 0.2", "price / 0.2"], 1,
      "Итог = цена × (1 − скидка).", "Экзамен"),
    q("Как вывести товары со скидкой больше 15%?",
      ["WHERE discount > 0.15", "WHERE discount < 15", "WHERE price > 0.15", "WHERE quantity = 15"], 0,
      "Скидка хранится долей 0..1, поэтому 15% — это 0.15.", "SQL"),
    q("Как сортируется список товаров по остатку?",
      ["По возрастанию и по убыванию", "Только по возрастанию", "Не сортируется", "По дате"], 0,
      "Сортировка по количеству на складе: ↑ и ↓.", "Экзамен"),
    q("Что вернёт lower('КРОССОВКИ') в SQLite?",
      ["'кроссовки'", "'КРОССОВКИ'", "Ошибку", "NULL"], 1,
      "lower() работает только с ASCII; для кириллицы регистр не меняется.", "SQL"),
    q("Как проверить отсутствие картинки?",
      ["image_path = NULL", "image_path IS NULL", "image_path == ''", "NOT image_path"], 1,
      "NULL сравнивается только через IS NULL.", "SQL"),
    q("Что делает LEFT JOIN?",
      ["Оставляет только совпадения", "Оставляет все строки левой таблицы и совпадения правой", "Удаляет дубли", "Сортирует результат"], 1,
      "LEFT JOIN сохраняет все строки левой таблицы; справа могут быть NULL.", "SQL"),
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
    q("Что должно происходить после добавления, редактирования или удаления товара/заказа?",
      ["Ничего", "Список на экране обновляется", "Приложение закрывается", "Удаляется БД"], 1,
      "После изменений данные в списке должны быть обновлены.", "Экзамен"),
    q("Какой элемент обязателен в интерфейсе окна товара, если товар в заказе?",
      ["Кнопка «Удалить» активна", "Удаление запрещено", "Заказ удаляется вместе с товаром", "Цена обнуляется"], 1,
      "Товар, который присутствует в заказе, удалить нельзя.", "Экзамен"),
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
     "task": "Выведите product_id, артикул, наименование, категорию, производителя, поставщика, цену, единицу измерения, остаток и скидку. Сортировка по product_id.",
     "hint": "4 JOIN: categories, manufacturers, suppliers, units",
     "expected": "SELECT p.product_id, p.article, p.name, c.category_name, m.manufacturer_name, "
                 "s.supplier_name, p.price, u.unit_name, p.quantity, p.discount "
                 "FROM products p "
                 "JOIN categories c ON c.category_id = p.category_id "
                 "JOIN manufacturers m ON m.manufacturer_id = p.manufacturer_id "
                 "JOIN suppliers s ON s.supplier_id = p.supplier_id "
                 "JOIN units u ON u.unit_id = p.unit_id ORDER BY p.product_id;"},
    {"id": "s02", "title": "2. Скидка больше 15%", "level": "лёгкое",
     "task": "Выведите product_id, наименование и скидку в процентах для товаров со скидкой больше 15%. Такие строки выделяются фоном #2E8B57. Сортировка по product_id.",
     "hint": "WHERE discount > 0.15; проценты: ROUND(discount * 100)",
     "expected": "SELECT product_id, name, ROUND(discount * 100) FROM products "
                 "WHERE discount > 0.15 ORDER BY product_id;"},
    {"id": "s03", "title": "3. Нет на складе", "level": "лёгкое",
     "task": "Выведите product_id и наименование товаров, у которых quantity = 0. Такие строки выделяются голубым цветом. Сортировка по product_id.",
     "hint": "WHERE quantity = 0",
     "expected": "SELECT product_id, name FROM products WHERE quantity = 0 ORDER BY product_id;"},
    {"id": "s04", "title": "4. Итоговая цена со скидкой", "level": "среднее",
     "task": "Выведите product_id, наименование, цену и итоговую цену с учётом скидки (округлите до копеек). Сортировка по product_id.",
     "hint": "ROUND(price * (1 - discount), 2)",
     "expected": "SELECT product_id, name, price, ROUND(price * (1 - discount), 2) "
                 "FROM products ORDER BY product_id;"},
    {"id": "s05", "title": "5. Поиск по всем текстовым полям", "level": "среднее",
     "task": "Найдите товары, где «Кросс» встречается в наименовании, описании, производителе или поставщике. Выведите product_id и наименование. Сортировка по product_id.",
     "hint": "name/description/manufacturer_name/supplier_name LIKE '%Кросс%'",
     "expected": "SELECT p.product_id, p.name FROM products p "
                 "JOIN manufacturers m ON m.manufacturer_id = p.manufacturer_id "
                 "JOIN suppliers s ON s.supplier_id = p.supplier_id "
                 "WHERE p.name LIKE '%Кросс%' OR p.description LIKE '%Кросс%' "
                 "OR m.manufacturer_name LIKE '%Кросс%' OR s.supplier_name LIKE '%Кросс%' "
                 "ORDER BY p.product_id;"},
    {"id": "s06", "title": "6. Фильтр по поставщику", "level": "лёгкое",
     "task": "Выведите product_id, наименование и цену товаров поставщика «ООО «Обувьторг»». Сортировка по product_id.",
     "hint": "JOIN suppliers + WHERE supplier_name = 'ООО «Обувьторг»'",
     "expected": "SELECT p.product_id, p.name, p.price FROM products p "
                 "JOIN suppliers s ON s.supplier_id = p.supplier_id "
                 "WHERE s.supplier_name = 'ООО «Обувьторг»' ORDER BY p.product_id;"},
    {"id": "s07", "title": "7. Сортировка по остатку ↑", "level": "лёгкое",
     "task": "Выведите наименование и остаток всех товаров, отсортировав по остатку по возрастанию.",
     "hint": "ORDER BY quantity ASC, product_id",
     "expected": "SELECT name, quantity FROM products ORDER BY quantity ASC, product_id;"},
    {"id": "s08", "title": "8. Сортировка по остатку ↓", "level": "лёгкое",
     "task": "Выведите наименование и остаток всех товаров, отсортировав по остатку по убыванию.",
     "hint": "ORDER BY quantity DESC, product_id",
     "expected": "SELECT name, quantity FROM products ORDER BY quantity DESC, product_id;"},
    {"id": "s09", "title": "9. Список заказов", "level": "среднее",
     "task": "Выведите order_id, артикул товара, статус, адрес пункта выдачи, дату заказа и дату выдачи. Сортировка по order_id.",
     "hint": "JOIN products, order_statuses, pickup_points",
     "expected": "SELECT o.order_id, p.article, st.status_name, pp.address, "
                 "o.order_date, o.issue_date FROM orders o "
                 "JOIN products p ON p.product_id = o.product_id "
                 "JOIN order_statuses st ON st.status_id = o.status_id "
                 "JOIN pickup_points pp ON pp.point_id = o.point_id ORDER BY o.order_id;"},
    {"id": "s10", "title": "10. Выполненные заказы", "level": "среднее",
     "task": "Выведите order_id, артикул и дату выдачи только для заказов со статусом «Выполнен». Сортировка по order_id.",
     "hint": "JOIN order_statuses + WHERE status_name = 'Выполнен'",
     "expected": "SELECT o.order_id, p.article, o.issue_date FROM orders o "
                 "JOIN products p ON p.product_id = o.product_id "
                 "JOIN order_statuses st ON st.status_id = o.status_id "
                 "WHERE st.status_name = 'Выполнен' ORDER BY o.order_id;"},
    {"id": "s11", "title": "11. Заказы по статусам", "level": "среднее",
     "task": "Посчитайте количество заказов в каждом статусе. Выведите status_id, название статуса и количество. Сортировка по status_id.",
     "hint": "LEFT JOIN orders + GROUP BY + COUNT",
     "expected": "SELECT st.status_id, st.status_name, COUNT(o.order_id) "
                 "FROM order_statuses st LEFT JOIN orders o ON o.status_id = st.status_id "
                 "GROUP BY st.status_id, st.status_name ORDER BY st.status_id;"},
    {"id": "s12", "title": "12. Товары дороже 8000", "level": "лёгкое",
     "task": "Выведите product_id, наименование и цену товаров дороже 8000. Сортировка по цене по убыванию, затем по product_id.",
     "hint": "WHERE price > 8000 ORDER BY price DESC",
     "expected": "SELECT product_id, name, price FROM products WHERE price > 8000 "
                 "ORDER BY price DESC, product_id;"},
    {"id": "s13", "title": "13. Товары без фото", "level": "лёгкое",
     "task": "Выведите product_id и наименование товаров, у которых нет изображения (image_path IS NULL). Для них в приложении выводится заглушка picture.png. Сортировка по product_id.",
     "hint": "WHERE image_path IS NULL",
     "expected": "SELECT product_id, name FROM products WHERE image_path IS NULL ORDER BY product_id;"},
    {"id": "s14", "title": "14. Количество товаров по категориям", "level": "среднее",
     "task": "Выведите название категории и количество товаров в ней. Сортировка по названию.",
     "hint": "JOIN categories + GROUP BY + COUNT",
     "expected": "SELECT c.category_name, COUNT(*) FROM products p "
                 "JOIN categories c ON c.category_id = p.category_id "
                 "GROUP BY c.category_name ORDER BY c.category_name;"},
    {"id": "s15", "title": "15. Средняя цена по категориям", "level": "среднее",
     "task": "Выведите название категории и среднюю цену товаров (округлите до 2 знаков). Сортировка по средней цене по убыванию.",
     "hint": "ROUND(AVG(price), 2) + GROUP BY",
     "expected": "SELECT c.category_name, ROUND(AVG(p.price), 2) AS avg_price "
                 "FROM products p JOIN categories c ON c.category_id = p.category_id "
                 "GROUP BY c.category_name ORDER BY avg_price DESC, c.category_name;"},
    {"id": "s16", "title": "16. INSERT: новый товар", "level": "сложное",
     "task": "Добавьте товар: артикул SKU-017, «Кроссовки New», категория 2, описание «Новая модель», производитель 1, поставщик 1, цена 5990, единица 1, остаток 5, скидка 0, без фото.",
     "hint": "INSERT INTO products (article, name, category_id, description, manufacturer_id, supplier_id, price, unit_id, quantity, discount, image_path) VALUES (...)",
     "mode": "script",
     "verify": "SELECT article, name, price, quantity FROM products ORDER BY product_id;",
     "expected": "INSERT INTO products (article, name, category_id, description, manufacturer_id, supplier_id, price, unit_id, quantity, discount, image_path) VALUES ('SKU-017', 'Кроссовки New', 2, 'Новая модель', 1, 1, 5990, 1, 5, 0, NULL);"},
    {"id": "s17", "title": "17. UPDATE: цена товара", "level": "среднее",
     "task": "Увеличьте цену товара product_id = 1 на 500 рублей.",
     "hint": "UPDATE products SET price = price + 500 WHERE product_id = 1;",
     "mode": "script",
     "verify": "SELECT product_id, price FROM products ORDER BY product_id;",
     "expected": "UPDATE products SET price = price + 500 WHERE product_id = 1;"},
    {"id": "s18", "title": "18. DELETE: товар без заказов", "level": "сложное",
     "task": "Удалите товар product_id = 4. Он не входит ни в один заказ, поэтому удаление разрешено.",
     "hint": "DELETE FROM products WHERE product_id = 4;",
     "mode": "script",
     "verify": "SELECT product_id FROM products ORDER BY product_id;",
     "expected": "DELETE FROM products WHERE product_id = 4;"},
    {"id": "s19", "title": "19. Просроченные заказы", "level": "сложное",
     "task": "Выведите order_id, артикул и дату выдачи для заказов, у которых дата выдачи уже прошла, а статус не «Выполнен». Сортировка по дате выдачи.",
     "hint": "WHERE issue_date < date('now') AND status_name <> 'Выполнен'",
     "expected": "SELECT o.order_id, p.article, o.issue_date FROM orders o "
                 "JOIN products p ON p.product_id = o.product_id "
                 "JOIN order_statuses st ON st.status_id = o.status_id "
                 "WHERE o.issue_date < date('now') AND st.status_name <> 'Выполнен' "
                 "ORDER BY o.issue_date, o.order_id;"},
]

# ---------------------------------------------------------------------------
# 6. КРИТЕРИИ 2027 (100 баллов)
# ---------------------------------------------------------------------------
CRITERIA = [
    ("Модуль 1. Разработка объектов базы данных в соответствии с результатами анализа предметной области — 6", [
        ("3НФ, PK/FK, согласованные имена, ссылочная целостность", 3),
        ("ER-диаграмма в PDF: таблицы, связи, атрибуты, ключи", 2),
        ("Структура таблиц соответствует функционалу подсистемы", 1),
    ]),
    ("Модуль 1. Реализация базы данных в конкретной системе управления базами данных — 4", [
        ("Скрипт БД и данные из import загружены", 2),
        ("База подключена к приложению", 2),
    ]),
    ("Модуль 2. Формирование алгоритмов разработки программных модулей в соответствии с техническим заданием — 2", [
        ("Блок-схема по ГОСТ 19.701-90 (PDF)", 2),
    ]),
    ("Модуль 2. Разработка программных модулей в соответствии с техническим заданием — 11", [
        ("Окно входа: логин из БД, гость, выход на окно входа", 3),
        ("ФИО в правом верхнем углу, единый стиль, логотип, иконка", 2),
        ("Список товаров из БД: фото или заглушка, все поля", 3),
        ("Подсветка: скидка больше 15% (#2E8B57), нет на складе (голубой), зачёркнутая цена", 3),
    ]),
    ("Модуль 2. Выполнение отладки программных модулей с использованием специализированных программных средств — 2", [
        ("Нет аварийных завершений, проверены сценарии", 2),
    ]),
    ("Модуль 3. Выполнение работ по модификации отдельных компонент программного обеспечения в соответствии с потребностями заказчика — 24", [
        ("Поиск по всем текстовым полям, сортировка по остатку, фильтр по поставщику — в реальном времени", 6),
        ("Форма добавления/редактирования товара, фото 300×200", 6),
        ("Валидация полей, сообщения об ошибках, кнопка «Назад»", 4),
        ("Удаление товара, запрет удаления товара из заказа", 4),
        ("Обновление списка после изменений, одно окно редактирования", 4),
    ]),
    ("Модуль 3. Использование современных средств поиска, анализа и интерпретации информации — 1", [
        ("Справочники, документация, git", 1),
    ]),
    ("Модуль 4. Выполнение интеграции модулей в программное обеспечение — 23", [
        ("Кнопка «Заказы», список заказов для менеджера и администратора", 5),
        ("Форма заказа: артикул, статус, пункт выдачи, даты", 6),
        ("Добавление, редактирование и удаление заказа (только администратор)", 6),
        ("Обновление списков, согласованность с товарами и остатками", 6),
    ]),
    ("Модуль 4. Выбор способов решения задач профессиональной деятельности — 2", [
        ("Обоснование решений в README", 2),
    ]),
    ("Вариативная часть (тренировочная, определяет колледж) — 25", [
        ("Тесты модулей (unittest)", 5),
        ("Руководство пользователя с скриншотами", 5),
        ("Запуск и сборка: инструкция, requirements", 5),
        ("Резервная копия БД и импорт/экспорт", 5),
        ("Оптимизация запросов: индексы, без повторов", 5),
    ]),
]

# ---------------------------------------------------------------------------
# 7. ШПАРГАЛКИ
# ---------------------------------------------------------------------------
SNIPPETS = [
    ("Схема БД по КОД 2026: 10 таблиц", """CREATE TABLE products (
    product_id      INTEGER PRIMARY KEY,
    article         TEXT NOT NULL UNIQUE,
    name            TEXT NOT NULL,
    category_id     INTEGER NOT NULL REFERENCES categories(category_id),
    description     TEXT,
    manufacturer_id INTEGER NOT NULL REFERENCES manufacturers(manufacturer_id),
    supplier_id     INTEGER NOT NULL REFERENCES suppliers(supplier_id),
    price           REAL NOT NULL CHECK (price >= 0),
    unit_id         INTEGER NOT NULL REFERENCES units(unit_id),
    quantity        INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    discount        REAL NOT NULL DEFAULT 0 CHECK (discount >= 0 AND discount <= 1),
    image_path      TEXT
);

CREATE TABLE orders (
    order_id   INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    status_id  INTEGER NOT NULL REFERENCES order_statuses(status_id),
    point_id   INTEGER NOT NULL REFERENCES pickup_points(point_id),
    order_date TEXT NOT NULL,
    issue_date TEXT NOT NULL
);"""),
    ("Вход: логин и пароль или гость", """def find_user(conn, login, password):
    return conn.execute(
        "SELECT u.user_id, u.full_name, r.role_name "
        "FROM users u JOIN roles r ON r.role_id = u.role_id "
        "WHERE u.login = ? AND u.password = ?", (login, password)).fetchone()

user = find_user(conn, login_var.get().strip(), password_var.get())
if user is None:
    messagebox.showerror("Ошибка входа",
        "Неверный логин или пароль. Проверьте раскладку и попробуйте снова.")
else:
    session.user = user
    show_catalog()

# Гость: только просмотр товаров без поиска/фильтра/сортировки
session.user = {"full_name": "Гость", "role_name": "Гость"}
show_catalog()"""),
    ("Список товаров: 4 JOIN", """SELECT p.product_id, p.article, p.name, c.category_name,
       p.description, m.manufacturer_name, s.supplier_name,
       p.price, u.unit_name, p.quantity, p.discount, p.image_path
FROM products p
JOIN categories c ON c.category_id = p.category_id
JOIN manufacturers m ON m.manufacturer_id = p.manufacturer_id
JOIN suppliers s ON s.supplier_id = p.supplier_id
JOIN units u ON u.unit_id = p.unit_id
ORDER BY p.product_id;"""),
    ("Поиск + сортировка + фильтр", """def load_products(text="", supplier="Все поставщики", order="ASC"):
    sql = ("SELECT p.product_id, p.name, m.manufacturer_name, s.supplier_name, "
           "p.price, p.quantity, p.discount FROM products p "
           "JOIN manufacturers m ON m.manufacturer_id = p.manufacturer_id "
           "JOIN suppliers s ON s.supplier_id = p.supplier_id WHERE 1=1")
    params = []
    if text:
        sql += (" AND (p.name LIKE ? OR p.description LIKE ? "
                "OR m.manufacturer_name LIKE ? OR s.supplier_name LIKE ?)")
        params += [f"%{text}%"] * 4
    if supplier != "Все поставщики":
        sql += " AND s.supplier_name = ?"
        params.append(supplier)
    sql += " ORDER BY p.quantity " + ("DESC" if order == "DESC" else "ASC")
    return conn.execute(sql, params).fetchall()

for var in (search_var, supplier_var, sort_var):
    var.trace_add("write", lambda *_: refresh())"""),
    ("Цвета строк по КОД 2026", """table.tag_configure("out_of_stock", background="#B3E5FC")  # голубой
table.tag_configure("big_discount", background="#2E8B57")   # скидка > 15%
table.tag_configure("old_price", foreground="#c0392b")

for row in rows:
    pid, name, supplier, price, qty, discount = row
    tag = "out_of_stock" if qty == 0 else ("big_discount" if discount > 0.15 else "")
    final = round(price * (1 - discount), 2)
    price_text = f"{price:.2f}" if discount == 0 else f"{price:.2f} → {final:.2f}"
    table.insert("", "end", values=(name, supplier, price_text, qty), tags=(tag,))"""),
    ("Сохранение товара: add/edit", """def save_product(data, product_id=None):
    if data["price"] < 0 or data["quantity"] < 0:
        messagebox.showerror("Ошибка", "Цена и количество не могут быть отрицательными.")
        return
    if product_id is None:
        next_id = conn.execute("SELECT COALESCE(MAX(product_id), 0) + 1 FROM products").fetchone()[0]
        conn.execute(
            "INSERT INTO products (product_id, article, name, category_id, description, "
            "manufacturer_id, supplier_id, price, unit_id, quantity, discount, image_path) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (next_id, *data.values()))
    else:
        conn.execute(
            "UPDATE products SET article=?, name=?, category_id=?, description=?, "
            "manufacturer_id=?, supplier_id=?, price=?, unit_id=?, quantity=?, "
            "discount=?, image_path=? WHERE product_id=?",
            (*data.values(), product_id))
    conn.commit()"""),
    ("Удаление товара из заказа запрещено", """used = conn.execute(
    "SELECT 1 FROM orders WHERE product_id = ?", (product_id,)).fetchone()
if used:
    messagebox.showwarning("Удаление запрещено",
        "Товар присутствует в заказе. Сначала удалите или измените заказ.")
    return
conn.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
conn.commit()"""),
    ("Заказы: список и форма", """SELECT o.order_id, p.article, st.status_name, pp.address,
       o.order_date, o.issue_date
FROM orders o
JOIN products p ON p.product_id = o.product_id
JOIN order_statuses st ON st.status_id = o.status_id
JOIN pickup_points pp ON pp.point_id = o.point_id
ORDER BY o.order_id;

INSERT INTO orders (product_id, status_id, point_id, order_date, issue_date)
VALUES (?, ?, ?, ?, ?);

UPDATE orders SET status_id = ?, point_id = ?, order_date = ?, issue_date = ?
WHERE order_id = ?;"""),
    ("Фото 300×200", """from PIL import Image

img = Image.open(src_path)
img = img.resize((300, 200))
dst = Path("images") / f"product_{product_id}.png"
img.save(dst)
conn.execute("UPDATE products SET image_path = ? WHERE product_id = ?",
             (str(dst), product_id))
conn.commit()"""),
    ("Ошибки и подтверждения", """messagebox.showerror("Ошибка данных",
    "Цена не может быть отрицательной. Введите число больше или равно 0.")
messagebox.showwarning("Удаление",
    "Товар будет удалён без возможности восстановления. Продолжить?")
if messagebox.askyesno("Подтверждение", "Удалить товар?"):
    delete_product(product_id)"""),
    ("Git: сдача работы", """git init
git add .
git commit -m "feat: БД, ER и список товаров"
git branch -M main
git remote add origin <url>
git push -u origin main

# после каждого модуля
git add .
git commit -m "feat: поиск, фильтр и CRUD товара"
git push"""),
    ("README и документы", """# Проект ДЭ 09.02.07-2

## Запуск
python app.py

## БД
schema.sql, 10 таблиц, 3НФ.

## Функционал
Вход/гость, каталог, поиск, фильтр, сортировка, CRUD товара, заказы.

## Скриншоты
1. Вход. 2. Каталог. 3. Форма товара. 4. Заказы.""")
]
