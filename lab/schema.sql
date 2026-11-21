-- ============================================================
-- ДЭ-2027, 09.02.07-2-2027 «Программист», Задание 1
-- Предметная область: торговая компания «Чудо Обувь»
-- 8 таблиц, 3НФ, PK/FK, CHECK/UNIQUE, ON DELETE.
-- Это и есть «скрипт БД с данными», который сдаётся на экзамене.
-- ============================================================
--
-- Даты заказов заданы относительными выражениями date('now', ...),
-- чтобы демо-данные всегда были актуальны: часть заказов попадает
-- в прошлый календарный месяц (для проверки скидки 25%).
--
-- Запуск:  sqlite3 chudo_obuv.db < schema.sql
-- или из Python: conn.executescript(open('schema.sql').read())
-- ============================================================


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
INSERT INTO roles (role_id, role_name) VALUES
 (1,'Администратор'),
 (2,'Менеджер'),
 (3,'Авторизованный пользователь');
INSERT INTO categories (category_id, category_name) VALUES
 (1,'Детская обувь'),
 (2,'Женская'),
 (3,'Мужская');
INSERT INTO sizes (size_id, size_value) VALUES
 (1,18),
 (2,19),
 (3,20),
 (4,21),
 (5,22),
 (6,23),
 (7,24),
 (8,25),
 (9,26),
 (10,27),
 (11,28),
 (12,29),
 (13,30),
 (14,31),
 (15,32),
 (16,33),
 (17,34),
 (18,35),
 (19,36),
 (20,36.5),
 (21,37),
 (22,37.5),
 (23,38),
 (24,38.5),
 (25,39),
 (26,39.5),
 (27,40),
 (28,40.5),
 (29,41),
 (30,41.5),
 (31,42),
 (32,42.5),
 (33,43),
 (34,44),
 (35,45);
INSERT INTO users (user_id, last_name, first_name, middle_name, login, role_id) VALUES
 (1,'Иванов','Иван','Иванович','admin',1),
 (2,'Петров','Пётр','Петрович','manager',2),
 (3,'Сидорова','Анна','Сергеевна','asidorova',3),
 (4,'Павлова','Елена','Викторовна','epavlova',3),
 (5,'Васильева','Ольга','Игоревна','ovasileva',3),
 (6,'Смирнов','Алексей','Дмитриевич','asmirnov',3),
 (7,'Кузнецова','Мария','Андреевна','mkuznetsova',3),
 (8,'Попов','Денис','Сергеевич','dpopov',3),
 (9,'Новикова','Ирина','Павловна','inovikova',3),
 (10,'Морозов','Кирилл','Олегович','kmorozov',3);
INSERT INTO products (product_id, category_id, subcategory, name, manufacturer, description, composition, image_path, price) VALUES
 (1,2,'Кроссовки','Кроссовки City Run','Азимут','Кроссовки для города и прогулок. Дышащий верх, мягкая подошва.','текстиль, резина','img/01.png',4590.0),
 (2,2,'Ботинки','Ботинки Classic','Марко','Классические женские ботинки на низком каблуке.','натуральная кожа','img/02.png',7890.0),
 (3,2,'Туфли','Туфли Office','Elegance','Туфли для офиса и деловых встреч. Устойчивый каблук.','эко-кожа',NULL,6290.0),
 (4,2,'Сандалии','Сандалии Summer','Азимут','Лёгкие летние сандалии с регулируемыми ремешками.','текстиль, ЭВА','img/04.png',2990.0),
 (5,2,'Кеды','Кеды White','Марко','Белые кеды на каждый день. Съёмная стелька.','текстиль, резина',NULL,3990.0),
 (6,2,'Ботинки','Ботинки Winter','Nord','Утеплённые ботинки с мембраной для холодной погоды.','нубук, мех','img/06.png',9490.0),
 (7,2,'Туфли','Туфли Elegance','Elegance','Вечерние туфли с декоративной пряжкой.','эко-кожа','img/07.png',7290.0),
 (8,3,'Кроссовки','Кроссовки Trail','Азимут','Кроссовки для пересечённой местности и лёгкого треккинга.','текстиль, резина','img/08.png',6990.0),
 (9,3,'Ботинки','Ботинки Trekker','Nord','Туристические ботинки с усиленной подошвой.','нубук, резина',NULL,8990.0),
 (10,3,'Кеды','Кеды Retro','Марко','Кеды в ретро-стиле, подходят к джинсам.','текстиль, резина','img/10.png',4490.0),
 (11,3,'Туфли','Туфли Business','Elegance','Мужские туфли для делового стиля.','натуральная кожа','img/11.png',8290.0),
 (12,3,'Сандалии','Сандалии Beach','Азимут','Пляжные сандалии, быстро сохнут.','ЭВА',NULL,3190.0),
 (13,3,'Кроссовки','Кроссовки Marathon','Азимут','Беговые кроссовки с амортизацией.','текстиль, резина','img/13.png',9990.0),
 (14,1,'Кроссовки','Кроссовки Sun Kids','Азимут','Детские кроссовки с липучками.','текстиль, резина','img/14.png',2490.0),
 (15,1,'Ботинки','Ботинки First Step','Nord','Детские ботинки с тёплой подкладкой.','нубук, мех',NULL,3290.0),
 (16,1,'Кеды','Кеды School','Марко','Школьные кеды, легко моются.','текстиль, резина','img/16.png',2790.0);
INSERT INTO product_items (item_id, product_id, size_id, quantity) VALUES
 (1,1,19,2),
 (2,1,21,3),
 (3,1,23,1),
 (4,1,25,0),
 (5,1,27,2),
 (6,1,29,0),
 (7,2,19,1),
 (8,2,21,1),
 (9,2,23,1),
 (10,2,25,0),
 (11,3,19,2),
 (12,3,21,2),
 (13,3,23,2),
 (14,3,25,2),
 (15,4,19,0),
 (16,4,21,1),
 (17,4,23,1),
 (18,5,19,3),
 (19,5,21,3),
 (20,5,23,3),
 (21,6,19,1),
 (22,6,21,1),
 (23,6,23,1),
 (24,6,25,1),
 (25,6,27,1),
 (26,7,19,1),
 (27,7,21,0),
 (28,8,27,2),
 (29,8,29,3),
 (30,8,31,1),
 (31,8,33,0),
 (32,9,27,1),
 (33,9,29,1),
 (34,9,31,1),
 (35,10,27,4),
 (36,10,29,4),
 (37,10,31,4),
 (38,11,27,1),
 (39,11,29,1),
 (40,11,31,1),
 (41,11,33,1),
 (42,12,27,0),
 (43,12,29,2),
 (44,12,31,2),
 (45,13,27,2),
 (46,13,29,2),
 (47,13,31,2),
 (48,13,33,2),
 (49,13,34,2),
 (50,14,5,2),
 (51,14,6,2),
 (52,14,7,2),
 (53,14,8,2),
 (54,15,5,1),
 (55,15,6,1),
 (56,15,7,1),
 (57,15,8,1),
 (58,16,5,1),
 (59,16,6,1),
 (60,16,7,1);
INSERT INTO orders (order_id, order_date, user_id) VALUES
 (1,date('now','start of month','-1 months','+3 days'),4),
 (2,date('now','start of month','-1 months','+7 days'),5),
 (3,date('now','start of month','-1 months','+12 days'),6),
 (4,date('now','start of month','-1 months','+18 days'),7),
 (5,date('now','start of month','0 months','+2 days'),4),
 (6,date('now','start of month','0 months','+9 days'),5),
 (7,date('now','start of month','0 months','+15 days'),6),
 (8,date('now','start of month','-2 months','+5 days'),7),
 (9,date('now','start of month','-2 months','+20 days'),8),
 (10,date('now','start of month','-2 months','+25 days'),8);
INSERT INTO order_items (order_item_id, order_id, item_id, quantity, unit_price) VALUES
 (1,1,1,1,4590.0),
 (2,2,12,2,6290.0),
 (3,3,20,1,3990.0),
 (4,4,29,1,6990.0),
 (5,5,35,1,4490.0),
 (6,6,47,2,9990.0),
 (7,7,8,1,7890.0),
 (8,8,23,1,9490.0),
 (9,9,52,2,2490.0);
