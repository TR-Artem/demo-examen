# -*- coding: utf-8 -*-
"""Валидация, CSRF, пароли и декораторы доступа."""
from __future__ import annotations

import re
import secrets
from datetime import datetime
from functools import wraps

from flask import abort, current_app, flash, g, redirect, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

LOGIN_RE = re.compile(r"^[A-Za-zА-Яа-яЁё0-9_]{3,}$")

PAYMENT_METHODS = {"cash", "phone_transfer"}
STATUSES = {
    1: "Новая",
    2: "Идет обучение",
    3: "Обучение завершено",
    4: "Отменена",
}


def hash_password(password: str) -> str:
    return generate_password_hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    return check_password_hash(password_hash, password)


def parse_date(value: str) -> str | None:
    """Принимает ДД.ММ.ГГГГ и YYYY-MM-DD, возвращает ISO или None."""
    value = (value or "").strip()
    for fmt in ("%d.%m.%Y", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            continue
    return None


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


def validate_application(form, courses) -> tuple[dict, dict[str, str]]:
    course_ids = {course.course_id for course in courses}
    data = {
        "course_id": form.get("course_id", type=int),
        "start_date": (form.get("start_date") or "").strip(),
        "payment_method": (form.get("payment_method") or "").strip(),
    }
    errors: dict[str, str] = {}

    if data["course_id"] not in course_ids:
        errors["course_id"] = "Выберите курс из списка."

    parsed = parse_date(data["start_date"])
    if not parsed:
        errors["start_date"] = "Дата в формате ДД.ММ.ГГГГ."
    else:
        data["start_date"] = parsed

    if data["payment_method"] not in PAYMENT_METHODS:
        errors["payment_method"] = "Выберите способ оплаты."

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
            flash("Сначала войдите в систему.", "error")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapper


def admin_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if g.user is None:
            flash("Сначала войдите как администратор.", "error")
            return redirect(url_for("login"))
        if not g.user.is_admin:
            abort(403)
        return view(*args, **kwargs)
    return wrapper
