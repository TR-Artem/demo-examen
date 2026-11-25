# -*- coding: utf-8 -*-
"""SQLite для учебного портала."""
from __future__ import annotations

import sqlite3
from pathlib import Path

from flask import current_app, g

from seed import seed


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_error=None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    db = get_db()
    db.executescript((Path(__file__).parent / "schema.sql").read_text(encoding="utf-8"))
    seed(db)
    db.commit()


def init_app(app) -> None:
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()
