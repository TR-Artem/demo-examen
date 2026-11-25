# -*- coding: utf-8 -*-
"""
Эталонное приложение к ДЭ 09.02.07-2-2026 («Программист»).
Стек: Python + SQLite + tkinter.
Запуск: python app.py
"""
from __future__ import annotations

import sqlite3
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "shop.db"

COLORS = {
    "out": "#B3E5FC",       # нет на складе
    "big": "#2E8B57",       # скидка больше 15%
    "discount": "#c0392b",  # старая цена
}


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    conn = connect()
    has_tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='products'"
    ).fetchone()
    if not has_tables:
        conn.executescript((ROOT / "schema.sql").read_text(encoding="utf-8"))
        conn.commit()
    conn.close()


def dates(value: str) -> str:
    """Принимает ДД.ММ.ГГГГ или YYYY-MM-DD, возвращает YYYY-MM-DD."""
    from datetime import datetime
    value = (value or "").strip()
    for fmt in ("%d.%m.%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            pass
    return ""


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Магазин обуви — ДЭ 09.02.07-2")
        self.geometry("1180x720")
        self.minsize(980, 600)
        self.conn = connect()
        self.user: dict | None = None
        self.product_form: ProductForm | None = None
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.show_login()

    # -- навигация -----------------------------------------------------
    def clear(self) -> None:
        for child in self.container.winfo_children():
            child.destroy()

    def show_login(self) -> None:
        self.clear()
        LoginFrame(self.container, self).pack(fill="both", expand=True)

    def show_catalog(self) -> None:
        self.clear()
        CatalogFrame(self.container, self).pack(fill="both", expand=True)

    def show_orders(self) -> None:
        self.clear()
        OrdersFrame(self.container, self).pack(fill="both", expand=True)

    def logout(self) -> None:
        self.user = None
        self.show_login()

    def on_close(self) -> None:
        try:
            self.conn.close()
        finally:
            self.destroy()


class LoginFrame(ttk.Frame):
    def __init__(self, parent, app: App):
        super().__init__(parent, padding=40)
        self.app = app

        card = ttk.Frame(self, padding=28)
        card.place(relx=.5, rely=.45, anchor="center")
        ttk.Label(card, text="Магазин обуви", font=("Segoe UI", 20, "bold")).pack()
        ttk.Label(card, text="Вход в систему", foreground="#666").pack(pady=(2, 18))

        ttk.Label(card, text="Логин").pack(anchor="w")
        self.login = ttk.Entry(card, width=34)
        self.login.pack(fill="x", pady=(2, 8))
        ttk.Label(card, text="Пароль").pack(anchor="w")
        self.password = ttk.Entry(card, width=34, show="*")
        self.password.pack(fill="x", pady=(2, 14))

        ttk.Button(card, text="Войти", command=self.do_login).pack(fill="x")
        ttk.Button(card, text="Гость", command=self.do_guest).pack(fill="x", pady=6)
        ttk.Label(card, text="admin / admin123   ·   manager / manager123",
                  foreground="#777").pack(pady=(12, 0))

    def do_login(self) -> None:
        row = self.app.conn.execute(
            "SELECT u.user_id, u.full_name, u.role_id, r.role_name "
            "FROM users u JOIN roles r ON r.role_id = u.role_id "
            "WHERE u.login = ? AND u.password = ?",
            (self.login.get().strip(), self.password.get()),
        ).fetchone()
        if row is None:
            messagebox.showerror(
                "Ошибка входа",
                "Неверный логин или пароль. Проверьте раскладку и попробуйте снова.")
            return
        self.app.user = dict(row)
        self.app.show_catalog()

    def do_guest(self) -> None:
        self.app.user = {"user_id": None, "full_name": "Гость", "role_id": 0,
                         "role_name": "Гость"}
        self.app.show_catalog()


class CatalogFrame(ttk.Frame):
    def __init__(self, parent, app: App):
        super().__init__(parent, padding=10)
        self.app = app
        role = app.user["role_id"]
        self.can_filter = role in (1, 2)
        self.is_admin = role == 1

        top = ttk.Frame(self)
        top.pack(fill="x", pady=(0, 8))
        ttk.Label(top, text="Каталог товаров", font=("Segoe UI", 15, "bold")).pack(side="left")
        ttk.Label(top, text=f"{app.user['full_name']} · {app.user['role_name']}",
                  foreground="#666").pack(side="left", padx=16)
        ttk.Button(top, text="Выйти", command=app.logout).pack(side="right")
        if role in (1, 2):
            ttk.Button(top, text="Заказы", command=app.show_orders).pack(side="right", padx=6)
        if self.is_admin:
            ttk.Button(top, text="Добавить товар", command=self.add_product).pack(side="right", padx=6)

        bar = ttk.Frame(self)
        bar.pack(fill="x", pady=4)
        ttk.Label(bar, text="Поиск").pack(side="left")
        self.search = tk.StringVar()
        search_entry = ttk.Entry(bar, textvariable=self.search, width=34)
        search_entry.pack(side="left", padx=(4, 12))
        ttk.Label(bar, text="Поставщик").pack(side="left")
        self.supplier = tk.StringVar(value="Все поставщики")
        self.supplier_box = ttk.Combobox(bar, textvariable=self.supplier, state="readonly", width=24)
        self.supplier_box.pack(side="left", padx=(4, 12))
        ttk.Label(bar, text="Сортировка").pack(side="left")
        self.order = tk.StringVar(value="По остатку ↑")
        ttk.Combobox(bar, textvariable=self.order, state="readonly", width=18,
                     values=("По остатку ↑", "По остатку ↓")).pack(side="left", padx=4)

        if not self.can_filter:
            search_entry.state(["disabled"])
            self.supplier_box.state(["disabled"])
            ttk.Label(bar, text="(гостю доступен только просмотр)",
                      foreground="#777").pack(side="left", padx=8)

        columns = ("article", "name", "category", "manufacturer", "supplier",
                   "price", "unit", "qty", "discount", "photo")
        self.table = ttk.Treeview(self, columns=columns, show="headings", height=18)
        titles = ("Артикул", "Наименование", "Категория", "Производитель",
                  "Поставщик", "Цена", "Ед.", "Остаток", "Скидка", "Фото")
        widths = (90, 220, 120, 120, 150, 150, 70, 80, 80, 70)
        for col, title, width in zip(columns, titles, widths):
            self.table.heading(col, text=title)
            self.table.column(col, width=width, anchor="w")
        self.table.tag_configure("out", background=COLORS["out"])
        self.table.tag_configure("big", background=COLORS["big"])
        self.table.tag_configure("discount", foreground=COLORS["discount"])
        self.table.pack(fill="both", expand=True, pady=6)
        self.table.bind("<Double-1>", lambda _e: self.edit_product())

        bottom = ttk.Frame(self)
        bottom.pack(fill="x")
        if self.is_admin:
            ttk.Button(bottom, text="Редактировать", command=self.edit_product).pack(side="left")
            ttk.Button(bottom, text="Удалить", command=self.delete_product).pack(side="left", padx=6)
        ttk.Label(bottom, text="Двойной щелчок — редактирование (администратор).",
                  foreground="#777").pack(side="left", padx=10)

        self.load_suppliers()
        self.search.trace_add("write", lambda *_: self.refresh())
        self.supplier.trace_add("write", lambda *_: self.refresh())
        self.order.trace_add("write", lambda *_: self.refresh())
        self.refresh()

    def load_suppliers(self) -> None:
        rows = self.app.conn.execute(
            "SELECT supplier_name FROM suppliers ORDER BY supplier_name").fetchall()
        self.supplier_box["values"] = ["Все поставщики"] + [r["supplier_name"] for r in rows]

    def refresh(self) -> None:
        if not self.can_filter:
            text, supplier, order = "", "Все поставщики", "ASC"
        else:
            text = self.search.get().strip()
            supplier = self.supplier.get()
            order = "DESC" if "↓" in self.order.get() else "ASC"

        sql = (
            "SELECT p.product_id, p.article, p.name, c.category_name, "
            "m.manufacturer_name, s.supplier_name, p.price, u.unit_name, "
            "p.quantity, p.discount, p.image_path "
            "FROM products p "
            "JOIN categories c ON c.category_id = p.category_id "
            "JOIN manufacturers m ON m.manufacturer_id = p.manufacturer_id "
            "JOIN suppliers s ON s.supplier_id = p.supplier_id "
            "JOIN units u ON u.unit_id = p.unit_id WHERE 1=1"
        )
        params: list = []
        if text:
            sql += (" AND (p.name LIKE ? OR p.description LIKE ? "
                    "OR m.manufacturer_name LIKE ? OR s.supplier_name LIKE ?)")
            params += [f"%{text}%"] * 4
        if supplier != "Все поставщики":
            sql += " AND s.supplier_name = ?"
            params.append(supplier)
        sql += f" ORDER BY p.quantity {order}, p.product_id"
        rows = self.app.conn.execute(sql, params).fetchall()

        self.table.delete(*self.table.get_children())
        for row in rows:
            discount = row["discount"] or 0
            final = row["price"] * (1 - discount)
            price = (f"{row['price']:.2f}" if not discount
                     else f"{row['price']:.2f} → {final:.2f}")
            tags = []
            if row["quantity"] == 0:
                tags.append("out")
            if discount > 0:
                tags.append("discount")
            if discount > 0.15:
                tags.append("big")
            self.table.insert("", "end", iid=row["product_id"], values=(
                row["article"], row["name"], row["category_name"],
                row["manufacturer_name"], row["supplier_name"], price,
                row["unit_name"], row["quantity"],
                f"{discount * 100:.0f}%", "есть" if row["image_path"] else "нет",
            ), tags=tuple(tags))

    def selected_id(self) -> int | None:
        selected = self.table.selection()
        return int(selected[0]) if selected else None

    def add_product(self) -> None:
        if self.app.product_form is not None:
            messagebox.showwarning("Форма уже открыта",
                                   "Закройте текущее окно редактирования товара.")
            return
        self.app.product_form = ProductForm(self.app, None)

    def edit_product(self) -> None:
        if not self.is_admin:
            return
        product_id = self.selected_id()
        if product_id is None:
            messagebox.showinfo("Товар", "Выберите товар в списке.")
            return
        if self.app.product_form is not None:
            messagebox.showwarning("Форма уже открыта",
                                   "Закройте текущее окно редактирования товара.")
            return
        self.app.product_form = ProductForm(self.app, product_id)

    def delete_product(self) -> None:
        product_id = self.selected_id()
        if product_id is None:
            messagebox.showinfo("Товар", "Выберите товар в списке.")
            return
        used = self.app.conn.execute(
            "SELECT 1 FROM orders WHERE product_id = ?", (product_id,)).fetchone()
        if used:
            messagebox.showwarning(
                "Удаление запрещено",
                "Товар присутствует в заказе. Сначала удалите или измените заказ.")
            return
        if not messagebox.askyesno("Удаление", "Удалить товар без возможности восстановления?"):
            return
        self.app.conn.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
        self.app.conn.commit()
        self.refresh()


class ProductForm(tk.Toplevel):
    def __init__(self, app: App, product_id: int | None):
        super().__init__(app)
        self.app = app
        self.product_id = product_id
        self.title("Редактирование товара" if product_id else "Добавление товара")
        self.geometry("560x620")
        self.transient(app)
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.values: dict[str, ttk.Combobox] = {}
        form = ttk.Frame(self, padding=16)
        form.pack(fill="both", expand=True)

        self.id_label = ttk.Label(form, text="")
        self.id_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        fields = [
            ("article", "Артикул"), ("name", "Наименование"),
        ]
        row = 1
        for key, label in fields:
            ttk.Label(form, text=label).grid(row=row, column=0, sticky="w", pady=3)
            entry = ttk.Entry(form, width=38)
            entry.grid(row=row, column=1, sticky="ew", pady=3)
            setattr(self, key, entry)
            row += 1

        ttk.Label(form, text="Категория").grid(row=row, column=0, sticky="w", pady=3)
        self.category = ttk.Combobox(form, state="readonly", width=36)
        self.category.grid(row=row, column=1, sticky="ew", pady=3); row += 1

        ttk.Label(form, text="Описание").grid(row=row, column=0, sticky="nw", pady=3)
        self.description = tk.Text(form, height=5, width=40, wrap="word")
        self.description.grid(row=row, column=1, sticky="ew", pady=3); row += 1

        for key, label, values in (
            ("manufacturer", "Производитель", self._names("manufacturers", "manufacturer_name")),
            ("supplier", "Поставщик", self._names("suppliers", "supplier_name")),
            ("unit", "Единица измерения", self._names("units", "unit_name")),
        ):
            ttk.Label(form, text=label).grid(row=row, column=0, sticky="w", pady=3)
            box = ttk.Combobox(form, state="readonly", width=36, values=values)
            box.grid(row=row, column=1, sticky="ew", pady=3)
            self.values[key] = box
            row += 1

        for key, label in (("price", "Цена"), ("quantity", "Количество"),
                           ("discount", "Скидка, %")):
            ttk.Label(form, text=label).grid(row=row, column=0, sticky="w", pady=3)
            entry = ttk.Entry(form, width=38)
            entry.grid(row=row, column=1, sticky="ew", pady=3)
            setattr(self, key, entry)
            row += 1

        ttk.Label(form, text="Фото").grid(row=row, column=0, sticky="w", pady=3)
        photo_row = ttk.Frame(form)
        photo_row.grid(row=row, column=1, sticky="ew", pady=3)
        self.image = ttk.Entry(photo_row)
        self.image.pack(side="left", fill="x", expand=True)
        ttk.Button(photo_row, text="...", width=3, command=self.choose_image).pack(side="left")
        row += 1

        buttons = ttk.Frame(form)
        buttons.grid(row=row, column=0, columnspan=2, pady=16, sticky="e")
        ttk.Button(buttons, text="Сохранить", command=self.save).pack(side="left")
        ttk.Button(buttons, text="Отмена", command=self.close).pack(side="left", padx=6)

        form.columnconfigure(1, weight=1)
        self.category["values"] = self._names("categories", "category_name")
        self.load()

    def _names(self, table: str, column: str) -> list[str]:
        return [r[column] for r in self.app.conn.execute(
            f"SELECT {column} FROM {table} ORDER BY {column}")]

    def _id(self, table: str, column: str, name: str) -> int:
        return self.app.conn.execute(
            f"SELECT {column} FROM {table} WHERE {column.replace('_id', '_name')} = ?",
            (name,)).fetchone()[0]

    def load(self) -> None:
        if self.product_id is None:
            self.id_label.config(text="ID: будет вычислен как MAX(product_id) + 1")
            self.values["unit"].set("пара")
            self.discount.insert(0, "0")
            return
        row = self.app.conn.execute(
            "SELECT p.*, c.category_name, m.manufacturer_name, s.supplier_name, u.unit_name "
            "FROM products p JOIN categories c ON c.category_id = p.category_id "
            "JOIN manufacturers m ON m.manufacturer_id = p.manufacturer_id "
            "JOIN suppliers s ON s.supplier_id = p.supplier_id "
            "JOIN units u ON u.unit_id = p.unit_id WHERE p.product_id = ?",
            (self.product_id,)).fetchone()
        if row is None:
            self.close(); return
        self.id_label.config(text=f"ID: {row['product_id']} (только чтение)")
        self.article.insert(0, row["article"])
        self.name.insert(0, row["name"])
        self.category.set(row["category_name"])
        self.description.insert("1.0", row["description"] or "")
        self.values["manufacturer"].set(row["manufacturer_name"])
        self.values["supplier"].set(row["supplier_name"])
        self.values["unit"].set(row["unit_name"])
        self.price.insert(0, f"{row['price']:.2f}")
        self.quantity.insert(0, str(row["quantity"]))
        self.discount.insert(0, f"{row['discount'] * 100:.0f}")
        self.image.insert(0, row["image_path"] or "")

    def choose_image(self) -> None:
        path = filedialog.askopenfilename(
            title="Фото товара", filetypes=[("Изображения", "*.png *.jpg *.jpeg")])
        if path:
            self.image.delete(0, "end")
            self.image.insert(0, path)

    def save(self) -> None:
        article = self.article.get().strip()
        name = self.name.get().strip()
        if not article or not name:
            messagebox.showerror("Ошибка", "Артикул и наименование обязательны.")
            return
        try:
            price = float(self.price.get().replace(",", "."))
            quantity = int(self.quantity.get())
            discount = float(self.discount.get().replace(",", ".")) / 100
            if price < 0 or quantity < 0 or not (0 <= discount <= 1):
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Ошибка", "Цена и количество — неотрицательные числа, скидка — от 0 до 100%.")
            return
        if not self.category.get() or not self.values["manufacturer"].get() \
                or not self.values["supplier"].get() or not self.values["unit"].get():
            messagebox.showerror("Ошибка", "Заполните категорию, производителя, поставщика и единицу.")
            return

        category_id = self._id("categories", "category_id", self.category.get())
        manufacturer_id = self._id("manufacturers", "manufacturer_id",
                                   self.values["manufacturer"].get())
        supplier_id = self._id("suppliers", "supplier_id", self.values["supplier"].get())
        unit_id = self._id("units", "unit_id", self.values["unit"].get())
        data = (article, name, category_id, self.description.get("1.0", "end").strip(),
                manufacturer_id, supplier_id, price, unit_id, quantity, discount,
                self.image.get().strip() or None)

        if self.product_id is None:
            next_id = self.app.conn.execute(
                "SELECT COALESCE(MAX(product_id), 0) + 1 FROM products").fetchone()[0]
            self.app.conn.execute(
                "INSERT INTO products (product_id, article, name, category_id, description, "
                "manufacturer_id, supplier_id, price, unit_id, quantity, discount, image_path) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (next_id, *data))
        else:
            self.app.conn.execute(
                "UPDATE products SET article=?, name=?, category_id=?, description=?, "
                "manufacturer_id=?, supplier_id=?, price=?, unit_id=?, quantity=?, "
                "discount=?, image_path=? WHERE product_id=?", (*data, self.product_id))
        self.app.conn.commit()
        self.close()
        for child in self.app.container.winfo_children():
            if isinstance(child, CatalogFrame):
                child.refresh()

    def close(self) -> None:
        self.app.product_form = None
        self.destroy()


class OrdersFrame(ttk.Frame):
    def __init__(self, parent, app: App):
        super().__init__(parent, padding=10)
        self.app = app
        self.is_admin = app.user["role_id"] == 1

        top = ttk.Frame(self)
        top.pack(fill="x", pady=(0, 8))
        ttk.Label(top, text="Заказы", font=("Segoe UI", 15, "bold")).pack(side="left")
        ttk.Label(top, text=f"{app.user['full_name']} · {app.user['role_name']}",
                  foreground="#666").pack(side="left", padx=16)
        ttk.Button(top, text="Назад в каталог", command=app.show_catalog).pack(side="right")
        if self.is_admin:
            ttk.Button(top, text="Добавить заказ", command=self.add).pack(side="right", padx=6)

        columns = ("id", "article", "status", "point", "order_date", "issue_date")
        self.table = ttk.Treeview(self, columns=columns, show="headings", height=18)
        for col, title, width in zip(columns, ("№", "Артикул", "Статус", "Пункт выдачи",
                                               "Дата заказа", "Дата выдачи"),
                                     (60, 120, 140, 220, 130, 130)):
            self.table.heading(col, text=title)
            self.table.column(col, width=width, anchor="w")
        self.table.pack(fill="both", expand=True, pady=6)
        self.table.bind("<Double-1>", lambda _e: self.edit())

        bottom = ttk.Frame(self)
        bottom.pack(fill="x")
        if self.is_admin:
            ttk.Button(bottom, text="Редактировать", command=self.edit).pack(side="left")
            ttk.Button(bottom, text="Удалить", command=self.delete).pack(side="left", padx=6)
        ttk.Label(bottom, text="Менеджер видит заказы; изменяет только администратор.",
                  foreground="#777").pack(side="left", padx=10)
        self.refresh()

    def refresh(self) -> None:
        rows = self.app.conn.execute(
            "SELECT o.order_id, p.article, st.status_name, pp.address, "
            "o.order_date, o.issue_date FROM orders o "
            "JOIN products p ON p.product_id = o.product_id "
            "JOIN order_statuses st ON st.status_id = o.status_id "
            "JOIN pickup_points pp ON pp.point_id = o.point_id ORDER BY o.order_id"
        ).fetchall()
        self.table.delete(*self.table.get_children())
        for row in rows:
            self.table.insert("", "end", iid=row["order_id"], values=(
                row["order_id"], row["article"], row["status_name"], row["address"],
                row["order_date"], row["issue_date"]))

    def selected_id(self) -> int | None:
        selected = self.table.selection()
        return int(selected[0]) if selected else None

    def add(self) -> None:
        OrderForm(self.app, None, self.refresh)

    def edit(self) -> None:
        if not self.is_admin:
            return
        order_id = self.selected_id()
        if order_id is None:
            messagebox.showinfo("Заказ", "Выберите заказ.")
            return
        OrderForm(self.app, order_id, self.refresh)

    def delete(self) -> None:
        order_id = self.selected_id()
        if order_id is None:
            messagebox.showinfo("Заказ", "Выберите заказ.")
            return
        if not messagebox.askyesno("Удаление", "Удалить заказ?"):
            return
        self.app.conn.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
        self.app.conn.commit()
        self.refresh()


class OrderForm(tk.Toplevel):
    def __init__(self, app: App, order_id: int | None, on_save):
        super().__init__(app)
        self.app = app
        self.order_id = order_id
        self.on_save = on_save
        self.title("Редактирование заказа" if order_id else "Добавление заказа")
        self.geometry("520x360")
        self.transient(app)

        form = ttk.Frame(self, padding=16)
        form.pack(fill="both", expand=True)

        products = self.app.conn.execute(
            "SELECT product_id, article || ' — ' || name AS label FROM products ORDER BY article"
        ).fetchall()
        self.product_map = {r["label"]: r["product_id"] for r in products}
        statuses = [r["status_name"] for r in self.app.conn.execute(
            "SELECT status_name FROM order_statuses ORDER BY status_id")]
        points = [r["address"] for r in self.app.conn.execute(
            "SELECT address FROM pickup_points ORDER BY point_id")]

        ttk.Label(form, text="Товар").grid(row=0, column=0, sticky="w", pady=4)
        self.product = ttk.Combobox(form, state="readonly", width=40, values=list(self.product_map))
        self.product.grid(row=0, column=1, sticky="ew", pady=4)
        ttk.Label(form, text="Статус").grid(row=1, column=0, sticky="w", pady=4)
        self.status = ttk.Combobox(form, state="readonly", width=40, values=statuses)
        self.status.grid(row=1, column=1, sticky="ew", pady=4)
        ttk.Label(form, text="Пункт выдачи").grid(row=2, column=0, sticky="w", pady=4)
        self.point = ttk.Combobox(form, state="readonly", width=40, values=points)
        self.point.grid(row=2, column=1, sticky="ew", pady=4)
        ttk.Label(form, text="Дата заказа (ДД.ММ.ГГГГ)").grid(row=3, column=0, sticky="w", pady=4)
        self.order_date = ttk.Entry(form, width=40)
        self.order_date.grid(row=3, column=1, sticky="ew", pady=4)
        ttk.Label(form, text="Дата выдачи (ДД.ММ.ГГГГ)").grid(row=4, column=0, sticky="w", pady=4)
        self.issue_date = ttk.Entry(form, width=40)
        self.issue_date.grid(row=4, column=1, sticky="ew", pady=4)

        buttons = ttk.Frame(form)
        buttons.grid(row=5, column=0, columnspan=2, sticky="e", pady=16)
        ttk.Button(buttons, text="Сохранить", command=self.save).pack(side="left")
        ttk.Button(buttons, text="Отмена", command=self.destroy).pack(side="left", padx=6)
        form.columnconfigure(1, weight=1)

        self.load()

    def load(self) -> None:
        from datetime import date
        if self.order_id is None:
            self.order_date.insert(0, date.today().strftime("%d.%m.%Y"))
            self.status.set("Новая")
            return
        row = self.app.conn.execute(
            "SELECT o.*, p.article, p.name, st.status_name, pp.address "
            "FROM orders o JOIN products p ON p.product_id = o.product_id "
            "JOIN order_statuses st ON st.status_id = o.status_id "
            "JOIN pickup_points pp ON pp.point_id = o.point_id WHERE o.order_id = ?",
            (self.order_id,)).fetchone()
        if row is None:
            self.destroy(); return
        self.product.set(f"{row['article']} — {row['name']}")
        self.status.set(row["status_name"])
        self.point.set(row["address"])
        self.order_date.insert(0, row["order_date"])
        self.issue_date.insert(0, row["issue_date"])

    def save(self) -> None:
        if not self.product.get() or not self.status.get() or not self.point.get():
            messagebox.showerror("Ошибка", "Выберите товар, статус и пункт выдачи.")
            return
        order_date = dates(self.order_date.get())
        issue_date = dates(self.issue_date.get())
        if not order_date or not issue_date:
            messagebox.showerror("Ошибка", "Даты в формате ДД.ММ.ГГГГ.")
            return
        product_id = self.product_map[self.product.get()]
        status_id = self.app.conn.execute(
            "SELECT status_id FROM order_statuses WHERE status_name = ?",
            (self.status.get(),)).fetchone()[0]
        point_id = self.app.conn.execute(
            "SELECT point_id FROM pickup_points WHERE address = ?",
            (self.point.get(),)).fetchone()[0]
        if self.order_id is None:
            self.app.conn.execute(
                "INSERT INTO orders (product_id, status_id, point_id, order_date, issue_date) "
                "VALUES (?, ?, ?, ?, ?)",
                (product_id, status_id, point_id, order_date, issue_date))
        else:
            self.app.conn.execute(
                "UPDATE orders SET product_id=?, status_id=?, point_id=?, "
                "order_date=?, issue_date=? WHERE order_id=?",
                (product_id, status_id, point_id, order_date, issue_date, self.order_id))
        self.app.conn.commit()
        self.on_save()
        self.destroy()


if __name__ == "__main__":
    init_db()
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
