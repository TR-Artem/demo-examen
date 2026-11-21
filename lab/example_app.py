# -*- coding: utf-8 -*-
"""
ОБРАЗЕЦ выполнения ДЭ-2027, 09.02.07-2-2027 «Программист» (ПУ).
Предметная область: торговая компания «Чудо Обувь».
Стек: Python + tkinter + SQLite.

Реализованы все 5 заданий:
  1. БД в 3НФ (schema.sql, 8 таблиц) + импорт (import_csv.py)
  2. Алгоритм/скидка, стиль, каталог, «много/мало», подсветка, скидка 25%
  3. Вход по логину, роли, ФИО, поиск/фильтр/сортировка, карточка, корзина, заказ
  4. Заказы у Менеджера/Администратора: список, состав, добавление/удаление,
     изменение даты (админ), удаление позиций (админ)
  5. Статистика заказов + шаблон руководства пользователя

Запуск:  python example_app.py
Сброс:   python example_app.py --reset

Логины (пароль не нужен):
  admin — Администратор, manager — Менеджер, asidorova/epavlova/... — пользователи.
  Кнопка «Без входа» — гость.
"""
from __future__ import annotations

import sqlite3
import sys
import tkinter as tk
from datetime import date
from pathlib import Path
from tkinter import messagebox, simpledialog, ttk

BASE = Path(__file__).resolve().parent
DB_PATH = BASE / "chudo_obuv.db"
SCHEMA = BASE / "schema.sql"

ROLE_ADMIN = "Администратор"
ROLE_MANAGER = "Менеджер"
ROLE_USER = "Авторизованный пользователь"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    if "--reset" in sys.argv and DB_PATH.exists():
        DB_PATH.unlink()
    if DB_PATH.exists():
        return
    conn = get_conn()
    try:
        conn.executescript(SCHEMA.read_text(encoding="utf-8"))
        conn.commit()
    finally:
        conn.close()


def fio(row) -> str:
    parts = [row["last_name"], row["first_name"]]
    if row["middle_name"]:
        parts.append(row["middle_name"])
    return " ".join(parts)


def money(value) -> str:
    return f"{float(value or 0):.2f}"


# ---------------------------------------------------------------------------
# Приложение
# ---------------------------------------------------------------------------
class App(tk.Tk):
    def __init__(self):
        init_db()
        super().__init__()
        self.conn = get_conn()
        self.user = None                 # sqlite3.Row или None (гость)
        self.cart = []                   # список позиций корзины
        self.title("Чудо Обувь — вход")
        self.geometry("1180x720")
        self.minsize(1000, 600)

        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", rowheight=26, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("Title.TLabel", font=("Segoe UI", 15, "bold"))
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))

        container = ttk.Frame(self, padding=8)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for key, cls in (("login", LoginFrame), ("catalog", CatalogFrame),
                         ("product", ProductFrame), ("cart", CartFrame),
                         ("orders", OrdersFrame), ("order_view", OrderViewFrame),
                         ("stats", StatisticsFrame)):
            frame = cls(container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[key] = frame

        self.show("login")
        self.protocol("WM_DELETE_WINDOW", self.close)

    # -- навигация ---------------------------------------------------------
    TITLES = {
        "login": "вход в систему",
        "catalog": "каталог товаров",
        "product": "карточка товара",
        "cart": "корзина",
        "orders": "заказы",
        "order_view": "состав заказа",
        "stats": "статистика заказов",
    }

    def show(self, key, **kwargs):
        frame = self.frames[key]
        if hasattr(frame, "on_show"):
            frame.on_show(**kwargs)
        frame.tkraise()
        self.title("Чудо Обувь — " + self.TITLES[key])

    def close(self):
        self.conn.close()
        self.destroy()

    # -- роль --------------------------------------------------------------
    @property
    def role(self):
        return self.user["role_name"] if self.user else "Гость"

    def is_staff(self):
        return self.role in (ROLE_MANAGER, ROLE_ADMIN)

    def is_admin(self):
        return self.role == ROLE_ADMIN

    def is_auth(self):
        return self.user is not None

    # -- авторизация -------------------------------------------------------
    def login(self, login_value: str):
        row = self.conn.execute(
            "SELECT u.user_id, u.last_name, u.first_name, u.middle_name, r.role_name "
            "FROM users u JOIN roles r ON u.role_id = r.role_id "
            "WHERE u.login = ?", (login_value,)).fetchone()
        if row is None:
            messagebox.showerror(
                "Ошибка авторизации",
                "Пользователь с таким логином не найден. Выберите логин из списка "
                "или войдите как гость.")
            return
        self.user = row
        self.show("catalog")

    def logout(self):
        self.user = None
        self.cart = []
        self.show("login")

    # -- товары ------------------------------------------------------------
    def final_price(self, product_id: int, price: float) -> float:
        has_discount = self.discount_flag(product_id)
        return round(price * 0.75, 2) if has_discount else round(price, 2)

    def discount_flag(self, product_id: int) -> bool:
        row = self.conn.execute(
            "SELECT NOT EXISTS ("
            "  SELECT 1 FROM orders o "
            "  JOIN order_items oi ON oi.order_id = o.order_id "
            "  JOIN product_items pi ON pi.item_id = oi.item_id "
            "  WHERE pi.product_id = ? "
            "    AND o.order_date >= date('now','start of month','-1 month') "
            "    AND o.order_date <  date('now','start of month')) AS flag",
            (product_id,)).fetchone()
        return bool(row["flag"])

    def catalog_rows(self, pattern="", category="Все категории", sort="По цене ↑"):
        sql = (
            "SELECT p.product_id, p.name, c.category_name, p.manufacturer, "
            "p.composition, p.image_path, p.price, "
            "COALESCE(SUM(pi.quantity), 0) AS total_qty, "
            "CASE WHEN NOT EXISTS ("
            "  SELECT 1 FROM orders o "
            "  JOIN order_items oi ON oi.order_id = o.order_id "
            "  JOIN product_items x ON x.item_id = oi.item_id "
            "  WHERE x.product_id = p.product_id "
            "    AND o.order_date >= date('now','start of month','-1 month') "
            "    AND o.order_date <  date('now','start of month')"
            ") THEN 1 ELSE 0 END AS has_discount "
            "FROM products p "
            "JOIN categories c ON p.category_id = c.category_id "
            "LEFT JOIN product_items pi ON pi.product_id = p.product_id "
            "WHERE 1 = 1")
        params = []
        if pattern:
            sql += " AND (p.name LIKE ? OR p.description LIKE ?)"
            params += [f"%{pattern}%", f"%{pattern}%"]
        if category and category != "Все категории":
            sql += " AND c.category_name = ?"
            params.append(category)
        sql += (" GROUP BY p.product_id, p.name, c.category_name, p.manufacturer, "
                "p.composition, p.image_path, p.price")
        if sort == "По цене ↓":
            sql += " ORDER BY p.price DESC, p.product_id"
        elif sort == "По наименованию":
            sql += " ORDER BY p.name ASC, p.product_id"
        else:
            sql += " ORDER BY p.price ASC, p.product_id"
        return self.conn.execute(sql, params).fetchall()

    def product(self, product_id: int):
        return self.conn.execute(
            "SELECT p.*, c.category_name FROM products p "
            "JOIN categories c ON p.category_id = c.category_id "
            "WHERE p.product_id = ?", (product_id,)).fetchone()

    def sizes(self, product_id: int):
        return self.conn.execute(
            "SELECT pi.item_id, s.size_value, pi.quantity "
            "FROM product_items pi JOIN sizes s ON s.size_id = pi.size_id "
            "WHERE pi.product_id = ? AND pi.quantity > 0 "
            "ORDER BY s.size_value", (product_id,)).fetchall()

    # -- корзина и заказ ---------------------------------------------------
    def cart_count(self):
        return sum(item["qty"] for item in self.cart)

    def update_cart_button(self):
        frame = self.frames.get("catalog")
        if frame and hasattr(frame, "cart_btn"):
            frame.cart_btn.config(text=f"Корзина ({self.cart_count()})")

    def create_order(self):
        if not self.user:
            raise ValueError("Оформить заказ может только авторизованный пользователь.")
        if not self.cart:
            raise ValueError("Корзина пуста.")
        try:
            self.conn.execute("BEGIN")
            cur = self.conn.execute(
                "INSERT INTO orders (order_date, user_id) VALUES (date('now'), ?)",
                (self.user["user_id"],))
            order_id = cur.lastrowid
            for item in self.cart:
                left = self.conn.execute(
                    "SELECT quantity FROM product_items WHERE item_id = ?",
                    (item["item_id"],)).fetchone()["quantity"]
                if item["qty"] > left:
                    raise ValueError(
                        f"«{item['name']}», размер {item['size']}: на складе осталось "
                        f"{left} пар. Уменьшите количество.")
                self.conn.execute(
                    "INSERT INTO order_items (order_id, item_id, quantity, unit_price) "
                    "VALUES (?, ?, ?, ?)",
                    (order_id, item["item_id"], item["qty"], item["price"]))
                self.conn.execute(
                    "UPDATE product_items SET quantity = quantity - ? WHERE item_id = ?",
                    (item["qty"], item["item_id"]))
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        self.cart.clear()
        return order_id

    # -- заказы ------------------------------------------------------------
    def order_rows(self, pattern=""):
        sql = (
            "SELECT o.order_id, o.order_date, "
            "u.last_name || ' ' || u.first_name || ' ' || COALESCE(u.middle_name, '') AS client, "
            "ROUND(COALESCE(SUM(oi.quantity * oi.unit_price), 0), 2) AS total "
            "FROM orders o "
            "JOIN users u ON u.user_id = o.user_id "
            "LEFT JOIN order_items oi ON oi.order_id = o.order_id "
            "WHERE 1 = 1")
        params = []
        if pattern:
            sql += (" AND (CAST(o.order_id AS TEXT) LIKE ? OR o.order_date LIKE ? "
                    "OR u.last_name LIKE ? OR u.first_name LIKE ?)")
            params += [f"%{pattern}%"] * 4
        sql += (" GROUP BY o.order_id, o.order_date, u.last_name, u.first_name, u.middle_name "
                "ORDER BY o.order_id DESC")
        return self.conn.execute(sql, params).fetchall()

    def order_items(self, order_id: int):
        return self.conn.execute(
            "SELECT oi.order_item_id, p.name, p.manufacturer, s.size_value, "
            "oi.quantity, oi.unit_price, ROUND(oi.quantity * oi.unit_price, 2) AS line_total "
            "FROM order_items oi "
            "JOIN product_items pi ON pi.item_id = oi.item_id "
            "JOIN products p ON p.product_id = pi.product_id "
            "JOIN sizes s ON s.size_id = pi.size_id "
            "WHERE oi.order_id = ? ORDER BY oi.order_item_id", (order_id,)).fetchall()

    def order_total(self, order_id: int) -> float:
        row = self.conn.execute(
            "SELECT ROUND(COALESCE(SUM(quantity * unit_price), 0), 2) AS total "
            "FROM order_items WHERE order_id = ?", (order_id,)).fetchone()
        return float(row["total"])

    def stats(self):
        return self.conn.execute(
            "SELECT COUNT(*) AS orders_count, "
            "COALESCE(SUM(total), 0) AS revenue, "
            "CASE WHEN COUNT(*) = 0 THEN 0 ELSE ROUND(SUM(total) / COUNT(*), 2) END AS avg_check "
            "FROM (SELECT o.order_id, SUM(oi.quantity * oi.unit_price) AS total "
            "      FROM orders o LEFT JOIN order_items oi ON oi.order_id = o.order_id "
            "      GROUP BY o.order_id)").fetchone()


# ---------------------------------------------------------------------------
# Экран 1. Вход по логину
# ---------------------------------------------------------------------------
class LoginFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        box = ttk.LabelFrame(self, text="Вход в систему", padding=26)
        box.place(relx=0.5, rely=0.44, anchor="center")
        ttk.Label(box, text="Чудо Обувь", style="Title.TLabel").grid(
            row=0, column=0, columnspan=2, pady=(0, 6))
        ttk.Label(box, text="Система оформления заказов обуви",
                  foreground="#5c6b7a").grid(row=1, column=0, columnspan=2, pady=(0, 18))
        ttk.Label(box, text="Логин *").grid(row=2, column=0, sticky="w", pady=4)
        self.login_var = tk.StringVar()
        self.login_box = ttk.Combobox(box, textvariable=self.login_var, width=30)
        self.login_box.grid(row=2, column=1, pady=4)
        ttk.Label(box, text="Пароль не требуется — вход только по логину",
                  foreground="#5c6b7a").grid(row=3, column=0, columnspan=2, pady=(0, 10))
        ttk.Button(box, text="Войти", command=self.do_login).grid(
            row=4, column=0, columnspan=2, sticky="ew", pady=4)
        ttk.Button(box, text="Без входа (гость)", command=self.as_guest).grid(
            row=5, column=0, columnspan=2, sticky="ew")
        ttk.Label(box, text="admin · manager · asidorova · epavlova · ovasileva",
                  foreground="#5c6b7a").grid(row=6, column=0, columnspan=2, pady=(12, 0))

    def on_show(self):
        logins = [r["login"] for r in self.app.conn.execute(
            "SELECT login FROM users ORDER BY login")]
        self.login_box["values"] = logins
        if not self.login_var.get() and logins:
            self.login_var.set(logins[0])

    def do_login(self):
        value = self.login_var.get().strip()
        if not value:
            messagebox.showwarning("Не заполнено поле",
                                   "Выберите логин из списка — поле обязательно.")
            return
        self.app.login(value)

    def as_guest(self):
        self.app.user = None
        self.app.show("catalog")


# ---------------------------------------------------------------------------
# Экран 2. Каталог
# ---------------------------------------------------------------------------
class CatalogFrame(ttk.Frame):
    COLS = ("name", "category", "manufacturer", "composition", "price", "discount", "stock", "photo")

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        top = ttk.Frame(self)
        top.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 6))
        self.fio = ttk.Label(top, text="", style="Title.TLabel")
        self.fio.pack(side="left")
        self.role_label = ttk.Label(top, text="", foreground="#5c6b7a")
        self.role_label.pack(side="left", padx=10)
        ttk.Button(top, text="Выход", command=app.logout).pack(side="right")
        self.stats_btn = ttk.Button(top, text="Статистика", command=lambda: app.show("stats"))
        self.orders_btn = ttk.Button(top, text="Заказы", command=lambda: app.show("orders"))
        self.cart_btn = ttk.Button(top, text="Корзина (0)", command=lambda: app.show("cart"))
        for btn in (self.stats_btn, self.orders_btn, self.cart_btn):
            btn.pack_forget()

        self.tools = ttk.LabelFrame(self, text="Поиск, фильтр и сортировка", padding=8)
        self.tools.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 6))
        self.search_var = tk.StringVar()
        self.category_var = tk.StringVar(value="Все категории")
        self.sort_var = tk.StringVar(value="По цене ↑")
        ttk.Label(self.tools, text="Поиск:").pack(side="left")
        ttk.Entry(self.tools, textvariable=self.search_var, width=30).pack(side="left", padx=6)
        ttk.Label(self.tools, text="Категория:").pack(side="left", padx=(12, 0))
        self.category_box = ttk.Combobox(self.tools, textvariable=self.category_var,
                                         state="readonly", width=18)
        self.category_box.pack(side="left", padx=6)
        ttk.Label(self.tools, text="Сортировка:").pack(side="left", padx=(12, 0))
        ttk.Combobox(self.tools, textvariable=self.sort_var, state="readonly", width=16,
                     values=["По цене ↑", "По цене ↓", "По наименованию"]).pack(side="left", padx=6)
        for var in (self.search_var, self.category_var, self.sort_var):
            var.trace_add("write", self.refresh)

        self.table = ttk.Treeview(self, columns=self.COLS, show="headings")
        titles = {"name": "Наименование", "category": "Категория",
                  "manufacturer": "Производство", "composition": "Состав",
                  "price": "Цена", "discount": "Скидка", "stock": "Остаток",
                  "photo": "Изображение"}
        for col in self.COLS:
            self.table.heading(col, text=titles[col])
            self.table.column(col, width=110, anchor="w")
        self.table.column("name", width=220)
        self.table.column("composition", width=170)
        self.table.column("price", width=150)
        scroll = ttk.Scrollbar(self, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scroll.set)
        self.table.grid(row=2, column=0, sticky="nsew")
        scroll.grid(row=2, column=1, sticky="ns")
        self.table.tag_configure("low_stock", background="#FFB6B6")
        self.table.bind("<Double-1>", self.open_selected)

        bottom = ttk.Frame(self)
        bottom.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        ttk.Button(bottom, text="Открыть карточку", command=self.open_selected).pack(side="left")
        ttk.Label(bottom, text="Двойной клик по строке — карточка товара",
                  foreground="#5c6b7a").pack(side="right")

    def on_show(self):
        self.fio.config(text=fio(self.app.user) if self.app.user else "Гость")
        self.role_label.config(text=f"({self.app.role})")
        auth = self.app.is_auth()
        self.cart_btn.pack(side="right", padx=4) if auth else self.cart_btn.pack_forget()
        if self.app.is_staff():
            self.orders_btn.pack(side="right", padx=4)
            self.stats_btn.pack(side="right", padx=4)
        else:
            self.orders_btn.pack_forget()
            self.stats_btn.pack_forget()
        if self.app.role == "Гость":
            self.tools.grid_remove()       # гостю — без поиска/сортировки/фильтра
        else:
            self.tools.grid()
            cats = [r["category_name"] for r in self.app.conn.execute(
                "SELECT category_name FROM categories ORDER BY category_name")]
            self.category_box["values"] = ["Все категории"] + cats
            if self.category_var.get() not in self.category_box["values"]:
                self.category_var.set("Все категории")
        self.app.update_cart_button()
        self.refresh()

    def refresh(self, *_args):
        pattern = self.search_var.get().strip() if self.app.role != "Гость" else ""
        category = self.category_var.get() if self.app.role != "Гость" else "Все категории"
        sort = self.sort_var.get() if self.app.role != "Гость" else "По цене ↑"
        rows = self.app.catalog_rows(pattern, category, sort)
        self.table.delete(*self.table.get_children())
        for row in rows:
            price = float(row["price"])
            final = price * 0.75 if row["has_discount"] else price
            price_text = f"{price:.2f} → {final:.2f}" if row["has_discount"] else f"{price:.2f}"
            total = int(row["total_qty"])
            label = "много" if total > 5 else "мало"
            tag = "low_stock" if total <= 3 else ""
            self.table.insert("", "end", iid=str(row["product_id"]),
                              values=(row["name"], row["category_name"],
                                      row["manufacturer"], row["composition"] or "",
                                      price_text, "−25%" if row["has_discount"] else "",
                                      label, row["image_path"] or "picture.png"),
                              tags=(tag,))
        self.app.update_cart_button()

    def open_selected(self, _event=None):
        sel = self.table.selection()
        if not sel:
            messagebox.showinfo("Выберите товар", "Выделите строку в каталоге.")
            return
        self.app.show("product", product_id=int(sel[0]))


# ---------------------------------------------------------------------------
# Экран 3. Карточка товара
# ---------------------------------------------------------------------------
class ProductFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.product_id = None
        self.size_rows = []
        self.vars = {k: tk.StringVar() for k in
                     ("name", "category", "manufacturer", "composition",
                      "description", "price")}
        ttk.Label(self, text="Карточка товара", style="Title.TLabel").grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

        self.canvas = tk.Canvas(self, width=200, height=140, bg="#eef2f4",
                                highlightthickness=1, highlightbackground="#c8d2d8")
        self.canvas.grid(row=1, column=0, rowspan=4, sticky="nw", padx=(0, 16))
        self.canvas.create_text(100, 70, text="picture.png", fill="#5c6b7a")

        rows = [("name", "Наименование"), ("category", "Категория"),
                ("manufacturer", "Производство"), ("composition", "Состав"),
                ("description", "Описание"), ("price", "Цена со скидкой")]
        for i, (key, caption) in enumerate(rows, start=1):
            ttk.Label(self, text=caption).grid(row=i, column=1, sticky="nw", pady=3)
            value = ttk.Label(self, textvariable=self.vars[key], wraplength=620,
                              justify="left")
            value.grid(row=i, column=2, sticky="nw", pady=3)

        ttk.Label(self, text="Размер:").grid(row=6, column=0, sticky="w", pady=(14, 3))
        self.size_var = tk.StringVar()
        self.size_box = ttk.Combobox(self, textvariable=self.size_var, state="readonly", width=18)
        self.size_box.grid(row=6, column=1, sticky="w")
        ttk.Label(self, text="Количество:").grid(row=7, column=0, sticky="w", pady=3)
        self.qty_var = tk.IntVar(value=1)
        self.qty_box = ttk.Spinbox(self, from_=1, to=1, textvariable=self.qty_var, width=8)
        self.qty_box.grid(row=7, column=1, sticky="w")
        self.stock_label = ttk.Label(self, text="", foreground="#5c6b7a")
        self.stock_label.grid(row=7, column=2, sticky="w", padx=8)

        bar = ttk.Frame(self)
        bar.grid(row=8, column=0, columnspan=3, sticky="ew", pady=(18, 0))
        self.add_btn = ttk.Button(bar, text="Добавить в корзину", command=self.add_to_cart)
        self.add_btn.pack(side="left")
        ttk.Button(bar, text="Назад в каталог",
                   command=lambda: app.show("catalog")).pack(side="left", padx=8)

    def on_show(self, product_id=None):
        self.product_id = product_id
        row = self.app.product(product_id)
        if row is None:
            messagebox.showerror("Ошибка", "Товар не найден.")
            self.app.show("catalog")
            return
        self.vars["name"].set(row["name"])
        self.vars["category"].set(row["category_name"])
        self.vars["manufacturer"].set(row["manufacturer"])
        self.vars["composition"].set(row["composition"] or "—")
        self.vars["description"].set(row["description"] or "—")
        final = self.app.final_price(product_id, float(row["price"]))
        if self.app.discount_flag(product_id):
            self.vars["price"].set(f"{row['price']:.2f} → {final:.2f}  (скидка 25%)")
        else:
            self.vars["price"].set(f"{final:.2f}")
        self.canvas.delete("all")
        self.canvas.create_text(100, 70, text=row["image_path"] or "picture.png",
                                fill="#5c6b7a", width=180)
        self.size_rows = self.app.sizes(product_id)
        self.size_box["values"] = [f"{r['size_value']:g}" for r in self.size_rows]
        self.size_var.set(self.size_box["values"][0] if self.size_rows else "")
        self.qty_var.set(1)
        self.qty_box.config(to=max(1, self.size_rows[0]["quantity"] if self.size_rows else 1))
        self.stock_label.config(text="нет в наличии" if not self.size_rows
                                else f"на складе: {self.size_rows[0]['quantity']} пар")
        self.add_btn.config(state="normal" if self.size_rows else "disabled")
        self.size_box.bind("<<ComboboxSelected>>", self.on_size_change)

    def on_size_change(self, _event=None):
        for row in self.size_rows:
            if f"{row['size_value']:g}" == self.size_var.get():
                self.qty_box.config(to=max(1, row["quantity"]))
                self.qty_var.set(1)
                self.stock_label.config(text=f"на складе: {row['quantity']} пар")
                break

    def add_to_cart(self):
        if not self.app.is_auth():
            messagebox.showwarning(
                "Требуется вход",
                "Оформлять заказы может только авторизованный пользователь. "
                "Нажмите «Выход» и войдите по логину.")
            return
        if not self.size_rows:
            return
        chosen = None
        for row in self.size_rows:
            if f"{row['size_value']:g}" == self.size_var.get():
                chosen = row
                break
        if chosen is None:
            messagebox.showerror("Ошибка", "Выберите размер из списка.")
            return
        try:
            qty = int(self.qty_var.get())
        except (ValueError, tk.TclError):
            messagebox.showerror("Ошибка ввода",
                                 "Количество должно быть целым числом. Введите 1 или больше.")
            return
        if qty < 1 or qty > chosen["quantity"]:
            messagebox.showerror(
                "Неверное количество",
                f"На складе {chosen['quantity']} пар. Введите число от 1 до {chosen['quantity']}.")
            return
        final = self.app.final_price(self.product_id, float(self.app.product(self.product_id)["price"]))
        self.app.cart.append({
            "item_id": chosen["item_id"],
            "name": self.vars["name"].get(),
            "size": f"{chosen['size_value']:g}",
            "qty": qty,
            "price": final,
        })
        self.app.update_cart_button()
        messagebox.showinfo("Добавлено",
                            f"{self.vars['name'].get()} · размер {chosen['size_value']:g} · "
                            f"{qty} пар добавлено в корзину.")
        self.app.show("catalog")


# ---------------------------------------------------------------------------
# Экран 4. Корзина
# ---------------------------------------------------------------------------
class CartFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        ttk.Label(self, text="Корзина", style="Title.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 8))
        self.table = ttk.Treeview(self, columns=("name", "size", "qty", "price", "sum"),
                                  show="headings")
        for col, title, width in (("name", "Наименование", 300), ("size", "Размер", 80),
                                  ("qty", "Количество", 100), ("price", "Цена", 120),
                                  ("sum", "Сумма", 120)):
            self.table.heading(col, text=title)
            self.table.column(col, width=width, anchor="w")
        self.table.grid(row=1, column=0, sticky="nsew")
        self.total_label = ttk.Label(self, text="Итого: 0.00", style="Title.TLabel")
        self.total_label.grid(row=2, column=0, sticky="w", pady=8)
        bar = ttk.Frame(self)
        bar.grid(row=3, column=0, sticky="ew")
        ttk.Button(bar, text="Удалить позицию", command=self.remove).pack(side="left")
        ttk.Button(bar, text="Оформить заказ", command=self.checkout).pack(side="left", padx=8)
        ttk.Button(bar, text="Назад в каталог",
                   command=lambda: app.show("catalog")).pack(side="left")

    def on_show(self):
        self.refresh()

    def refresh(self):
        self.table.delete(*self.table.get_children())
        total = 0.0
        for i, item in enumerate(self.app.cart):
            line = item["qty"] * item["price"]
            total += line
            self.table.insert("", "end", iid=str(i),
                              values=(item["name"], item["size"], item["qty"],
                                      money(item["price"]), money(line)))
        self.total_label.config(text=f"Итого: {money(total)}")

    def remove(self):
        sel = self.table.selection()
        if not sel:
            messagebox.showinfo("Выберите позицию", "Выделите строку корзины.")
            return
        del self.app.cart[int(sel[0])]
        self.app.update_cart_button()
        self.refresh()

    def checkout(self):
        if not self.app.is_auth():
            messagebox.showwarning("Требуется вход",
                                   "Войдите по логину, чтобы оформить заказ.")
            return
        if not self.app.cart:
            messagebox.showwarning("Корзина пуста", "Добавьте хотя бы одну позицию.")
            return
        if not messagebox.askyesno("Подтверждение",
                                   "Оформить заказ? Отменить после сохранения будет нельзя."):
            return
        try:
            order_id = self.app.create_order()
        except (ValueError, sqlite3.Error) as err:
            messagebox.showerror("Заказ не создан", f"{err}\n\nИсправьте данные и повторите.")
            return
        messagebox.showinfo("Готово", f"Заказ №{order_id} оформлен. Остатки обновлены.")
        self.app.show("catalog")


# ---------------------------------------------------------------------------
# Экран 5. Список заказов (Менеджер/Администратор)
# ---------------------------------------------------------------------------
class OrdersFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        top = ttk.Frame(self)
        top.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        ttk.Label(top, text="Заказы", style="Title.TLabel").pack(side="left")
        ttk.Button(top, text="← Назад в каталог",
                   command=lambda: app.show("catalog")).pack(side="right")
        tools = ttk.Frame(self)
        tools.grid(row=1, column=0, sticky="ew", pady=(0, 6))
        self.search_var = tk.StringVar()
        ttk.Label(tools, text="Поиск (номер, дата, ФИО):").pack(side="left")
        ttk.Entry(tools, textvariable=self.search_var, width=32).pack(side="left", padx=6)
        self.search_var.trace_add("write", self.refresh)
        self.table = ttk.Treeview(self, columns=("id", "date", "client", "total"),
                                  show="headings")
        for col, title, width in (("id", "№", 70), ("date", "Дата заказа", 140),
                                  ("client", "ФИО клиента", 340), ("total", "Сумма", 140)):
            self.table.heading(col, text=title)
            self.table.column(col, width=width, anchor="w")
        self.table.grid(row=2, column=0, sticky="nsew")
        self.table.bind("<Double-1>", self.view_selected)
        bar = ttk.Frame(self)
        bar.grid(row=3, column=0, sticky="ew", pady=8)
        ttk.Button(bar, text="Состав заказа", command=self.view_selected).pack(side="left")
        ttk.Button(bar, text="Добавить заказ", command=self.add_order).pack(side="left", padx=8)
        self.delete_btn = ttk.Button(bar, text="Удалить заказ", command=self.delete_selected)
        self.delete_btn.pack(side="left")

    def on_show(self):
        if not self.app.is_staff():
            messagebox.showwarning("Доступ запрещён",
                                   "Заказы доступны Менеджеру и Администратору.")
            self.app.show("catalog")
            return
        self.refresh()

    def refresh(self, *_args):
        rows = self.app.order_rows(self.search_var.get().strip())
        self.table.delete(*self.table.get_children())
        for row in rows:
            self.table.insert("", "end", iid=str(row["order_id"]),
                              values=(row["order_id"], row["order_date"],
                                      row["client"], money(row["total"])))

    def selected_id(self):
        sel = self.table.selection()
        return int(sel[0]) if sel else None

    def view_selected(self, _event=None):
        oid = self.selected_id()
        if oid is None:
            messagebox.showinfo("Выберите заказ", "Выделите строку в списке.")
            return
        self.app.show("order_view", order_id=oid)

    def add_order(self):
        messagebox.showinfo(
            "Новый заказ",
            "Выберите товары в каталоге, добавьте их в корзину и нажмите "
            "«Оформить заказ». Заказ сохранится с текущей датой.")
        self.app.show("catalog")

    def delete_selected(self):
        oid = self.selected_id()
        if oid is None:
            messagebox.showinfo("Выберите заказ", "Выделите строку в списке.")
            return
        if not messagebox.askyesno("Удаление заказа",
                                   f"Удалить заказ №{oid} вместе со всеми позициями?"):
            return
        try:
            self.app.conn.execute("DELETE FROM orders WHERE order_id = ?", (oid,))
            self.app.conn.commit()
        except sqlite3.Error as err:
            messagebox.showerror("Ошибка базы данных", str(err))
            return
        self.refresh()


# ---------------------------------------------------------------------------
# Экран 6. Состав заказа
# ---------------------------------------------------------------------------
class OrderViewFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.order_id = None
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.header = ttk.Label(self, text="", style="Title.TLabel")
        self.header.grid(row=0, column=0, sticky="w", pady=(0, 6))
        self.table = ttk.Treeview(
            self, columns=("name", "manufacturer", "size", "qty", "price", "sum"),
            show="headings")
        for col, title, width in (("name", "Товар", 260), ("manufacturer", "Производство", 150),
                                  ("size", "Размер", 80), ("qty", "Кол-во", 80),
                                  ("price", "Цена за ед.", 120), ("sum", "Сумма", 120)):
            self.table.heading(col, text=title)
            self.table.column(col, width=width, anchor="w")
        self.table.grid(row=2, column=0, sticky="nsew")
        self.total_label = ttk.Label(self, text="Итого: 0.00", style="Title.TLabel")
        self.total_label.grid(row=3, column=0, sticky="w", pady=8)
        bar = ttk.Frame(self)
        bar.grid(row=4, column=0, sticky="ew")
        self.date_btn = ttk.Button(bar, text="Изменить дату", command=self.change_date)
        self.del_item_btn = ttk.Button(bar, text="Удалить позицию", command=self.delete_item)
        self.add_item_btn = ttk.Button(bar, text="Добавить позицию", command=self.add_item)
        for btn in (self.date_btn, self.del_item_btn, self.add_item_btn):
            btn.pack(side="left", padx=(0, 8))
        ttk.Button(bar, text="← Назад к заказам",
                   command=lambda: app.show("orders")).pack(side="right")

    def on_show(self, order_id=None):
        if not self.app.is_staff():
            messagebox.showwarning("Доступ запрещён", "Состав заказа доступен персоналу.")
            self.app.show("catalog")
            return
        self.order_id = order_id
        row = self.app.conn.execute(
            "SELECT o.order_id, o.order_date, "
            "u.last_name || ' ' || u.first_name || ' ' || COALESCE(u.middle_name, '') AS client "
            "FROM orders o JOIN users u ON u.user_id = o.user_id WHERE o.order_id = ?",
            (order_id,)).fetchone()
        self.header.config(
            text=f"Заказ №{order_id} от {row['order_date']} — {row['client']}")
        for btn in (self.date_btn, self.del_item_btn):
            btn.pack(side="left", padx=(0, 8)) if self.app.is_admin() else btn.pack_forget()
        self.refresh()

    def refresh(self):
        rows = self.app.order_items(self.order_id)
        self.table.delete(*self.table.get_children())
        for row in rows:
            self.table.insert("", "end", iid=str(row["order_item_id"]),
                              values=(row["name"], row["manufacturer"],
                                      f"{row['size_value']:g}", row["quantity"],
                                      money(row["unit_price"]), money(row["line_total"])))
        self.total_label.config(text=f"Итого: {money(self.app.order_total(self.order_id))}")

    def selected_item(self):
        sel = self.table.selection()
        return int(sel[0]) if sel else None

    def change_date(self):
        if not self.app.is_admin():
            return
        current = self.app.conn.execute(
            "SELECT order_date FROM orders WHERE order_id = ?",
            (self.order_id,)).fetchone()["order_date"]
        value = simpledialog.askstring(
            "Дата заказа", "Введите дату в формате ГГГГ-ММ-ДД:", initialvalue=current,
            parent=self)
        if not value:
            return
        try:
            date.fromisoformat(value.strip())
        except ValueError:
            messagebox.showerror("Неверная дата",
                                 "Введите дату в формате ГГГГ-ММ-ДД, например 2026-05-15.")
            return
        try:
            self.app.conn.execute(
                "UPDATE orders SET order_date = ? WHERE order_id = ?",
                (value.strip(), self.order_id))
            self.app.conn.commit()
        except sqlite3.Error as err:
            messagebox.showerror("Ошибка базы данных",
                                 f"Не удалось изменить дату: {err}")
            return
        self.on_show(order_id=self.order_id)

    def delete_item(self):
        if not self.app.is_admin():
            return
        item_id = self.selected_item()
        if item_id is None:
            messagebox.showinfo("Выберите позицию", "Выделите строку заказа.")
            return
        if not messagebox.askyesno("Удаление позиции",
                                   "Удалить позицию из заказа? Остаток не вернётся."):
            return
        try:
            self.app.conn.execute(
                "DELETE FROM order_items WHERE order_item_id = ?", (item_id,))
            self.app.conn.commit()
        except sqlite3.Error as err:
            messagebox.showerror("Ошибка базы данных",
                                 f"Не удалось удалить позицию: {err}")
            return
        self.refresh()

    def add_item(self):
        AddItemDialog(self.app, self.order_id, on_done=self.refresh)


class AddItemDialog(tk.Toplevel):
    def __init__(self, app, order_id, on_done):
        super().__init__(app)
        self.app = app
        self.order_id = order_id
        self.on_done = on_done
        self.title("Чудо Обувь — добавить позицию")
        self.geometry("520x300")
        self.transient(app)
        self.grab_set()
        self.products = app.conn.execute(
            "SELECT product_id, name FROM products ORDER BY name").fetchall()
        self.product_map = {p["name"]: p["product_id"] for p in self.products}
        self.sizes_rows = []

        box = ttk.Frame(self, padding=16)
        box.pack(fill="both", expand=True)
        ttk.Label(box, text="Товар:").grid(row=0, column=0, sticky="w", pady=4)
        self.product_var = tk.StringVar()
        self.product_box = ttk.Combobox(box, textvariable=self.product_var,
                                        values=list(self.product_map), state="readonly", width=38)
        self.product_box.grid(row=0, column=1, pady=4)
        self.product_box.bind("<<ComboboxSelected>>", self.load_sizes)
        ttk.Label(box, text="Размер:").grid(row=1, column=0, sticky="w", pady=4)
        self.size_var = tk.StringVar()
        self.size_box = ttk.Combobox(box, textvariable=self.size_var, state="readonly", width=18)
        self.size_box.grid(row=1, column=1, sticky="w", pady=4)
        ttk.Label(box, text="Количество:").grid(row=2, column=0, sticky="w", pady=4)
        self.qty_var = tk.IntVar(value=1)
        ttk.Spinbox(box, from_=1, to=1, textvariable=self.qty_var, width=8).grid(
            row=2, column=1, sticky="w", pady=4)
        ttk.Button(box, text="Добавить", command=self.add).grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=(14, 4))
        ttk.Label(box, text="Цена берётся с учётом скидки 25% на текущую дату.",
                  foreground="#5c6b7a", wraplength=460).grid(
            row=4, column=0, columnspan=2, sticky="w")

    def load_sizes(self, _event=None):
        pid = self.product_map.get(self.product_var.get())
        if pid is None:
            return
        self.sizes_rows = self.app.sizes(pid)
        self.size_box["values"] = [f"{r['size_value']:g}" for r in self.sizes_rows]
        self.size_var.set(self.size_box["values"][0] if self.sizes_rows else "")

    def add(self):
        pid = self.product_map.get(self.product_var.get())
        chosen = None
        for row in self.sizes_rows:
            if f"{row['size_value']:g}" == self.size_var.get():
                chosen = row
                break
        if pid is None or chosen is None:
            messagebox.showerror("Ошибка", "Выберите товар и размер.")
            return
        try:
            qty = int(self.qty_var.get())
        except (ValueError, tk.TclError):
            qty = 0
        if qty < 1 or qty > chosen["quantity"]:
            messagebox.showerror(
                "Неверное количество",
                f"На складе {chosen['quantity']} пар. Введите от 1 до {chosen['quantity']}.")
            return
        price = self.app.final_price(pid, float(self.app.product(pid)["price"]))
        try:
            self.app.conn.execute(
                "INSERT INTO order_items (order_id, item_id, quantity, unit_price) "
                "VALUES (?, ?, ?, ?)", (self.order_id, chosen["item_id"], qty, price))
            self.app.conn.execute(
                "UPDATE product_items SET quantity = quantity - ? WHERE item_id = ?",
                (qty, chosen["item_id"]))
            self.app.conn.commit()
        except sqlite3.Error as err:
            messagebox.showerror("Ошибка базы данных", str(err))
            return
        self.on_done()
        self.destroy()


# ---------------------------------------------------------------------------
# Экран 7. Статистика (Задание 5)
# ---------------------------------------------------------------------------
class StatisticsFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        ttk.Label(self, text="Статистика заказов", style="Title.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 8))
        self.summary = ttk.Label(self, text="", font=("Segoe UI", 11, "bold"))
        self.summary.grid(row=1, column=0, sticky="w", pady=(0, 8))
        self.table = ttk.Treeview(self, columns=("id", "date", "client", "total"),
                                  show="headings")
        for col, title, width in (("id", "№ заказа", 90), ("date", "Дата", 140),
                                  ("client", "ФИО клиента", 360), ("total", "Сумма", 140)):
            self.table.heading(col, text=title)
            self.table.column(col, width=width, anchor="w")
        self.table.grid(row=3, column=0, sticky="nsew")
        ttk.Button(self, text="← Назад в каталог",
                   command=lambda: app.show("catalog")).grid(
            row=4, column=0, sticky="w", pady=8)

    def on_show(self):
        if not self.app.is_staff():
            messagebox.showwarning("Доступ запрещён",
                                   "Статистика доступна Менеджеру и Администратору.")
            self.app.show("catalog")
            return
        stats = self.app.stats()
        self.summary.config(
            text=f"Всего заказов: {stats['orders_count']}   ·   "
                 f"Выручка: {money(stats['revenue'])} ₽   ·   "
                 f"Средний чек: {money(stats['avg_check'])} ₽")
        self.table.delete(*self.table.get_children())
        for row in self.app.order_rows():
            self.table.insert("", "end", values=(row["order_id"], row["order_date"],
                                                 row["client"], money(row["total"])))


if __name__ == "__main__":
    app = App()
    app.mainloop()
