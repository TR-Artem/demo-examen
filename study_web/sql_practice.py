# -*- coding: utf-8 -*-
"""Проверка SQL-практики на встроенной SQLite."""
from __future__ import annotations

import sqlite3


def _norm(rows):
    out = []
    for row in rows:
        clean = []
        for value in row:
            if isinstance(value, float):
                value = round(value, 2)
            elif value is None:
                value = ""
            elif isinstance(value, str):
                value = value.strip()
            clean.append(value)
        out.append(tuple(clean))
    return out


def _fetch(con, sql):
    cur = con.execute(sql)
    rows = _norm(cur.fetchall())
    cols = [d[0] for d in cur.description] if cur.description else []
    return cols, rows


def _equal(left, right) -> bool:
    if len(left) != len(right):
        return False
    for row_a, row_b in zip(left, right):
        if len(row_a) != len(row_b):
            return False
        for a, b in zip(row_a, row_b):
            if isinstance(a, float) and isinstance(b, float):
                if abs(a - b) > 0.011:
                    return False
            elif a != b:
                return False
    return True


def check(module, task, user_sql: str):
    """Возвращает (ok, error, actual, expected)."""
    user_sql = (user_sql or "").strip()
    if not user_sql:
        return False, "Напишите SQL-запрос.", [], []

    schema = task.get("schema_sql", module.SCHEMA_SQL)
    try:
        ref = sqlite3.connect(":memory:")
        ref.executescript(schema)
        if task.get("mode") == "script":
            ref.executescript(task["expected"])
            expected_cols, expected = _fetch(ref, task["verify"])
        else:
            expected_cols, expected = _fetch(ref, task["expected"])
        ref.close()

        con = sqlite3.connect(":memory:")
        con.executescript(schema)
        if task.get("mode") == "script":
            con.executescript(user_sql)
            actual_cols, actual = _fetch(con, task["verify"])
        else:
            actual_cols, actual = _fetch(con, user_sql)
        con.close()
    except sqlite3.Error as err:
        return False, f"Ошибка SQL: {err}", [], []

    return _equal(actual, expected), None, actual, expected
