# -*- coding: utf-8 -*-
"""Пользователи учебного портала."""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    login: str
    password_hash: str
    created_at: str = ""


class UserRepository:
    def __init__(self, db: sqlite3.Connection):
        self.db = db

    def by_login(self, login: str) -> User | None:
        row = self.db.execute(
            "SELECT * FROM users WHERE login = ?", (login,)
        ).fetchone()
        return User(**dict(row)) if row else None

    def by_id(self, user_id: int) -> User | None:
        row = self.db.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
        return User(**dict(row)) if row else None

    def login_exists(self, login: str) -> bool:
        return self.db.execute(
            "SELECT 1 FROM users WHERE login = ?", (login,)
        ).fetchone() is not None

    def create(self, login: str, password_hash: str) -> int:
        cur = self.db.execute(
            "INSERT INTO users (login, password_hash) VALUES (?, ?)",
            (login, password_hash),
        )
        self.db.commit()
        return int(cur.lastrowid)


class ProgressRepository:
    def __init__(self, db: sqlite3.Connection):
        self.db = db

    def for_course(self, user_id: int, course: str) -> dict[tuple[int, int], dict]:
        rows = self.db.execute(
            "SELECT module, step, status, score FROM progress "
            "WHERE user_id = ? AND course = ?",
            (user_id, course),
        ).fetchall()
        return {
            (row["module"], row["step"]): {
                "status": row["status"],
                "score": row["score"],
            }
            for row in rows
        }

    def mark(self, user_id: int, course: str, module: int, step: int,
             score: int | None = None, status: str = "done") -> None:
        self.db.execute(
            "INSERT INTO progress (user_id, course, module, step, status, score) "
            "VALUES (?, ?, ?, ?, ?, ?) "
            "ON CONFLICT(user_id, course, module, step) DO UPDATE SET "
            "status = excluded.status, score = excluded.score, "
            "updated_at = datetime('now')",
            (user_id, course, module, step, status, score),
        )
        self.db.commit()

    def practical_for_course(self, user_id: int, course: str) -> set[tuple[int, int, str]]:
        rows = self.db.execute(
            "SELECT module, step, task_id FROM practical_progress "
            "WHERE user_id = ? AND course = ?",
            (user_id, course),
        ).fetchall()
        return {(row["module"], row["step"], row["task_id"]) for row in rows}

    def mark_practical(self, user_id: int, course: str, module: int,
                       step: int, task_id: str) -> None:
        self.db.execute(
            "INSERT INTO practical_progress "
            "(user_id, course, module, step, task_id) VALUES (?, ?, ?, ?, ?) "
            "ON CONFLICT(user_id, course, module, step, task_id) DO UPDATE SET "
            "updated_at = datetime('now')",
            (user_id, course, module, step, task_id),
        )
        self.db.commit()
