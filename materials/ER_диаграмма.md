# ER-диаграмма «Корочки.есть» (6 таблиц)

Скопируй код в **mermaid.live** или в **draw.io**
(`Extras → Edit Diagram → вставить Mermaid → Apply`),
затем `File → Export as → PDF`.

```mermaid
erDiagram
    ROLES ||--o{ USERS : "роль"
    USERS ||--o{ APPLICATIONS : "создаёт"
    COURSES ||--o{ APPLICATIONS : "выбран"
    APPLICATION_STATUSES ||--o{ APPLICATIONS : "статус"
    APPLICATIONS ||--o| REVIEWS : "отзыв"
    USERS ||--o{ REVIEWS : "пишет"

    ROLES {
        int role_id PK
        string role_name
    }
    USERS {
        int user_id PK
        string login UK
        string password_hash
        string full_name
        string phone
        string email UK
        int role_id FK
        string created_at
    }
    COURSES {
        int course_id PK
        string title
        string description
        int duration_hours
        real price
        string image
    }
    APPLICATION_STATUSES {
        int status_id PK
        string status_name
    }
    APPLICATIONS {
        int application_id PK
        int user_id FK
        int course_id FK
        string start_date
        string payment_method
        int status_id FK
        string cancel_reason
        string created_at
    }
    REVIEWS {
        int review_id PK
        int application_id FK "UNIQUE"
        int user_id FK
        int rating
        string review_text
        string created_at
    }
```

## Что проверить на защите

- 6 таблиц, 3НФ;
- PK/FK, `UNIQUE` на `login`, `email`, `reviews.application_id`;
- `CHECK` на оплату и рейтинг;
- кардинальности `1` и `M`;
- подписи связей;
- PDF/PNG приложен к README.
