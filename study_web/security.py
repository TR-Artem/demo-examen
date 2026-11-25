# -*- coding: utf-8 -*-
"""Валидация, пароли, CSRF и доступ."""
from __future__ import annotations

import re
import secrets
from functools import wraps

from flask import abort, current_app, flash, g, redirect, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

LOGIN_RE = re.compile(r"^[A-Za-zА-Яа-яЁё0-9_]{3,}$")


def hash_password(password: str) -> str:
    return generate_password_hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    return check_password_hash(password_hash, password)


def validate_registration(form, users) -> tuple[dict, dict[str, str]]:
    data = {
        "login": (form.get("login") or "").strip(),
        "password": form.get("password") or "",
        "password2": form.get("password2") or "",
    }
    errors: dict[str, str] = {}

    if not LOGIN_RE.fullmatch(data["login"]):
        errors["login"] = "Никнейм: буквы, цифры и _, не менее 3 символов."
    elif users.login_exists(data["login"]):
        errors["login"] = "Такой никнейм уже занят."

    if len(data["password"]) < 8:
        errors["password"] = "Пароль должен содержать не менее 8 символов."
    elif data["password"] != data["password2"]:
        errors["password2"] = "Пароли не совпадают."

    return data, errors


def get_csrf_token() -> str:
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    return session["csrf_token"]


def validate_csrf() -> None:
    if not current_app.config.get("CSRF_ENABLED", True):
        return
    if request.method != "POST":
        return
    token = session.get("csrf_token")
    sent = request.form.get("csrf_token", "")
    if not token or not secrets.compare_digest(token, sent):
        abort(400, description="CSRF-токен недействителен. Обновите форму.")


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if g.user is None:
            flash("Сначала войдите в аккаунт.", "error")
            target = request.path
            if request.query_string:
                target += "?" + request.query_string.decode()
            return redirect(url_for("login", next=target))
        return view(*args, **kwargs)
    return wrapper
