# -*- coding: utf-8 -*-
"""Демо-аккаунт учебного портала."""
from __future__ import annotations

import sqlite3

from werkzeug.security import generate_password_hash


def seed(conn: sqlite3.Connection) -> None:
    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]:
        return
    conn.execute(
        "INSERT INTO users (login, password_hash) VALUES (?, ?)",
        ("student", generate_password_hash("password123")),
    )
    conn.commit()
