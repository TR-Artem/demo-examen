# ER-диаграмма «Чудо Обувь» (8 таблиц)

Скопируй код ниже в **mermaid.live** или в **draw.io**:
`Extras → Edit Diagram → вставить Mermaid → Apply`, затем
`File → Export as → PDF`.

```mermaid
erDiagram
    ROLES ||--o{ USERS : "роль"
    CATEGORIES ||--o{ PRODUCTS : "категория"
    PRODUCTS ||--o{ PRODUCT_ITEMS : "позиции"
    SIZES ||--o{ PRODUCT_ITEMS : "размер"
    USERS ||--o{ ORDERS : "оформляет"
    ORDERS ||--o{ ORDER_ITEMS : "содержит"
    PRODUCT_ITEMS ||--o{ ORDER_ITEMS : "заказано"

    ROLES {
        int role_id PK
        string role_name
    }
    CATEGORIES {
        int category_id PK
        string category_name
    }
    SIZES {
        int size_id PK
        real size_value
    }
    USERS {
        int user_id PK
        string last_name
        string first_name
        string middle_name
        string login
        int role_id FK
    }
    PRODUCTS {
        int product_id PK
        int category_id FK
        string subcategory
        string name
        string manufacturer
        string description
        string composition
        string image_path
        real price
    }
    PRODUCT_ITEMS {
        int item_id PK
        int product_id FK
        int size_id FK
        int quantity
    }
    ORDERS {
        int order_id PK
        date order_date
        int user_id FK
    }
    ORDER_ITEMS {
        int order_item_id PK
        int order_id FK
        int item_id FK
        int quantity
        real unit_price
    }
```

## Чек-лист перед экспортом

- [ ] все 8 таблиц;
- [ ] атрибуты;
- [ ] PK и FK;
- [ ] связи 1:M;
- [ ] согласованные имена;
- [ ] экспорт **в PDF** (не PNG);
- [ ] проверить, что текст читается при 100% масштабе.

## Вариант без Mermaid

В draw.io: ` Arrange → Insert → From Text` не нужен — просто нарисуй 8
прямоугольников, подпиши поля, соедини линиями и подпиши связи «1» и «M».
Главное — чтобы эксперт увидел таблицы, атрибуты, ключи и связи.
