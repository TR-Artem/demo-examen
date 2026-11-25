# -*- coding: utf-8 -*-
"""Демонстрационные данные портала «Корочки.есть»."""
from __future__ import annotations

import sqlite3

from werkzeug.security import generate_password_hash


COURSES = [
    ("Основы алгоритмизации и программирования",
     "Логика, блок-схемы, базовые конструкции и первые программы.", 72, 12000, "slide-1.svg"),
    ("Основы веб-дизайна",
     "Композиция, цвет, типографика, макеты и адаптивные интерфейсы.", 48, 9000, "slide-2.svg"),
    ("Основы проектирования баз данных",
     "Модели данных, нормализация, ER-диаграммы, SQL и ограничения.", 64, 11000, "slide-3.svg"),
]

USERS = [
    ("Admin", "KorokNET", "Администратор портала",
     "8(900)000-00-00", "admin@korochki.ru", 1),
    ("demo01", "password123", "Демо Пользователь",
     "8(921)111-11-11", "demo@example.ru", 2),
    ("ivanov01", "password123", "Иванов Иван Иванович",
     "8(921)222-22-22", "ivanov@example.ru", 2),
    ("petrova02", "password123", "Петрова Анна Сергеевна",
     "8(921)333-33-33", "petrova@example.ru", 2),
    ("sidorov03", "password123", "Сидоров Пётр Алексеевич",
     "8(812)444-44-44", "sidorov@example.ru", 2),
]

# user_login, course_index, start_date, payment, status_id, cancel_reason, created_offset
APPLICATIONS = [
    ("demo01", 0, "+14 days", "cash", 1, None, "-75 days"),
    ("ivanov01", 1, "+7 days", "phone_transfer", 2, None, "-70 days"),
    ("petrova02", 2, "-20 days", "cash", 3, None, "-45 days"),
    ("sidorov03", 0, "-60 days", "phone_transfer", 3, None, "-40 days"),
    ("demo01", 3, "-10 days", "cash", 4, "Не подошло расписание", "-20 days"),
    ("ivanov01", 4, "+21 days", "cash", 1, None, "-15 days"),
    ("petrova02", 1, "-5 days", "cash", 3, None, "-10 days"),
    ("sidorov03", 2, "+3 days", "phone_transfer", 2, None, "-5 days"),
    ("demo01", 5, "-30 days", "phone_transfer", 3, None, "-2 days"),
    ("ivanov01", 3, "+30 days", "cash", 1, None, "0 days"),
    ("petrova02", 4, "-45 days", "cash", 4, "Нет свободных мест", "-50 days"),
    ("sidorov03", 5, "-15 days", "cash", 3, None, "-25 days"),
    ("demo01", 0, "+10 days", "phone_transfer", 2, None, "-35 days"),
    ("ivanov01", 2, "-2 days", "cash", 1, None, "-12 days"),
]

# application_index (1-based), rating, text, created_offset
REVIEWS = [
    (3, 5, "Отличный курс, много практики по проектированию БД.", "-15 days"),
    (4, 4, "Понятно объясняют алгоритмы, но мало домашних заданий.", "-20 days"),
    (7, 5, "Веб-дизайн — лучший курс, сразу применил на проекте.", "-3 days"),
    (9, 3, "Материал полезный, однако темп слишком быстрый.", "-1 days"),
    (12, 4, "Хорошее введение в безопасность, пригодилось на работе.", "-8 days"),
]


def seed(conn: sqlite3.Connection) -> None:
    """Заполняет пустую БД демо-данными."""
    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]:
        return

    conn.executemany(
        "INSERT INTO roles (role_id, role_name) VALUES (?, ?)",
        [(1, "Администратор"), (2, "Пользователь")],
    )

    for login, password, full_name, phone, email, role_id in USERS:
        conn.execute(
            "INSERT INTO users (login, password_hash, full_name, phone, email, role_id) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (login, generate_password_hash(password), full_name, phone, email, role_id),
        )

    conn.executemany(
        "INSERT INTO courses (title, description, duration_hours, price, image) "
        "VALUES (?, ?, ?, ?, ?)",
        COURSES,
    )

    conn.executemany(
        "INSERT INTO application_statuses (status_id, status_name) VALUES (?, ?)",
        [(1, "Новая"), (2, "Идет обучение"), (3, "Обучение завершено"), (4, "Отменена")],
    )

    user_ids = {
        row["login"]: row["user_id"]
        for row in conn.execute("SELECT user_id, login FROM users")
    }
    course_ids = [
        row["course_id"]
        for row in conn.execute("SELECT course_id FROM courses ORDER BY course_id")
    ]

    for login, course_index, start, payment, status_id, reason, created in APPLICATIONS:
        conn.execute(
            "INSERT INTO applications "
            "(user_id, course_id, start_date, payment_method, status_id, "
            " cancel_reason, created_at) "
            "VALUES (?, ?, date('now', ?), ?, ?, ?, datetime('now', ?))",
            (user_ids[login], course_ids[course_index % len(course_ids)], start, payment,
             status_id, reason, created),
        )

    application_ids = [
        row["application_id"]
        for row in conn.execute("SELECT application_id FROM applications ORDER BY application_id")
    ]
    user_of_application = {
        row["application_id"]: row["user_id"]
        for row in conn.execute("SELECT application_id, user_id FROM applications")
    }

    for app_number, rating, text, created in REVIEWS:
        application_id = application_ids[app_number - 1]
        conn.execute(
            "INSERT INTO reviews "
            "(application_id, user_id, rating, review_text, created_at) "
            "VALUES (?, ?, ?, ?, datetime('now', ?))",
            (application_id, user_of_application[application_id], rating, text, created),
        )

    conn.commit()


if __name__ == "__main__":
    import sys
    from pathlib import Path

    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("instance/korochki.db")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    con.executescript(Path("schema.sql").read_text(encoding="utf-8"))
    seed(con)
    con.close()
    print(f"База создана: {db_path}")
