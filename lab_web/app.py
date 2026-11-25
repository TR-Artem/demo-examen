# -*- coding: utf-8 -*-
"""
Портал онлайн-курсов «Корочки.есть» — эталонный проект к ДЭ
09.02.07 «Разработчик веб и мультимедийных приложений».

Запуск:
    python -m venv venv
    venv\\Scripts\\activate        (Windows)
    source venv/bin/activate       (macOS/Linux)
    pip install -r requirements.txt
    python app.py
"""
from __future__ import annotations

import math
import os
from datetime import datetime
from pathlib import Path

from flask import (Flask, abort, flash, g, jsonify, redirect, render_template,
                   request, session, url_for)

import db
from models import (ApplicationRepository, CourseRepository, ReviewRepository,
                    UserRepository)
from security import (STATUSES, admin_required, get_csrf_token, hash_password,
                      login_required, validate_application, validate_csrf,
                      validate_registration, verify_password)

BASE_DIR = Path(__file__).resolve().parent


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-change-me"),
        DATABASE=os.environ.get("DATABASE", str(BASE_DIR / "instance" / "korochki.db")),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        CSRF_ENABLED=True,
        MAX_CONTENT_LENGTH=2 * 1024 * 1024,
    )
    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)

    db.init_app(app)

    # ------------------------------------------------------------------
    # Контекст запроса
    # ------------------------------------------------------------------
    @app.before_request
    def load_user() -> None:
        user_id = session.get("user_id")
        g.user = None
        if user_id:
            g.user = UserRepository(db.get_db()).by_id(user_id)
            if g.user is None:
                session.clear()

    @app.before_request
    def protect_csrf() -> None:
        validate_csrf()

    @app.context_processor
    def inject_globals() -> dict:
        return {
            "current_user": g.get("user"),
            "csrf_token": get_csrf_token(),
            "statuses": STATUSES,
        }

    # ------------------------------------------------------------------
    # Фильтры Jinja2
    # ------------------------------------------------------------------
    @app.template_filter("date_ru")
    def date_ru(value: str | None) -> str:
        if not value:
            return "—"
        raw = value.split("T")[0].split(" ")[0]
        for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
            try:
                return datetime.strptime(raw, fmt).strftime("%d.%m.%Y")
            except ValueError:
                continue
        return value

    @app.template_filter("money")
    def money(value: float | int | None) -> str:
        number = float(value or 0)
        text = f"{number:,.2f}".replace(",", " ").replace(".", ",")
        return f"{text} ₽"

    @app.template_filter("badge")
    def badge(status_name: str) -> str:
        return {
            "Новая": "badge--new",
            "Идет обучение": "badge--progress",
            "Обучение завершено": "badge--done",
            "Отменена": "badge--cancel",
        }.get(status_name, "badge--new")

    # ------------------------------------------------------------------
    # Публичные страницы
    # ------------------------------------------------------------------
    @app.get("/")
    def index():
        if g.user is None:
            return redirect(url_for("login"))
        return redirect(url_for("admin" if g.user.is_admin else "dashboard"))

    @app.route("/register", methods=["GET", "POST"])
    def register():
        users = UserRepository(db.get_db())
        errors: dict[str, str] = {}
        form: dict = {}
        if request.method == "POST":
            form, errors = validate_registration(request.form, users)
            if not errors:
                users.create(
                    login=form["login"],
                    password_hash=hash_password(form["password"]),
                )
                flash("Регистрация успешна. Войдите в систему.", "success")
                return redirect(url_for("login"))
        return render_template("register.html", errors=errors, form=form)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if g.user is not None:
            return redirect(url_for("admin" if g.user.is_admin else "dashboard"))
        error = None
        login_value = ""
        if request.method == "POST":
            login_value = (request.form.get("login") or "").strip()
            password = request.form.get("password") or ""
            user = UserRepository(db.get_db()).by_login(login_value)
            if user and verify_password(user.password_hash, password):
                session.clear()
                session["user_id"] = user.user_id
                session["role_id"] = user.role_id
                get_csrf_token()
                flash(f"Добро пожаловать, {user.full_name}!", "success")
                return redirect(url_for("admin" if user.is_admin else "dashboard"))
            error = "Неверный логин или пароль."
        return render_template("login.html", error=error, login_value=login_value)

    @app.post("/logout")
    @login_required
    def logout():
        session.clear()
        flash("Вы вышли из системы.", "success")
        return redirect(url_for("index"))

    # ------------------------------------------------------------------
    # Личный кабинет
    # ------------------------------------------------------------------
    @app.get("/dashboard")
    @login_required
    def dashboard():
        applications = ApplicationRepository(db.get_db()).for_user(g.user.user_id)
        return render_template("dashboard.html", applications=applications)

    @app.route("/applications/new", methods=["GET", "POST"])
    @login_required
    def application_new():
        courses = CourseRepository(db.get_db()).all()
        selected_course = request.args.get("course", type=int)
        errors: dict[str, str] = {}
        form: dict = {}
        if request.method == "POST":
            form, errors = validate_application(request.form, courses)
            if not errors:
                ApplicationRepository(db.get_db()).create(
                    user_id=g.user.user_id,
                    course_id=form["course_id"],
                    start_date=form["start_date"],
                    payment_method=form["payment_method"],
                )
                flash("Заявка отправлена администратору.", "success")
                return redirect(url_for("dashboard"))
        return render_template(
            "application_new.html", courses=courses, errors=errors, form=form,
            selected_course=selected_course)

    @app.post("/applications/<int:application_id>/review")
    @login_required
    def application_review(application_id: int):
        applications = ApplicationRepository(db.get_db())
        application = applications.by_id(application_id)
        if application is None or application.user_id != g.user.user_id:
            abort(404)
        if application.status_id != 3:
            flash("Отзыв доступен только после завершения курса.", "error")
            return redirect(url_for("dashboard"))
        reviews = ReviewRepository(db.get_db())
        if reviews.exists(application_id):
            flash("Отзыв уже оставлен.", "error")
            return redirect(url_for("dashboard"))

        rating = request.form.get("rating", type=int)
        text = (request.form.get("review_text") or "").strip()
        if rating not in range(1, 6):
            flash("Поставьте оценку от 1 до 5.", "error")
        elif len(text) < 5:
            flash("Напишите хотя бы несколько слов об обучении.", "error")
        else:
            reviews.create(application_id, g.user.user_id, rating, text)
            flash("Спасибо за отзыв!", "success")
        return redirect(url_for("dashboard"))

    # ------------------------------------------------------------------
    # Админ-панель
    # ------------------------------------------------------------------
    @app.get("/admin")
    @admin_required
    def admin():
        status_id = request.args.get("status", type=int)
        query = (request.args.get("q") or "").strip()
        page = max(request.args.get("page", 1, type=int), 1)
        per_page = 8

        applications, total = ApplicationRepository(db.get_db()).admin_page(
            status_id=status_id, query=query, page=page, per_page=per_page)
        pages = max(1, math.ceil(total / per_page))
        if page > pages:
            page = pages
        stats = ApplicationRepository(db.get_db()).counts_by_status()
        revenue = ApplicationRepository(db.get_db()).revenue()
        return render_template(
            "admin.html", applications=applications, total=total,
            page=page, pages=pages, per_page=per_page,
            status_id=status_id, query=query, stats=stats, revenue=revenue)

    @app.post("/admin/applications/<int:application_id>/status")
    @admin_required
    def admin_status(application_id: int):
        applications = ApplicationRepository(db.get_db())
        application = applications.by_id(application_id)
        if application is None:
            abort(404)

        status_id = request.form.get("status_id", type=int)
        reason = (request.form.get("cancel_reason") or "").strip()
        if status_id not in STATUSES:
            flash("Некорректный статус.", "error")
        elif status_id == 4 and not reason:
            flash("Для отмены заявки укажите причину.", "error")
        else:
            applications.update_status(
                application_id, status_id, reason if status_id == 4 else None)
            flash(f"Статус заявки №{application_id} обновлён.", "success")

        args = {}
        back_status = request.form.get("back_status")
        back_query = request.form.get("back_q")
        back_page = request.form.get("back_page")
        if back_status:
            args["status"] = back_status
        if back_query:
            args["q"] = back_query
        if back_page and back_page != "1":
            args["page"] = back_page
        return redirect(url_for("admin", **args))

    # ------------------------------------------------------------------
    # Вариативная часть: JSON API
    # ------------------------------------------------------------------
    @app.get("/api/applications")
    @login_required
    def api_applications():
        rows = ApplicationRepository(db.get_db()).for_user(g.user.user_id)
        return jsonify([
            {
                "id": row.application_id,
                "course": row.course_title,
                "start_date": row.start_date,
                "payment": row.payment_method,
                "status": row.status_name,
                "cancel_reason": row.cancel_reason,
                "can_review": row.can_review,
            }
            for row in rows
        ])

    @app.get("/api/admin/applications")
    @admin_required
    def api_admin_applications():
        status_id = request.args.get("status", type=int)
        query = (request.args.get("q") or "").strip()
        rows, total = ApplicationRepository(db.get_db()).admin_page(
            status_id=status_id, query=query, page=1, per_page=100)
        return jsonify({
            "total": total,
            "items": [
                {
                    "id": row.application_id,
                    "user": row.user_full_name,
                    "phone": row.user_phone,
                    "course": row.course_title,
                    "start_date": row.start_date,
                    "payment": row.payment_method,
                    "status": row.status_name,
                    "cancel_reason": row.cancel_reason,
                }
                for row in rows
            ],
        })

    # ------------------------------------------------------------------
    # Ошибки
    # ------------------------------------------------------------------
    @app.errorhandler(400)
    def bad_request(error):
        return render_template("error.html", code=400,
                               message=getattr(error, "description", "Некорректный запрос.")), 400

    @app.errorhandler(403)
    def forbidden(_error):
        return render_template("error.html", code=403,
                               message="Доступ запрещён: недостаточно прав."), 403

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("error.html", code=404,
                               message="Страница или заявка не найдена."), 404

    @app.errorhandler(500)
    def server_error(_error):
        return render_template("error.html", code=500,
                               message="Внутренняя ошибка сервера."), 500

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=True)
