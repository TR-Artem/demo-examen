# -*- coding: utf-8 -*-
"""Модели и репозитории: слой доступа к данным (ООП)."""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    login: str
    password_hash: str
    full_name: str
    phone: str
    email: str
    role_id: int
    created_at: str = ""

    @property
    def is_admin(self) -> bool:
        return self.role_id == 1


@dataclass
class Course:
    course_id: int
    title: str
    description: str
    duration_hours: int
    price: float
    image: str


@dataclass
class Application:
    application_id: int
    user_id: int
    course_id: int
    start_date: str
    payment_method: str
    status_id: int
    cancel_reason: str | None
    created_at: str
    course_title: str = ""
    course_price: float = 0.0
    course_duration: int = 0
    status_name: str = ""
    user_full_name: str = ""
    user_phone: str = ""
    user_email: str = ""
    review_id: int | None = None
    review_rating: int | None = None

    @property
    def payment_label(self) -> str:
        return "Наличными" if self.payment_method == "cash" else "Переводом по телефону"

    @property
    def can_review(self) -> bool:
        return self.status_id == 3 and self.review_id is None


def _user(row: sqlite3.Row) -> User:
    return User(**dict(row))


def _course(row: sqlite3.Row) -> Course:
    return Course(**dict(row))


def _application(row: sqlite3.Row) -> Application:
    data = dict(row)
    known = {field for field in Application.__dataclass_fields__}
    return Application(**{key: value for key, value in data.items() if key in known})


class UserRepository:
    def __init__(self, db: sqlite3.Connection):
        self.db = db

    def by_login(self, login: str) -> User | None:
        row = self.db.execute(
            "SELECT * FROM users WHERE login = ?", (login,)
        ).fetchone()
        return _user(row) if row else None

    def by_id(self, user_id: int) -> User | None:
        row = self.db.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
        return _user(row) if row else None

    def login_exists(self, login: str) -> bool:
        return self.db.execute(
            "SELECT 1 FROM users WHERE login = ?", (login,)
        ).fetchone() is not None

    def email_exists(self, email: str) -> bool:
        return self.db.execute(
            "SELECT 1 FROM users WHERE email = ?", (email,)
        ).fetchone() is not None

    def create(self, login: str, password_hash: str) -> int:
        cur = self.db.execute(
            "INSERT INTO users (login, password_hash, full_name, phone, email, role_id) "
            "VALUES (?, ?, ?, '', ?, 2)",
            (login, password_hash, login, f"{login}@local"),
        )
        self.db.commit()
        return int(cur.lastrowid)


class CourseRepository:
    def __init__(self, db: sqlite3.Connection):
        self.db = db

    def all(self) -> list[Course]:
        rows = self.db.execute(
            "SELECT * FROM courses ORDER BY course_id"
        ).fetchall()
        return [_course(row) for row in rows]

    def by_id(self, course_id: int) -> Course | None:
        row = self.db.execute(
            "SELECT * FROM courses WHERE course_id = ?", (course_id,)
        ).fetchone()
        return _course(row) if row else None


class ApplicationRepository:
    _base = """
        SELECT a.*, c.title AS course_title, c.price AS course_price,
               c.duration_hours AS course_duration, s.status_name,
               u.full_name AS user_full_name, u.phone AS user_phone,
               u.email AS user_email,
               r.review_id, r.rating AS review_rating
        FROM applications a
        JOIN courses c ON c.course_id = a.course_id
        JOIN application_statuses s ON s.status_id = a.status_id
        JOIN users u ON u.user_id = a.user_id
        LEFT JOIN reviews r ON r.application_id = a.application_id
    """

    def __init__(self, db: sqlite3.Connection):
        self.db = db

    def for_user(self, user_id: int) -> list[Application]:
        rows = self.db.execute(
            self._base + " WHERE a.user_id = ? ORDER BY a.created_at DESC, a.application_id DESC",
            (user_id,),
        ).fetchall()
        return [_application(row) for row in rows]

    def by_id(self, application_id: int) -> Application | None:
        row = self.db.execute(
            self._base + " WHERE a.application_id = ?", (application_id,)
        ).fetchone()
        return _application(row) if row else None

    def create(self, user_id: int, course_id: int, start_date: str,
               payment_method: str) -> int:
        cur = self.db.execute(
            "INSERT INTO applications "
            "(user_id, course_id, start_date, payment_method, status_id) "
            "VALUES (?, ?, ?, ?, 1)",
            (user_id, course_id, start_date, payment_method),
        )
        self.db.commit()
        return int(cur.lastrowid)

    def update_status(self, application_id: int, status_id: int,
                      cancel_reason: str | None) -> None:
        self.db.execute(
            "UPDATE applications SET status_id = ?, cancel_reason = ? "
            "WHERE application_id = ?",
            (status_id, cancel_reason, application_id),
        )
        self.db.commit()

    def admin_page(self, status_id: int | None = None, query: str = "",
                   page: int = 1, per_page: int = 8) -> tuple[list[Application], int]:
        where, params = [], []
        if status_id:
            where.append("a.status_id = ?")
            params.append(status_id)
        if query:
            where.append("(u.full_name LIKE ? OR u.phone LIKE ? OR c.title LIKE ?)")
            like = f"%{query}%"
            params.extend([like, like, like])
        clause = ("WHERE " + " AND ".join(where)) if where else ""

        total = self.db.execute(
            "SELECT COUNT(*) FROM applications a "
            "JOIN users u ON u.user_id = a.user_id "
            "JOIN courses c ON c.course_id = a.course_id " + clause,
            params,
        ).fetchone()[0]

        rows = self.db.execute(
            self._base + clause +
            " ORDER BY a.created_at DESC, a.application_id DESC LIMIT ? OFFSET ?",
            params + [per_page, max(page - 1, 0) * per_page],
        ).fetchall()
        return [_application(row) for row in rows], int(total)

    def counts_by_status(self) -> dict[str, int]:
        rows = self.db.execute(
            "SELECT s.status_name, COUNT(a.application_id) AS cnt "
            "FROM application_statuses s "
            "LEFT JOIN applications a ON a.status_id = s.status_id "
            "GROUP BY s.status_id, s.status_name ORDER BY s.status_id"
        ).fetchall()
        return {row["status_name"]: row["cnt"] for row in rows}

    def revenue(self) -> float:
        row = self.db.execute(
            "SELECT COALESCE(SUM(c.price), 0) AS total "
            "FROM applications a JOIN courses c ON c.course_id = a.course_id "
            "WHERE a.status_id = 3"
        ).fetchone()
        return float(row["total"])


class ReviewRepository:
    def __init__(self, db: sqlite3.Connection):
        self.db = db

    def exists(self, application_id: int) -> bool:
        return self.db.execute(
            "SELECT 1 FROM reviews WHERE application_id = ?", (application_id,)
        ).fetchone() is not None

    def create(self, application_id: int, user_id: int,
               rating: int, text: str) -> None:
        self.db.execute(
            "INSERT INTO reviews (application_id, user_id, rating, review_text) "
            "VALUES (?, ?, ?, ?)",
            (application_id, user_id, rating, text),
        )
        self.db.commit()
