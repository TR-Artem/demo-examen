# -*- coding: utf-8 -*-
"""
Учебный портал «ДЭ.Курс»: вход → выбор курса → курс.
Запуск: python app.py
"""
from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import urlparse

from flask import (Flask, Response, abort, flash, g, redirect,
                   render_template, request, session, url_for)

import db
import study_content
import sql_practice
from models import ProgressRepository, UserRepository
from security import (get_csrf_token, hash_password, login_required,
                      validate_csrf, validate_registration, verify_password)

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent

COURSES = {
    "web": {
        "title": "Веб и мультимедиа",
        "code": "09.02.07-3",
        "description": "Flask, SQLite, HTML/CSS/JS: три модуля экзамена, "
                       "SQL-практика, тесты и пробник.",
        "file": BASE / "DemoExam-mobile.html",
    },
    "programmer": {
        "title": "Программист",
        "code": "09.02.07-2",
        "description": "Python, SQLite, tkinter: четыре модуля экзамена, "
                       "SQL-практика, тесты и пробник.",
        "file": BASE / "DemoExam-mobile-programmer.html",
    },
    "is": {
        "title": "Информационные системы",
        "code": "09.02.07-5",
        "description": "ER, SQL, авторизация, API и Postman: шесть заданий "
                       "профильного экзамена.",
        "file": BASE / "DemoExam-mobile-is.html",
    },
}


def _prev_url(slug: str, module_no: int, step_no: int, modules) -> str | None:
    if step_no > 1:
        return url_for("step", slug=slug, module_no=module_no, step_no=step_no - 1)
    if module_no > 1:
        prev_module = module_no - 1
        return url_for("step", slug=slug, module_no=prev_module,
                       step_no=len(modules[prev_module - 1]["steps"]))
    return None


def _safe_next(value: str | None) -> str | None:
    if not value:
        return None
    parsed = urlparse(value)
    if parsed.scheme or parsed.netloc or not value.startswith("/"):
        return None
    return value


def _next_url(slug: str, module_no: int, step_no: int, modules) -> str:
    if step_no < len(modules[module_no - 1]["steps"]):
        return url_for("step", slug=slug, module_no=module_no,
                       step_no=step_no + 1)
    if module_no < len(modules):
        return url_for("module", slug=slug, module_no=module_no + 1)
    return url_for("module", slug=slug, module_no=module_no)


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "study-secret-change-me"),
        DATABASE=os.environ.get("DATABASE", str(ROOT / "instance" / "study.db")),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        CSRF_ENABLED=True,
    )
    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)
    db.init_app(app)

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
        return {"current_user": g.get("user"), "csrf_token": get_csrf_token()}

    @app.get("/")
    def index():
        return render_template("courses.html", courses=COURSES)

    @app.route("/register", methods=["GET", "POST"])
    def register():
        users = UserRepository(db.get_db())
        errors: dict[str, str] = {}
        form: dict = {}
        next_url = _safe_next(request.values.get("next"))
        if request.method == "POST":
            form, errors = validate_registration(request.form, users)
            if not errors:
                users.create(form["login"], hash_password(form["password"]))
                flash("Аккаунт создан. Войдите в систему.", "success")
                if next_url:
                    return redirect(url_for("login", next=next_url))
                return redirect(url_for("login"))
        return render_template("register.html", errors=errors, form=form,
                               next_url=next_url or "")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        next_url = _safe_next(request.values.get("next"))
        if g.user is not None:
            return redirect(next_url or url_for("courses"))
        error = None
        login_value = ""
        if request.method == "POST":
            login_value = (request.form.get("login") or "").strip()
            password = request.form.get("password") or ""
            user = UserRepository(db.get_db()).by_login(login_value)
            if user and verify_password(user.password_hash, password):
                session.clear()
                session["user_id"] = user.user_id
                get_csrf_token()
                flash("Вы вошли в аккаунт.", "success")
                return redirect(next_url or url_for("courses"))
            error = "Неверный никнейм или пароль."
        return render_template("login.html", error=error,
                               login_value=login_value,
                               next_url=next_url or "")

    @app.post("/logout")
    @login_required
    def logout():
        session.clear()
        flash("Вы вышли из аккаунта.", "success")
        return redirect(url_for("login"))

    @app.get("/courses")
    def courses():
        return render_template("courses.html", courses=COURSES)

    @app.get("/course/<slug>")
    @login_required
    def course(slug: str):
        if slug not in COURSES:
            abort(404)
        modules = study_content.modules(slug)
        progress = ProgressRepository(db.get_db()).for_course(g.user.user_id, slug)
        target_module, target_step = 1, 1
        for module_no, module in enumerate(modules, start=1):
            for step_no in range(1, len(module["steps"]) + 1):
                if not progress.get((module_no, step_no)):
                    target_module, target_step = module_no, step_no
                    return redirect(url_for("step", slug=slug,
                                            module_no=target_module,
                                            step_no=target_step))
        return redirect(url_for("step", slug=slug, module_no=target_module,
                                step_no=target_step))

    @app.get("/course/<slug>/module/<int:module_no>")
    @login_required
    def module(slug: str, module_no: int):
        if slug not in COURSES:
            abort(404)
        modules = study_content.modules(slug)
        if not 1 <= module_no <= len(modules):
            abort(404)
        progress = ProgressRepository(db.get_db()).for_course(g.user.user_id, slug)
        module = modules[module_no - 1]
        target = 1
        for step_no in range(1, len(module["steps"]) + 1):
            if not progress.get((module_no, step_no)):
                target = step_no
                break
        return redirect(url_for("step", slug=slug, module_no=module_no,
                                step_no=target))

    @app.route("/course/<slug>/module/<int:module_no>/step/<int:step_no>",
               methods=["GET", "POST"])
    @login_required
    def step(slug: str, module_no: int, step_no: int):
        if slug not in COURSES:
            abort(404)
        modules = study_content.modules(slug)
        if not 1 <= module_no <= len(modules):
            abort(404)
        module = modules[module_no - 1]
        if not 1 <= step_no <= len(module["steps"]):
            abort(404)
        current = module["steps"][step_no - 1]
        progress_repo = ProgressRepository(db.get_db())
        progress = progress_repo.for_course(g.user.user_id, slug)
        for mi, mod in enumerate(modules, start=1):
            for si, st in enumerate(mod["steps"], start=1):
                st["done"] = bool(progress.get((mi, si)))
        total_steps = sum(len(mod["steps"]) for mod in modules)
        done_steps = sum(1 for mi, mod in enumerate(modules, start=1)
                         for si in range(1, len(mod["steps"]) + 1)
                         if progress.get((mi, si)))
        result = None
        sql_result = None
        session_key = f"sql_done:{slug}:{module_no}:{step_no}"
        sql_done = set(session.get(session_key, []))
        just_done = False

        if request.method == "POST":
            if current["type"] == "theory":
                progress_repo.mark(g.user.user_id, slug, module_no, step_no)
                return redirect(_next_url(slug, module_no, step_no, modules))

            if current["type"] in ("quiz", "test"):
                answers = {}
                details = []
                score = 0
                for index, question in enumerate(current["questions"]):
                    raw = request.form.get(f"q{index}")
                    chosen = int(raw) if raw is not None and raw.isdigit() else -1
                    correct = chosen == question["ans"]
                    score += int(correct)
                    answers[index] = chosen
                    details.append({"chosen": chosen, "correct": correct})
                total = len(current["questions"])
                percent = round(score / total * 100) if total else 0
                threshold = 70 if current["type"] == "test" else 60
                passed = percent >= threshold
                if passed:
                    progress_repo.mark(g.user.user_id, slug, module_no,
                                       step_no, percent)
                result = {
                    "score": score, "total": total, "percent": percent,
                    "passed": passed, "threshold": threshold,
                    "answers": answers, "details": details,
                }

            if current["type"] == "sql":
                task_id = request.form.get("task_id")
                task = next((t for t in current["tasks"] if t["id"] == task_id), None)
                if task is not None:
                    ok, error, actual, expected = sql_practice.check(
                        study_content.COURSE_DATA[slug], task,
                        request.form.get("user_sql", ""))
                    if ok:
                        sql_done.add(task["id"])
                        session[session_key] = sorted(sql_done)
                        task_ids = {t["id"] for t in current["tasks"]}
                        if task_ids <= sql_done:
                            progress_repo.mark(g.user.user_id, slug,
                                               module_no, step_no)
                            just_done = True
                    sql_result = {"task_id": task_id, "ok": ok, "error": error,
                                  "actual": actual, "expected": expected}

        progress = progress_repo.for_course(g.user.user_id, slug)
        for mi, mod in enumerate(modules, start=1):
            for si, st in enumerate(mod["steps"], start=1):
                st["done"] = bool(progress.get((mi, si)))
        done_steps = sum(1 for mi, mod in enumerate(modules, start=1)
                         for si in range(1, len(mod["steps"]) + 1)
                         if progress.get((mi, si)))
        done = bool(progress.get((module_no, step_no))) or just_done
        return render_template(
            "step.html", slug=slug, course=COURSES[slug],
            module_no=module_no, step_no=step_no, module=module,
            step=current, result=result, done=done, sql_result=sql_result,
            sql_done=sql_done, modules=modules, total_steps=total_steps,
            done_steps=done_steps,
            prev_url=_prev_url(slug, module_no, step_no, modules),
            next_url=_next_url(slug, module_no, step_no, modules),
            module_url=url_for("module", slug=slug, module_no=module_no),
        )

    @app.get("/course/<slug>/content")
    @login_required
    def course_content(slug: str):
        if slug not in COURSES:
            abort(404)
        path = COURSES[slug]["file"]
        if not path.exists():
            abort(404, description="Файл курса не найден.")
        html = path.read_text(encoding="utf-8")
        html = html.replace(
            "</head>",
            "<style>:root{--topbar-h:0px !important}"
            ".topbar{display:none !important}</style></head>",
            1,
        )
        return Response(html, mimetype="text/html")

    @app.errorhandler(403)
    def forbidden(_error):
        return render_template("error.html", code=403,
                               message="Доступ запрещён."), 403

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("error.html", code=404,
                               message="Страница или курс не найдены."), 404

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=False)
