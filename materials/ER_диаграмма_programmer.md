# ER-диаграмма «Магазин обуви» (09.02.07-2, КОД 2026)

Скопируй код в **mermaid.live** или **draw.io**
(`Extras → Edit Diagram → вставить Mermaid → Apply`),
затем `File → Export as → PDF`.

```mermaid
erDiagram
    ROLES ||--o{ USERS : "роль"
    CATEGORIES ||--o{ PRODUCTS : "категория"
    MANUFACTURERS ||--o{ PRODUCTS : "производитель"
    SUPPLIERS ||--o{ PRODUCTS : "поставщик"
    UNITS ||--o{ PRODUCTS : "единица"
    PRODUCTS ||--o{ ORDERS : "заказ"
    ORDER_STATUSES ||--o{ ORDERS : "статус"
    PICKUP_POINTS ||--o{ ORDERS : "пункт выдачи"

    ROLES {
        int role_id PK
        string role_name
    }
    USERS {
        int user_id PK
        string login UK
        string password
        string full_name
        int role_id FK
    }
    CATEGORIES {
        int category_id PK
        string category_name
    }
    MANUFACTURERS {
        int manufacturer_id PK
        string manufacturer_name
    }
    SUPPLIERS {
        int supplier_id PK
        string supplier_name
    }
    UNITS {
        int unit_id PK
        string unit_name
    }
    PICKUP_POINTS {
        int point_id PK
        string address
    }
    ORDER_STATUSES {
        int status_id PK
        string status_name
    }
    PRODUCTS {
        int product_id PK
        string article UK
        string name
        int category_id FK
        string description
        int manufacturer_id FK
        int supplier_id FK
        real price
        int unit_id FK
        int quantity
        real discount
        string image_path
    }
    ORDERS {
        int order_id PK
        int product_id FK
        int status_id FK
        int point_id FK
        date order_date
        date issue_date
    }
```

## Что проверить

- 10 таблиц, 3НФ;
- PK/FK и `UNIQUE(article)`;
- `CHECK(price >= 0)`, `CHECK(quantity >= 0)`, `CHECK(discount 0..1)`;
- кардинальности `1` и `M`;
- PDF приложен к README.
