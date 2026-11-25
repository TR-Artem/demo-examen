# -*- coding: utf-8 -*-
"""Реестр курсов тренажёра: веб-квалификация и «Программист»."""
from __future__ import annotations

import importlib
import os

DEFAULT_COURSE = "web"

ALIASES = {
    "2": "programmer",
    "09.02.07-2": "programmer",
    "09.02.07-2-2027": "programmer",
    "3": "web",
    "09.02.07-3": "web",
    "09.02.07-3-2027": "web",
    "5": "is",
    "09.02.07-5": "is",
    "09.02.07-5-2027": "is",
}

COURSES = {
    "web": {
        "module": "course2027",
        "title": "Веб и мультимедиа",
        "code": "09.02.07-3-2027",
        "subtitle": "Flask + SQLite + HTML/CSS/JS · 3 модуля",
    },
    "programmer": {
        "module": "course_programmer",
        "title": "Программист",
        "code": "09.02.07-2-2027",
        "subtitle": "Python + SQLite + tkinter · 4 модуля",
    },
    "is": {
        "module": "course_is",
        "title": "Информационные системы",
        "code": "09.02.07-5-2027",
        "subtitle": "ER, SQL, ИС, API · 6 заданий",
    },
}


def normalize(value: str | None) -> str:
    """Принимает ключ, код или название; возвращает ключ курса."""
    if not value:
        return DEFAULT_COURSE
    raw = value.strip().lower()
    if raw in COURSES:
        return raw
    if raw in ALIASES:
        return ALIASES[raw]
    for key, meta in COURSES.items():
        if raw in {key.lower(), meta["code"].lower(), meta["title"].lower()}:
            return key
        if raw in f"{meta['title']} — {meta['code']}".lower():
            return key
    return DEFAULT_COURSE


def current_key() -> str:
    return normalize(os.environ.get("DEMOEXAM_COURSE"))


def load_course(key: str | None = None):
    return importlib.import_module(COURSES[normalize(key)]["module"])


def labels() -> list[str]:
    return [f"{meta['title']} — {meta['code']}" for meta in COURSES.values()]


def key_by_label(label: str) -> str:
    for key, meta in COURSES.items():
        if label == f"{meta['title']} — {meta['code']}":
            return key
    return normalize(label)
