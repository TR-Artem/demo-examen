# -*- coding: utf-8 -*-
"""Stepik-структура курсов: модули и шаги."""
from __future__ import annotations

import importlib.util
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, BASE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


COURSE_DATA = {
    "web": _load("course2027"),
    "programmer": _load("course_programmer"),
}

MODULE_SPECS = {
    "web": [
        ("Введение. HTML и CSS", [
            ("theory", "Экзамен: структура и модули", ["l01"]),
            ("quiz", "Вопросы по экзамену", ["Экзамен"], 5),
            ("theory", "HTML: каркас и формы", ["l02"]),
            ("quiz", "Практика: HTML", ["HTML"], 5),
            ("theory", "CSS: каскад и сетки", ["l03"]),
            ("quiz", "Практика: CSS", ["CSS"], 5),
            ("theory", "Адаптивность 390×844", ["l04"]),
            ("quiz", "Практика: адаптив", ["CSS", "HTML"], 5),
        ]),
        ("JavaScript и Git", [
            ("theory", "JavaScript: DOM и валидация", ["l05"]),
            ("quiz", "Практика: JavaScript", ["JS"], 5),
            ("theory", "Слайдер и анимации", ["l06"]),
            ("quiz", "Практика: слайдер", ["JS", "Дизайн"], 5),
            ("theory", "Git и структура проекта", ["l07"]),
            ("quiz", "Практика: Git", ["Git"], 5),
        ]),
        ("Flask", [
            ("theory", "Flask: маршруты и шаблоны", ["l08"]),
            ("quiz", "Практика: Flask", ["Flask"], 5),
            ("theory", "Формы, сессии и flash", ["l09"]),
            ("quiz", "Практика: формы", ["Flask"], 5),
        ]),
        ("SQL и база данных", [
            ("theory", "SQL: SELECT, JOIN, GROUP BY", ["l10"]),
            ("sql", "SQL-практика 1–5", ["s01", "s02", "s03", "s04", "s05"]),
            ("theory", "База данных «Корочки.есть»", ["l11"]),
            ("sql", "SQL-практика 6–10", ["s06", "s07", "s08", "s09", "s10"]),
            ("sql", "SQL-практика 11–15", ["s11", "s12", "s13", "s14", "s15"]),
            ("sql", "SQL-практика 16–19", ["s16", "s17", "s18", "s19"]),
            ("quiz", "Практика: SQL и БД", ["SQL", "БД"], 5),
        ]),
        ("Безопасность, дизайн и экзамен", [
            ("theory", "Безопасность и роли", ["l12"]),
            ("quiz", "Практика: безопасность", ["Безопасность"], 5),
            ("theory", "Заявки, статусы и админка", ["l13"]),
            ("quiz", "Практика: сценарии", ["Экзамен"], 5),
            ("theory", "Дизайн и документы", ["l14"]),
            ("quiz", "Практика: дизайн", ["Дизайн"], 5),
            ("theory", "Стратегия и тайминг", ["l15"]),
            ("test", "Итоговый тест по курсу", ["Экзамен", "Дизайн", "Безопасность"], 10),
        ]),
    ],
    "programmer": [
        ("Введение. Python", [
            ("theory", "Экзамен: 4 модуля и баллы", ["l01"]),
            ("quiz", "Вопросы по экзамену", ["Экзамен"], 5),
            ("theory", "Python: типы и строки", ["l02"]),
            ("quiz", "Практика: Python", ["Python"], 5),
            ("theory", "Управление и коллекции", ["l03"]),
            ("quiz", "Практика: коллекции", ["Python"], 5),
            ("theory", "Исключения и файлы", ["l04"]),
            ("quiz", "Практика: исключения", ["Python"], 5),
        ]),
        ("База данных и SQL", [
            ("theory", "10 таблиц по КОД 2026", ["l05"]),
            ("quiz", "Практика: структура БД", ["БД"], 5),
            ("theory", "3НФ, ключи и ER", ["l06"]),
            ("quiz", "Практика: 3НФ", ["БД"], 5),
            ("theory", "Блок-схема по ГОСТ", ["l07"]),
            ("quiz", "Практика: алгоритм", ["Экзамен"], 5),
            ("theory", "SELECT, WHERE, ORDER BY", ["l08"]),
            ("sql", "SQL-практика 1–5", ["s01", "s02", "s03", "s04", "s05"]),
            ("theory", "JOIN, GROUP BY, CASE", ["l09"]),
            ("sql", "SQL-практика 6–10", ["s06", "s07", "s08", "s09", "s10"]),
            ("theory", "DDL и изменение данных", ["l10"]),
            ("sql", "SQL-практика 11–15", ["s11", "s12", "s13", "s14", "s15"]),
            ("theory", "Python + SQLite", ["l11"]),
            ("sql", "SQL-практика 16–19", ["s16", "s17", "s18", "s19"]),
        ]),
        ("tkinter и каталог", [
            ("theory", "tkinter: каталог и цвета", ["l12"]),
            ("quiz", "Практика: интерфейс", ["UI"], 5),
            ("theory", "Модули 1–2", ["l13"]),
            ("quiz", "Практика: модули 1–2", ["Экзамен"], 5),
        ]),
        ("CRUD, заказы и экзамен", [
            ("theory", "Модули 3–4", ["l14"]),
            ("quiz", "Практика: CRUD и заказы", ["Экзамен"], 5),
            ("theory", "Стратегия и тайминг", ["l15"]),
            ("test", "Итоговый тест по курсу", ["Экзамен"], 10),
        ]),
    ],
}


def _lessons(module, ids):
    by_id = {lesson[0]: lesson for lesson in module.LESSONS}
    parts = []
    for lesson_id in ids:
        lesson = by_id.get(lesson_id)
        if lesson:
            parts.append(f"{lesson[2]}\n\n{lesson[4].strip()}")
    return "\n\n".join(parts)


def _take_questions(module, topics, count, used):
    pool = [q for q in module.QUIZ if q["topic"] in topics and q["q"] not in used]
    if len(pool) < count:
        extra = [q for q in module.QUIZ if q["q"] not in used and q not in pool]
        pool += extra
    if len(pool) < count:
        pool += [q for q in module.QUIZ if q not in pool]
    selected = pool[:count]
    used.update(q["q"] for q in selected)
    return selected


def _tasks(module, ids):
    by_id = {task["id"]: task for task in module.SQL_TASKS}
    return [by_id[task_id] for task_id in ids if task_id in by_id]


def modules(slug: str) -> list[dict]:
    module = COURSE_DATA[slug]
    result = []
    for title, steps in MODULE_SPECS[slug]:
        used: set[str] = set()
        built = []
        for spec in steps:
            kind, step_title = spec[0], spec[1]
            if kind == "theory":
                built.append({
                    "type": "theory",
                    "title": step_title,
                    "content": _lessons(module, spec[2]),
                })
            elif kind in ("quiz", "test"):
                built.append({
                    "type": kind,
                    "title": step_title,
                    "questions": _take_questions(module, spec[2], spec[3], used),
                })
            elif kind == "sql":
                built.append({
                    "type": "sql",
                    "title": step_title,
                    "tasks": _tasks(module, spec[2]),
                })
        result.append({"title": title, "steps": built})
    return result
