# tkinter: интерфейс на 25 + 25 + 25 баллов

В КИМ-2027 интерфейс — это Задания 3, 4 и 5 (75 из 100 баллов).

## Экраны и переходы

```python
container = ttk.Frame(root)
container.grid(row=0, column=0, sticky="nsew")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

frames = {}
for key, cls in (("login", LoginFrame), ("catalog", CatalogFrame),
                 ("product", ProductFrame), ("cart", CartFrame),
                 ("orders", OrdersFrame), ("order_view", OrderViewFrame),
                 ("stats", StatisticsFrame)):
    frame = cls(container, app)
    frame.grid(row=0, column=0, sticky="nsew")
    frames[key] = frame

def show(key, **kwargs):
    frames[key].on_show(**kwargs)
    frames[key].tkraise()
    root.title("Чудо Обувь — " + TITLES[key])   # заголовок = назначение
```

«Назад» = `show("catalog")`, выход = `show("login")`.

## Вход только по логину

```python
logins = [r["login"] for r in conn.execute("SELECT login FROM users ORDER BY login")]
combo = ttk.Combobox(parent, values=logins, state="readonly")
# кнопка «Войти» → найти пользователя по login
# кнопка «Без входа» → session.user = None
```

Пароля нет. После входа — ФИО в правом верхнем углу.

## Роли

| Роль | Каталог | Поиск/фильтр | Корзина/заказ | Заказы | Статистика | CRUD |
|---|---|---|---|---|---|---|
| Гость | да | нет | нет | нет | нет | нет |
| Пользователь | да | да | да | нет | нет | нет |
| Менеджер | да | да | да | да | да | заказы |
| Администратор | да | да | да | да | да | всё |

```python
auth = app.user is not None
staff = app.role in ("Менеджер", "Администратор")
admin = app.role == "Администратор"
btn.pack() if staff else btn.pack_forget()
```

## Поиск, фильтр, сортировка в реальном времени

```python
search_var = tk.StringVar()
ttk.Entry(tools, textvariable=search_var).pack()
for var in (search_var, category_var, sort_var):
    var.trace_add("write", lambda *_: refresh())
```

Никакой кнопки «Найти». «Все категории» первым пунктом и сбрасывает фильтр.

## Каталог и подсветка

```python
table = ttk.Treeview(parent, columns=("name", "category", "price", "stock"),
                     show="headings")
table.tag_configure("low_stock", background="#FFB6B6")   # остаток ≤ 3

for row in rows:
    price = row["price"] * (0.75 if row["has_discount"] else 1)
    label = "много" if row["total_qty"] > 5 else "мало"
    tag = "low_stock" if row["total_qty"] <= 3 else ""
    table.insert("", "end",
                 values=(row["name"], row["category_name"], f"{price:.2f}", label),
                 tags=(tag,))
```

## Карточка, размер, корзина

```python
sizes = conn.execute(
    "SELECT pi.item_id, s.size_value, pi.quantity "
    "FROM product_items pi JOIN sizes s ON s.size_id = pi.size_id "
    "WHERE pi.product_id = ? AND pi.quantity > 0 "
    "ORDER BY s.size_value", (product_id,)).fetchall()

size_box["values"] = [f"{s['size_value']:g}" for s in sizes]
# при выборе размера qty_box.config(to=sizes[...]["quantity"])
```

Корзина — список словарей; «Оформить заказ» → транзакция (см. шпаргалку 03).

## Заказы и состав

* список: `№`, дата, ФИО, итог;
* «Состав» → отдельный экран: товар + производство, размер, количество,
  цена за единицу, сумма строки, итог;
* менеджер/админ: добавить/удалить позицию, удалить заказ;
* админ: изменить дату заказа.

## Статистика

```python
summary.config(
    text=f"Всего заказов: {stats['orders_count']}   ·   "
         f"Выручка: {stats['revenue']:.2f} ₽   ·   "
         f"Средний чек: {stats['avg_check']:.2f} ₽")
```

## Сообщения и валидация

```python
messagebox.showerror("Ошибка ввода",
    "Количество должно быть целым числом от 1 до 5. Исправьте поле и повторите.")
messagebox.showwarning("Удаление невозможно",
    "Товар присутствует в заказе. Сначала удалите позицию из заказа.")
messagebox.showinfo("Готово", "Заказ №12 оформлен.")
messagebox.askyesno("Подтверждение", "Удалить заказ №12 вместе с позициями?")
```

Текст — что случилось + что сделать. Заголовок и пиктограмма появляются сами.

## Мелочи, которые стоят баллов

- [ ] Заголовок у каждого окна
- [ ] ФИО справа вверху после входа
- [ ] «Назад» на каждом экране
- [ ] «Все категории» первым
- [ ] поиск по названию **и описанию**
- [ ] поиск + фильтр + сортировка работают совместно
- [ ] «много/мало» и подсветка ≤ 3
- [ ] скидка 25% (цена и в каталоге, и в карточке, и в заказе)
- [ ] размер и количество при добавлении
- [ ] остаток списывается, каталог обновляется
- [ ] комментарии только в неочевидных местах
- [ ] `snake_case`, одна команда в строке
