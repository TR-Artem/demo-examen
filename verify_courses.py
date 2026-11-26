# -*- coding: utf-8 -*-
"""Проверка курсов по официальным КИМ/КОД. Запуск: python verify_courses.py"""
from __future__ import annotations

import importlib.util
import os
import re
import sqlite3
from pathlib import Path

import practical
import practical_tasks

ROOT = Path(__file__).resolve().parent


def load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check(name: str, ok: bool, detail: str = "") -> None:
    print(("OK  " if ok else "FAIL") + "  " + name + ((" — " + detail) if detail else ""))
    if not ok:
        raise SystemExit(1)


def main() -> None:
    web = load(ROOT / "course2027.py")
    prog = load(ROOT / "course_programmer.py")
    infosys = load(ROOT / "course_is.py")

    # --- Веб: критерии 25 + 25 + 25 + 25 ---
    groups = {}
    for title, items in web.CRITERIA:
        module = re.match(r"Модуль (\d)", title)
        if module:
            groups.setdefault(module.group(1), 0)
            groups[module.group(1)] += sum(w for _, w in items)
    check("веб: критерии по модулям 25/25/25",
          [groups.get(k) for k in ("1", "2", "3")] == [25, 25, 25],
          str(groups))
    check("веб: всего 100", sum(w for _, items in web.CRITERIA for _, w in items) == 100)
    check("веб: 3 модуля в тексте экзамена", "3 модуля" in web.LESSONS[0][4])
    check("веб: 390×844", "390×844" in web.LESSONS[0][4])
    check("веб: слайдер 4 / 3 секунды",
          "4 изображения" in web.LESSONS[0][4] and "3 секунды" in web.LESSONS[0][4])
    check("веб: Admin/KorokNET", "Admin / KorokNET" in web.LESSONS[0][4])
    check("веб: 3 курса в лаборатории",
          len(re.findall(r'^\s*\("(?:Основы алгоритмизации и программирования|Основы веб-дизайна|Основы проектирования баз данных)"',
                         (ROOT / "lab_web" / "seed.py").read_text(encoding="utf-8"), re.M)) == 3)
    check("веб: 6 таблиц в lab_web",
          all(t in (ROOT / "lab_web" / "schema.sql").read_text(encoding="utf-8")
              for t in ("roles", "users", "courses", "application_statuses",
                        "applications", "reviews")))
    check("веб: SQL-задачи выполняются", sql_ok(web))
    check("веб: практические задания к тестам", practical_ok(web, "web"))
    check("веб: без дублей вопросов", len({q["q"] for q in web.QUIZ}) == len(web.QUIZ))

    # --- Программист: 4 модуля, 10+15+25+25 + 25 ---
    pgroups = {}
    for title, items in prog.CRITERIA:
        module = re.match(r"Модуль (\d)", title)
        if module:
            pgroups.setdefault(module.group(1), 0)
            pgroups[module.group(1)] += sum(w for _, w in items)
    check("программист: критерии 10/15/25/25",
          [pgroups.get(k) for k in ("1", "2", "3", "4")] == [10, 15, 25, 25],
          str(pgroups))
    check("программист: всего 100",
          sum(w for _, items in prog.CRITERIA for _, w in items) == 100)
    l01 = prog.LESSONS[0][4]
    for text in ("0 ч 50", "0 ч 40", "1 ч 30", "1 ч 00",
                 "10 баллов", "15 баллов", "25 баллов"):
        check(f"программист: l01 содержит «{text}»", text in l01)
    check("программист: l01 — 4 модуля", "4 модуля" in prog.LESSONS[0][2])
    check("программист: 41 вопрос", len(prog.QUIZ) == 41, str(len(prog.QUIZ)))
    check("программист: без дублей вопросов",
          len({q["q"] for q in prog.QUIZ}) == len(prog.QUIZ))
    check("программист: 10 таблиц",
          all(f"CREATE TABLE {t}" in prog.SCHEMA_SQL for t in (
              "roles", "users", "categories", "manufacturers", "suppliers",
              "units", "pickup_points", "order_statuses", "products", "orders")))
    check("программист: нет старых таблиц размеров/строк",
          "product_items" not in prog.SCHEMA_SQL and "order_items" not in prog.SCHEMA_SQL
          and "CREATE TABLE sizes" not in prog.SCHEMA_SQL)
    check("программист: SQL-задачи выполняются", sql_ok(prog))
    check("программист: практические задания к тестам", practical_ok(prog, "programmer"))
    check("программист: 19 SQL-задач", len(prog.SQL_TASKS) == 19)
    check("программист: lab_programmer есть",
          (ROOT / "lab_programmer" / "app.py").exists()
          and (ROOT / "lab_programmer" / "schema.sql").exists())
    lab_schema = (ROOT / "lab_programmer" / "schema.sql").read_text(encoding="utf-8")
    check("программист: lab schema 10 таблиц",
          all(f"CREATE TABLE {t}" in lab_schema for t in (
              "roles", "users", "categories", "manufacturers", "suppliers",
              "units", "pickup_points", "order_statuses", "products", "orders")))

    # --- Офлайн-версии ---
    web_html = (ROOT / "DemoExam-mobile.html").read_text(encoding="utf-8")
    prog_html = (ROOT / "DemoExam-mobile-programmer.html").read_text(encoding="utf-8")
    check("веб-html: 3 модуля", "3 модуля" in web_html)
    check("веб-html: 53 вопроса", "53 вопроса" in web_html)
    check("веб-html: практика в тестах", "web-exam-skeleton" in web_html and "practiceSel" in web_html)
    check("программист-html: 4 модуля", "4 модуля" in prog_html)
    check("программист-html: 41 вопрос", "41 вопрос" in prog_html)
    check("программист-html: практика в тестах", "prog-exam-score" in prog_html and "practiceSel" in prog_html)
    check("программист-html: без «5 заданий»", "5 заданий" not in prog_html)

    # --- Информационные системы: 6 заданий, 3:30, 75 + 25 ---
    check("ИС: всего 100",
          sum(w for _, items in infosys.CRITERIA for _, w in items) == 100)
    check("ИС: 6 заданий", "6 заданий" in infosys.LESSONS[0][2])
    check("ИС: 3 ч 30 мин", "3 ч 30" in infosys.LESSONS[0][4])
    check("ИС: 75 и 25", "75" in infosys.LESSONS[0][4] and "25" in infosys.LESSONS[0][4])
    check("ИС: 39 вопросов", len(infosys.QUIZ) == 39, str(len(infosys.QUIZ)))
    check("ИС: без дублей вопросов",
          len({q["q"] for q in infosys.QUIZ}) == len(infosys.QUIZ))
    check("ИС: 11 таблиц",
          all(f"CREATE TABLE {t}" in infosys.SCHEMA_SQL for t in (
              "roles", "users", "customers", "specifications", "products",
              "materials", "product_materials", "operations",
              "product_operations", "orders", "order_items")))
    check("ИС: SQL-задачи выполняются", sql_ok(infosys))
    check("ИС: практические задания к тестам", practical_ok(infosys, "is"))
    is_html = (ROOT / "DemoExam-mobile-is.html").read_text(encoding="utf-8")
    check("ИС-html: 6 заданий", "6 заданий" in is_html)
    check("ИС-html: 39 вопросов", "39 вопросов" in is_html)
    check("ИС-html: практика в тестах", "is-exam-json" in is_html and "practiceSel" in is_html)

    # --- Сайт: выбор трёх курсов онлайн ---
    chooser = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    for name in ("DemoExam-mobile.html", "DemoExam-mobile-programmer.html",
                 "DemoExam-mobile-is.html"):
        check(f"сайт: онлайн-ссылка на {name}", f'href="{name}"' in chooser)
    check("сайт: ИС открывается без скачивания",
          "Открыть онлайн" in chooser and "Информационные системы" in chooser)
    for name in ("DemoExam-mobile.html", "DemoExam-mobile-programmer.html",
                 "DemoExam-mobile-is.html"):
        page = (ROOT / "docs" / name).read_text(encoding="utf-8")
        check(f"сайт: переключатель курсов на {name}", "course-switch" in page)

    print("\nВСЕ ПРОВЕРКИ ПРОЙДЕНЫ")


def sql_ok(module) -> bool:
    con = sqlite3.connect(":memory:")
    con.executescript(module.SCHEMA_SQL)
    try:
        for task in module.SQL_TASKS:
            if task.get("mode") == "script":
                con.execute(task["verify"])
            else:
                con.execute(task["expected"]).fetchall()
        return True
    except Exception as err:  # noqa: BLE001
        print("SQL error:", err)
        return False
    finally:
        con.close()


def practical_ok(module, slug: str) -> bool:
    tasks = practical_tasks.all_for(slug)
    if not tasks:
        print("Нет практических заданий для", slug)
        return False
    for task in tasks:
        result = practical.check(module, task, task["solution"])
        if not result["ok"]:
            print("Практика не проходит:", task["id"], result["details"])
            return False
    return True


if __name__ == "__main__":
    main()
