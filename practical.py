# -*- coding: utf-8 -*-
"""
Автопроверка практических заданий.

Поддерживает:
  * Python — реальный запуск кода в отдельном процессе с таймаутом;
  * SQL и DDL — встроенный SQLite;
  * HTML — разбор тегов, атрибутов и текста;
  * CSS/JS/Git/текст — проверка обязательных и запрещённых шаблонов;
  * JSON — структура, длины массивов, суммы и обязательные ключи.

Модуль общий для учебного портала, тренажёра и сборки офлайн-сайта.
"""
from __future__ import annotations

import ast
import json
import os
import re
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STUDY_WEB = ROOT / "study_web"
if str(STUDY_WEB) not in sys.path:
    sys.path.insert(0, str(STUDY_WEB))

try:  # SQL-проверка живёт рядом с порталом
    import sql_practice  # type: ignore
except Exception:  # pragma: no cover - на случай отдельного запуска
    sql_practice = None

MAX_OUTPUT = 4000


def _result(ok: bool, message: str, details: list[str] | None = None) -> dict:
    return {"ok": ok, "message": message, "details": details or []}


def _flags(kind: str) -> int:
    if kind in {"python"}:
        return re.MULTILINE
    return re.MULTILINE | re.IGNORECASE


def _pattern_checks(code: str, items, kind: str) -> list[str]:
    """Вернуть подписи обязательных шаблонов, которые не найдены."""
    missing = []
    flags = _flags(kind)
    for item in items or []:
        if isinstance(item, str):
            item = {"label": item, "pattern": item}
        pattern = item.get("pattern", "")
        label = item.get("label") or pattern
        try:
            found = re.search(pattern, code, flags) is not None
        except re.error as err:
            missing.append(f"{label}: ошибка в правиле проверки ({err})")
            continue
        if not found:
            missing.append(label)
    return missing


def _forbidden_checks(code: str, items, kind: str) -> list[str]:
    """Вернуть подписи запрещённых шаблонов, которые встретились."""
    matched = []
    flags = _flags(kind)
    for item in items or []:
        if isinstance(item, str):
            item = {"label": item, "pattern": item}
        pattern = item.get("pattern", "")
        label = item.get("label") or pattern
        try:
            if re.search(pattern, code, flags) is not None:
                matched.append(label)
        except re.error:
            continue
    return matched


def _patterns(code: str, spec: dict, kind: str = "patterns") -> dict:
    missing = _pattern_checks(code, spec.get("require"), kind)
    forbidden = _forbidden_checks(code, spec.get("forbid"), kind)
    details = [f"Не найдено: {item}" for item in missing]
    details += [f"Убери: {item}" for item in forbidden]
    if details:
        return _result(False, "Решение пока не проходит проверку.", details)
    return _result(True, "Все требования выполнены.")


class _HTMLCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tags: list[str] = []
        self.attrs: list[tuple[str, dict[str, str | None]]] = []
        self.text_parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag.lower())
        self.attrs.append((tag.lower(), {k.lower(): v for k, v in attrs}))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_data(self, data):
        if data.strip():
            self.text_parts.append(data.strip())


def _html(code: str, spec: dict) -> dict:
    parser = _HTMLCollector()
    try:
        parser.feed(code)
    except Exception as err:  # pragma: no cover
        return _result(False, f"Не удалось разобрать HTML: {err}")

    missing = []
    for tag in spec.get("require_tags", []):
        if tag.lower() not in parser.tags:
            missing.append(f"тег <{tag}>")

    for item in spec.get("require_attrs", []):
        tag, attr, value = item
        found = False
        for parsed_tag, attrs in parser.attrs:
            if parsed_tag != tag.lower():
                continue
            if attr.lower() not in attrs:
                continue
            if value is None or (attrs[attr.lower()] or "").lower() == str(value).lower():
                found = True
                break
        if not found:
            if value is None:
                missing.append(f"атрибут {attr} у <{tag}>")
            else:
                missing.append(f"{attr}=\"{value}\" у <{tag}>")

    text = " ".join(parser.text_parts).lower()
    for needle in spec.get("text", []):
        if needle.lower() not in text:
            missing.append(f"текст «{needle}»")

    pattern_missing = _pattern_checks(code, spec.get("require"), "html")
    missing += pattern_missing
    forbidden = _forbidden_checks(code, spec.get("forbid"), "html")

    details = [f"Не найдено: {item}" for item in missing]
    details += [f"Убери: {item}" for item in forbidden]
    if details:
        return _result(False, "Разметка пока не соответствует заданию.", details)
    return _result(True, "Разметка соответствует требованиям.")


def _normalize_output(text: str) -> list[str]:
    return [line.rstrip() for line in (text or "").strip().splitlines()]


def _numbers_equal(left: str, right: str) -> bool:
    try:
        a = float(left)
        b = float(right)
    except (TypeError, ValueError):
        return False
    return abs(a - b) <= 0.011


def _outputs_equal(actual: list[str], expected: list[str]) -> bool:
    if len(actual) != len(expected):
        return False
    return all(
        a == b or _numbers_equal(a, b)
        for a, b in zip(actual, expected)
    )


def _check_python(task: dict, code: str) -> dict:
    spec = task["check"]
    tests = spec.get("tests", "")
    expected = spec.get("expected_output", "")

    try:
        ast.parse(code)
    except SyntaxError as err:
        return _result(False, f"Синтаксическая ошибка в Python: {err.msg} "
                              f"(строка {err.lineno}).")

    script = code.rstrip() + "\n\n" + tests.strip() + "\n"
    with tempfile.TemporaryDirectory(prefix="de-practice-") as tmp:
        path = Path(tmp) / "solution.py"
        path.write_text(script, encoding="utf-8")
        env = {
            "PYTHONIOENCODING": "utf-8",
            "PYTHONUTF8": "1",
            "PATH": os.environ.get("PATH", ""),
            "HOME": tmp,
            "TMPDIR": tmp,
        }
        cmd = [sys.executable, "-I", "-S", str(path)]
        preexec = None
        if os.name == "posix":
            def _limit():
                try:
                    import resource
                    resource.setrlimit(resource.RLIMIT_CPU, (3, 3))
                except Exception:
                    pass
            preexec = _limit
        try:
            proc = subprocess.run(
                cmd, cwd=tmp, env=env, capture_output=True, text=True,
                timeout=8, preexec_fn=preexec,
            )
        except subprocess.TimeoutExpired:
            return _result(False, "Код выполнялся слишком долго (таймаут 8 секунд).")

    stdout = (proc.stdout or "")[:MAX_OUTPUT]
    stderr = (proc.stderr or "")[:MAX_OUTPUT]
    if proc.returncode != 0:
        tail = "\n".join(stderr.strip().splitlines()[-6:])
        return _result(False, "Код завершился с ошибкой.", [tail or "Нет вывода."])

    actual_lines = _normalize_output(stdout)
    expected_lines = _normalize_output(expected)
    if not _outputs_equal(actual_lines, expected_lines):
        details = []
        details.append("Ожидалось:")
        details.extend(expected_lines[:12])
        details.append("Получено:")
        details.extend(actual_lines[:12] or ["(пусто)"])
        return _result(False, "Код работает, но результат отличается.", details)
    return _result(True, "Код выполнен, результат совпал с ожидаемым.")


def _check_sql(module, task: dict, code: str) -> dict:
    if sql_practice is None:
        return _result(False, "SQL-проверка недоступна: не найден sql_practice.py.")
    spec = dict(task.get("check") or {})
    if task.get("check", {}).get("type") == "ddl":
        spec["mode"] = "script"
    ok, error, actual, expected = sql_practice.check(module, spec, code)
    if ok:
        return _result(True, "Запрос возвращает ожидаемый результат.")
    details = []
    if error:
        details.append(error)
    elif actual != expected:
        details.append(f"Строк получено: {len(actual)}, ожидалось: {len(expected)}.")
    return _result(False, "Результат отличается от эталона.", details)


def _check_ddl(module, task: dict, code: str) -> dict:
    sql_result = _check_sql(module, task, code)
    if not sql_result["ok"]:
        return sql_result
    pattern_result = _patterns(code, task.get("check") or {}, "sql")
    if not pattern_result["ok"]:
        return pattern_result
    return _result(True, "Таблицы созданы с нужными ограничениями.")


def _resolve(data, path: str):
    return data[path] if path in data else None


def _check_json(task: dict, code: str) -> dict:
    try:
        data = json.loads(code)
    except json.JSONDecodeError as err:
        return _result(False, f"Это не валидный JSON: {err.msg} (строка {err.lineno}).")
    if not isinstance(data, dict):
        return _result(False, "На верхнем уровне должен быть JSON-объект.")

    spec = task["check"]
    missing = []
    for key in spec.get("keys", []):
        if key not in data:
            missing.append(f"ключ {key}")
    for key, length in (spec.get("list_len") or {}).items():
        value = _resolve(data, key)
        if not isinstance(value, list):
            missing.append(f"{key} должен быть массивом")
        elif len(value) != length:
            missing.append(f"в {key} должно быть элементов: {length}, сейчас {len(value)}")
    for path, total in (spec.get("sum") or {}).items():
        base, _, field = path.partition("[].")
        value = _resolve(data, base)
        if not isinstance(value, list) or not field:
            missing.append(f"не удалось посчитать сумму {path}")
            continue
        try:
            actual_sum = sum(float(item[field]) for item in value)
        except (KeyError, TypeError, ValueError):
            missing.append(f"у элементов {base} нет числового поля {field}")
            continue
        if round(actual_sum, 2) != round(float(total), 2):
            missing.append(f"сумма {path} = {actual_sum:g}, нужна {total}")
    for key, fields in (spec.get("item_keys") or {}).items():
        value = _resolve(data, key)
        if not isinstance(value, list):
            missing.append(f"{key} должен быть массивом")
            continue
        for index, item in enumerate(value, start=1):
            if not isinstance(item, dict):
                missing.append(f"элемент {key}[{index}] должен быть объектом")
                continue
            for field in fields:
                if field not in item:
                    missing.append(f"в {key}[{index}] нет поля {field}")

    pattern_missing = _pattern_checks(code, spec.get("require"), "json")
    missing += pattern_missing
    forbidden = _forbidden_checks(code, spec.get("forbid"), "json")

    details = [f"Не найдено: {item}" for item in missing]
    details += [f"Убери: {item}" for item in forbidden]
    if details:
        return _result(False, "JSON пока не соответствует заданию.", details)
    return _result(True, "JSON корректен и соответствует требованиям.")


def check(module, task: dict, code: str) -> dict:
    """Проверить решение. module — course2027/course_programmer/course_is."""
    code = (code or "").strip()
    if not code:
        return _result(False, "Напишите решение в редакторе.")

    spec = task.get("check") or {}
    kind = spec.get("type", "patterns")
    if kind == "python":
        return _check_python(task, code)
    if kind == "sql":
        return _check_sql(module, task, code)
    if kind == "ddl":
        return _check_ddl(module, task, code)
    if kind == "html":
        return _html(code, spec)
    if kind == "json":
        return _check_json(task, code)
    return _patterns(code, spec, spec.get("language") or task.get("language", "patterns"))
