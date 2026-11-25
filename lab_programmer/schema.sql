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
