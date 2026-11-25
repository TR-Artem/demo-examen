# -*- coding: utf-8 -*-
"""
Собирает офлайн-HTML для обоих курсов из trainer.py:
  DemoExam-mobile.html             — веб-квалификация (09.02.07-3)
  DemoExam-mobile-programmer.html  — «Программист» (09.02.07-2)

Запуск: python build_mobile.py
После сборки можно запустить publish_site.py, чтобы обновить docs/.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "mobile" / "assets"

WEB_TIPS_OLD = [
    "1. Открой «SQL-практику» и реши задания 1–7. Это фундамент Модуля 1 и списка товаров.",
    "2. Прочитай уроки про веб, Flask, БД и разбор трёх модулей.",
    "3. На компьютере запусти lab_web/app.py — пройди регистрацию, заявку и админку.",
]

VARIANTS = {
    "web": {
        "out": ROOT / "DemoExam-mobile.html",
        "replacements": {
            'placeholder="SELECT ... FROM products;"':
                'placeholder="SELECT ... FROM courses;"',
        },
        "data_js": True,
    },
    "programmer": {
        "out": ROOT / "DemoExam-mobile-programmer.html",
        "replacements": {
            "ДЭ 09.02.07-3-2027 — Тренажёр":
                "ДЭ 09.02.07-2-2027 — Тренажёр",
            "<b>ДЭ 09.02.07-3-2027 · Веб и мультимедиа</b>":
                "<b>ДЭ 09.02.07-2-2027 · Программист</b>",
            "Профильный демонстрационный экзамен · 3 модуля · 100 баллов":
                "Профильный демонстрационный экзамен · 4 модуля · 100 баллов",
            "ДЭ 09.02.07-3-2027 «Разработчик веб и мультимедийных приложений»":
                "ДЭ 09.02.07-2-2027 «Программист»",
            ">3 модуля · 100 баллов · офлайн<":
                ">4 модуля · 100 баллов · офлайн<",
            WEB_TIPS_OLD[0]:
                "1. Открой «SQL-практику» и реши задачи 1–7. Это фундамент Модуля 1 и каталога товаров.",
            WEB_TIPS_OLD[1]:
                "2. Прочитай уроки про БД, нормальные формы, разбор 4 модулей и баллы.",
            WEB_TIPS_OLD[2]:
                "3. На компьютере запусти lab_programmer/app.py — пройди вход, каталог и заказы.",
            "15 уроков по веб-разработке · отметь прочитанное":
                "15 уроков по Python, SQL и заданиям · отметь прочитанное",
            "53 вопроса": "__QUIZ_COUNT__",
        },
        "data_js": False,
    },
}


def load_trainer(course: str):
    os.environ["DEMOEXAM_COURSE"] = course
    name = f"trainer_mobile_{course}"
    spec = importlib.util.spec_from_file_location(name, ROOT / "trainer.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def course_data(module) -> str:
    data = {
        "plan": module.PLAN,
        "lessons": [list(item) for item in module.LESSONS],
        "quiz": module.QUIZ,
        "sql": module.SQL_TASKS,
        "criteria": [[title, [[text, weight] for text, weight in items]]
                     for title, items in module.CRITERIA],
        "snippets": [[title, code] for title, code in module.SNIPPETS],
        "schema": module.SCHEMA_SQL,
        "max_score": module.MAX_SCORE,
    }
    return "window.DEMO_DATA = " + json.dumps(
        data, ensure_ascii=False, separators=(",", ":")) + ";\n"


def apply_variant(html: str, replacements: dict[str, str], quiz_count: int) -> str:
    for old, new in replacements.items():
        new = new.replace("__QUIZ_COUNT__", f"{quiz_count} вопросов")
        if old not in html:
            raise RuntimeError(f"Не найдена строка для замены: {old[:80]!r}")
        html = html.replace(old, new)
    return html


def build() -> None:
    wasm = (ASSETS / "wasm_data.js").read_text(encoding="utf-8")
    sqljs = (ASSETS / "sql-wasm.js").read_text(encoding="utf-8")

    for course, variant in VARIANTS.items():
        module = load_trainer(course)
        data = course_data(module)
        if variant["data_js"]:
            (ASSETS / "data.js").write_text(data, encoding="utf-8")

        html = apply_variant(
            (ASSETS / "index.html").read_text(encoding="utf-8"),
            variant["replacements"], len(module.QUIZ))
        for name, code in (("data.js", data),
                           ("wasm_data.js", wasm),
                           ("sql-wasm.js", sqljs)):
            code = code.replace("</script", "<\\/script")
            tag = f'<script src="{name}"></script>'
            if tag not in html:
                raise RuntimeError(f"{course}: не найден тег {tag}")
            html = html.replace(tag, "<script>\n" + code + "\n</script>")

        variant["out"].write_text(html, encoding="utf-8")
        print(f"{course}: {variant['out'].name} "
              f"({len(html) / 1024 / 1024:.2f} МБ)")


if __name__ == "__main__":
    build()
