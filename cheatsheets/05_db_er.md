# БД «Корочки.есть»: 6 таблиц, 3НФ, ER

## Схема

```
roles 1──M users 1──M applications M──1 courses
                     │
                     ├──1 reviews
                     └──M application_statuses
```

| Таблица | Поля |
|---|---|
| `roles` | role_id, role_name |
| `users` | user_id, login UNIQUE, password_hash, full_name, phone, email UNIQUE, role_id, created_at |
| `courses` | course_id, title, description, duration_hours, price, image |
| `application_statuses` | status_id, status_name |
| `applications` | application_id, user_id, course_id, start_date, payment_method, status_id, cancel_reason, created_at |
| `reviews` | review_id, application_id UNIQUE, user_id, rating 1–5, review_text, created_at |

## 3НФ

- **1НФ** — атомарные значения, нет списков в ячейке.
- **2НФ** — неключевой атрибут зависит от всего ключа.
- **3НФ** — нет транзитивных зависимостей: статус, курс и роль вынесены
  в справочники, а не хранятся текстом в заявке.

## Ограничения

```sql
login TEXT NOT NULL UNIQUE
email TEXT NOT NULL UNIQUE
payment_method TEXT NOT NULL CHECK (payment_method IN ('cash', 'phone_transfer'))
rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5)
application_id INTEGER NOT NULL UNIQUE REFERENCES applications(application_id)
```

## DDL

```sql
CREATE TABLE applications (
    application_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id        INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    course_id      INTEGER NOT NULL REFERENCES courses(course_id) ON DELETE RESTRICT,
    start_date     TEXT NOT NULL,
    payment_method TEXT NOT NULL CHECK (payment_method IN ('cash', 'phone_transfer')),
    status_id      INTEGER NOT NULL REFERENCES application_statuses(status_id),
    cancel_reason  TEXT,
    created_at     TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_applications_user ON applications(user_id);
CREATE INDEX idx_applications_status ON applications(status_id);
```

## ER-диаграмма

Нарисуй 6 прямоугольников, атрибуты, PK/FK, линии связей и кардинальности
`1` / `M`. Сохрани PDF/PNG и приложи к README.

## Скрипт сдачи

`schema.sql` = `CREATE TABLE` + `INSERT` с демо-данными.
Эксперт должен поднять базу одной командой:

```bash
sqlite3 instance/korochki.db < schema.sql
```
