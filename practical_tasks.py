# -*- coding: utf-8 -*-
"""
Практические задания к тестам всех трёх курсов.

Каждое задание привязано к шагу курса (модуль + шаг) и содержит:
  * формулировку и чек-лист требований;
  * заготовку кода;
  * подсказку и эталонное решение;
  * правило автопроверки (HTML-разметка, CSS/JS-шаблоны, запуск Python,
    SQL на SQLite, JSON, DDL и т. п.).

Данные намеренно хранятся отдельно от course_*.py: их используют
учебный портал study_web, тренажёр trainer.py и сборка офлайн-сайта.
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# ВЕБ И МУЛЬТИМЕДИА · 09.02.07-3
# ---------------------------------------------------------------------------
WEB = [
    {
        "id": "web-exam-skeleton",
        "module": 1,
        "step": 2,
        "topic": "Экзамен",
        "title": "Каркас страницы каталога",
        "level": "лёгкое",
        "language": "html",
        "task": (
            "Собери HTML5-каркас страницы каталога курсов. Нужны корректный "
            "DOCTYPE, русский язык, мобильный viewport, заголовок «Курсы», "
            "шапка, основная часть с h1 и подвал."
        ),
        "requirements": [
            "<!DOCTYPE html> в первой строке",
            "<html lang=\"ru\">",
            "<meta charset=\"utf-8\"> и viewport",
            "<title>Курсы</title>",
            "Семантические теги header, main, footer",
            "Заголовок h1 с текстом «Курсы»",
        ],
        "starter": "<!DOCTYPE html>\n<html>\n<head>\n  <meta charset=\"utf-8\">\n</head>\n<body>\n\n</body>\n</html>\n",
        "hint": (
            "Каркас: doctype → html lang=ru → head (charset, viewport, title) → "
            "body → header, main, footer. Внутри main положи h1."
        ),
        "solution": (
            "<!DOCTYPE html>\n"
            "<html lang=\"ru\">\n"
            "<head>\n"
            "  <meta charset=\"utf-8\">\n"
            "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "  <title>Курсы</title>\n"
            "</head>\n"
            "<body>\n"
            "  <header><strong>ДЭ.Курс</strong></header>\n"
            "  <main>\n"
            "    <h1>Курсы</h1>\n"
            "    <p>Выберите направление подготовки.</p>\n"
            "  </main>\n"
            "  <footer>© 2027</footer>\n"
            "</body>\n"
            "</html>\n"
        ),
        "check": {
            "type": "html",
            "require": [
                r"<!doctype\s+html",
                r"<meta[^>]+name=[\"']viewport[\"'][^>]*width=device-width",
            ],
            "require_tags": ["html", "head", "meta", "title", "body",
                             "header", "main", "footer", "h1"],
            "require_attrs": [
                ["html", "lang", "ru"],
                ["meta", "charset", None],
            ],
            "text": ["Курсы"],
        },
    },
    {
        "id": "web-html-form",
        "module": 1,
        "step": 4,
        "topic": "HTML",
        "title": "Форма заявки на курс",
        "level": "среднее",
        "language": "html",
        "task": (
            "Сверстай форму заявки: ФИО, e-mail, телефон и выбор курса. "
            "Каждое поле свяжи с label, обязательные поля отметь required, "
            "форму отправь методом POST на /apply."
        ),
        "requirements": [
            "<form action=\"/apply\" method=\"post\">",
            "label с for и input/select с совпадающим id",
            "name=\"full_name\", type=\"email\", type=\"tel\"",
            "select name=\"course_id\" с вариантами курсов",
            "Кнопка type=\"submit\" с текстом «Отправить заявку»",
            "У обязательных полей есть required",
        ],
        "starter": "<form>\n  <p>Поле ФИО</p>\n  <p>Поле e-mail</p>\n</form>\n",
        "hint": (
            "Связка label/input: <label for=\"email\">E-mail</label> и "
            "<input id=\"email\" name=\"email\" type=\"email\" required>. "
            "Для телефона используй type=\"tel\", для курса — select."
        ),
        "solution": (
            "<form action=\"/apply\" method=\"post\">\n"
            "  <label for=\"full_name\">ФИО</label>\n"
            "  <input id=\"full_name\" name=\"full_name\" type=\"text\" required>\n\n"
            "  <label for=\"email\">E-mail</label>\n"
            "  <input id=\"email\" name=\"email\" type=\"email\" required>\n\n"
            "  <label for=\"phone\">Телефон</label>\n"
            "  <input id=\"phone\" name=\"phone\" type=\"tel\" required>\n\n"
            "  <label for=\"course_id\">Курс</label>\n"
            "  <select id=\"course_id\" name=\"course_id\" required>\n"
            "    <option value=\"web\">Веб и мультимедиа</option>\n"
            "    <option value=\"programmer\">Программист</option>\n"
            "    <option value=\"is\">Информационные системы</option>\n"
            "  </select>\n\n"
            "  <button type=\"submit\">Отправить заявку</button>\n"
            "</form>\n"
        ),
        "check": {
            "type": "html",
            "require": [r"required", r"type=[\"']submit[\"']"],
            "require_tags": ["form", "label", "input", "select", "option", "button"],
            "require_attrs": [
                ["form", "action", "/apply"],
                ["form", "method", "post"],
                ["input", "name", "full_name"],
                ["input", "type", "email"],
                ["input", "type", "tel"],
                ["select", "name", "course_id"],
                ["label", "for", "full_name"],
                ["label", "for", "email"],
                ["label", "for", "phone"],
                ["label", "for", "course_id"],
            ],
            "text": ["Отправить заявку"],
        },
    },
    {
        "id": "web-css-grid",
        "module": 1,
        "step": 6,
        "topic": "CSS",
        "title": "Сетка карточек курсов",
        "level": "среднее",
        "language": "css",
        "task": (
            "Оформи каталог: контейнер .cards — CSS Grid из трёх равных колонок, "
            "у .card — отступы, скругление, тень; при наведении карточка слегка "
            "поднимается. На ширине до 600px — одна колонка."
        ),
        "requirements": [
            ".cards { display: grid; }",
            "grid-template-columns: repeat(3, 1fr) и gap",
            ".card с padding, border-radius, box-shadow",
            "Плавный transition и :hover с transform",
            "Media query max-width: 600px → одна колонка",
        ],
        "starter": ".cards {\n  /* сетка */\n}\n\n.card {\n  /* карточка */\n}\n",
        "hint": (
            "Начни с .cards { display:grid; grid-template-columns:repeat(3,1fr); "
            "gap:16px; }. В media query переопредели колонки на 1fr."
        ),
        "solution": (
            ".cards {\n"
            "  display: grid;\n"
            "  grid-template-columns: repeat(3, 1fr);\n"
            "  gap: 18px;\n"
            "}\n\n"
            ".card {\n"
            "  padding: 20px;\n"
            "  border-radius: 12px;\n"
            "  background: #fff;\n"
            "  box-shadow: 0 4px 16px rgba(15, 23, 42, .08);\n"
            "  transition: transform .18s ease, box-shadow .18s ease;\n"
            "}\n\n"
            ".card:hover {\n"
            "  transform: translateY(-3px);\n"
            "  box-shadow: 0 10px 24px rgba(15, 23, 42, .14);\n"
            "}\n\n"
            "@media (max-width: 600px) {\n"
            "  .cards { grid-template-columns: 1fr; }\n"
            "}\n"
        ),
        "check": {
            "type": "patterns",
            "require": [
                {"label": "display: grid", "pattern": r"\.cards\s*\{[^}]*display\s*:\s*grid"},
                {"label": "три колонки repeat(3, 1fr)", "pattern": r"grid-template-columns\s*:\s*repeat\(\s*3\s*,\s*1fr\s*\)"},
                {"label": "gap", "pattern": r"\.cards\s*\{[^}]*gap\s*:"},
                {"label": "padding у .card", "pattern": r"\.card\s*\{[^}]*padding\s*:"},
                {"label": "border-radius", "pattern": r"\.card\s*\{[^}]*border-radius\s*:"},
                {"label": "box-shadow", "pattern": r"\.card\s*\{[^}]*box-shadow\s*:"},
                {"label": "transition", "pattern": r"transition\s*:"},
                {"label": ":hover с transform", "pattern": r"\.card:hover\s*\{[^}]*transform\s*:"},
                {"label": "media query max-width: 600px", "pattern": r"@media\s*\([^)]*max-width\s*:\s*600px"},
                {"label": "одна колонка в mobile", "pattern": r"@media[^{]*\{[\s\S]*grid-template-columns\s*:\s*1fr"},
            ],
            "forbid": [
                {"label": "фиксированная ширина 1200px", "pattern": r"width\s*:\s*1200px"},
            ],
        },
    },
    {
        "id": "web-responsive",
        "module": 1,
        "step": 8,
        "topic": "CSS",
        "title": "Мобильная версия 390×844",
        "level": "среднее",
        "language": "css",
        "task": (
            "Подготовь страницу к экрану 390×844: картинки не выходят за пределы "
            "контейнера, навигация на узком экране становится колонкой, кнопки "
            "удобно нажимать пальцем."
        ),
        "requirements": [
            "img { max-width: 100%; height: auto; }",
            "Media query max-width: 600px",
            ".nav в колонку на мобильном",
            "Кнопки/ссылки с min-height: 44px",
            "Никаких фиксированных ширин больше 390px",
        ],
        "starter": ".nav {\n  display: flex;\n  gap: 12px;\n}\n\nimg {\n  /* ограничь ширину */\n}\n",
        "hint": (
            "Мобильный минимум: img { max-width:100%; height:auto; } и "
            "@media (max-width:600px) { .nav { flex-direction:column; } }"
        ),
        "solution": (
            "img {\n"
            "  max-width: 100%;\n"
            "  height: auto;\n"
            "  display: block;\n"
            "}\n\n"
            ".nav {\n"
            "  display: flex;\n"
            "  gap: 12px;\n"
            "}\n\n"
            ".nav a,\n"
            "button {\n"
            "  min-height: 44px;\n"
            "  display: inline-flex;\n"
            "  align-items: center;\n"
            "}\n\n"
            "@media (max-width: 600px) {\n"
            "  .nav { flex-direction: column; }\n"
            "  body { padding: 12px; }\n"
            "}\n"
        ),
        "check": {
            "type": "patterns",
            "require": [
                {"label": "max-width: 100% у img", "pattern": r"img\s*\{[^}]*max-width\s*:\s*100%"},
                {"label": "height: auto у img", "pattern": r"img\s*\{[^}]*height\s*:\s*auto"},
                {"label": "media query max-width: 600px", "pattern": r"@media\s*\([^)]*max-width\s*:\s*(600|640|768)px"},
                {"label": "навигация в колонку", "pattern": r"@media[^{]*\{[\s\S]*\.nav\s*\{[^}]*flex-direction\s*:\s*column"},
                {"label": "min-height: 44px", "pattern": r"min-height\s*:\s*44px"},
            ],
            "forbid": [
                {"label": "width больше 390px", "pattern": r"(?<![-\w])width\s*:\s*(4[0-9]{2}|[5-9][0-9]{2}|[1-9][0-9]{3,})px"},
            ],
        },
    },
    {
        "id": "web-js-validation",
        "module": 2,
        "step": 2,
        "topic": "JS",
        "title": "Валидация формы на JavaScript",
        "level": "среднее",
        "language": "js",
        "task": (
            "Напиши обработчик отправки формы #applicationForm: отмени стандартное "
            "поведение, проверь ФИО (не короче 3 символов) и e-mail по регулярному "
            "выражению. Ошибку выведи в #error, успешную отправку разреши."
        ),
        "requirements": [
            "addEventListener('submit', ...)",
            "event.preventDefault()",
            "Проверка value.length >= 3 для ФИО",
            "Регулярное выражение для e-mail",
            "Вывод ошибки в элемент #error",
            "При успехе — отправка формы (form.submit() или снятие блокировки)",
        ],
        "starter": (
            "const form = document.querySelector('#applicationForm');\n"
            "const errorBox = document.querySelector('#error');\n\n"
            "form.addEventListener('submit', (event) => {\n"
            "  // проверь поля\n"
            "});\n"
        ),
        "hint": (
            "Проверь: const name = form.full_name.value.trim(); "
            "if (name.length < 3) { event.preventDefault(); errorBox.textContent = '...'; }. "
            "E-mail: /^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(email)."
        ),
        "solution": (
            "const form = document.querySelector('#applicationForm');\n"
            "const errorBox = document.querySelector('#error');\n\n"
            "form.addEventListener('submit', (event) => {\n"
            "  const name = form.full_name.value.trim();\n"
            "  const email = form.email.value.trim();\n"
            "  const emailOk = /^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(email);\n\n"
            "  if (name.length < 3) {\n"
            "    event.preventDefault();\n"
            "    errorBox.textContent = 'ФИО должно быть не короче 3 символов';\n"
            "    return;\n"
            "  }\n\n"
            "  if (!emailOk) {\n"
            "    event.preventDefault();\n"
            "    errorBox.textContent = 'Проверьте e-mail';\n"
            "    return;\n"
            "  }\n\n"
            "  errorBox.textContent = '';\n"
            "  form.submit();\n"
            "});\n"
        ),
        "check": {
            "type": "patterns",
            "require": [
                {"label": "addEventListener('submit')", "pattern": r"addEventListener\(\s*[\"']submit[\"']"},
                {"label": "preventDefault()", "pattern": r"preventDefault\s*\(\s*\)"},
                {"label": "обращение к value", "pattern": r"\.value"},
                {"label": "проверка длины", "pattern": r"\.length\s*(>=|<|>|<=)\s*3"},
                {"label": "регулярное выражение для e-mail", "pattern": r"\.test\s*\(|match\s*\("},
                {"label": "вывод в #error", "pattern": r"#error|errorBox|error\.textContent"},
                {"label": "успешная отправка", "pattern": r"\.submit\s*\(|return\s+true"},
            ],
        },
    },
    {
        "id": "web-js-slider",
        "module": 2,
        "step": 4,
        "topic": "JS",
        "title": "Слайдер на три слайда",
        "level": "сложное",
        "language": "js",
        "task": (
            "Сделай слайдер: массив слайдов, кнопки «Назад»/«Вперёд», автопрокрутка "
            "каждые 3 секунды. Активный слайд получает класс .is-active, остальные "
            "класс теряют."
        ),
        "requirements": [
            "Массив слайдов или querySelectorAll",
            "Функция showSlide(index)",
            "Переключение classList .is-active",
            "Кнопки next/prev",
            "setInterval с задержкой 3000 мс",
        ],
        "starter": (
            "const slides = document.querySelectorAll('.slide');\n"
            "let index = 0;\n\n"
            "function showSlide(i) {\n"
            "  // переключи классы\n"
            "}\n"
        ),
        "hint": (
            "slides.forEach((s, i) => s.classList.toggle('is-active', i === index)); "
            "Затем next: index = (index + 1) % slides.length; showSlide(index); "
            "setInterval(next, 3000)."
        ),
        "solution": (
            "const slides = document.querySelectorAll('.slide');\n"
            "let index = 0;\n\n"
            "function showSlide(i) {\n"
            "  index = (i + slides.length) % slides.length;\n"
            "  slides.forEach((slide, n) => {\n"
            "    slide.classList.toggle('is-active', n === index);\n"
            "  });\n"
            "}\n\n"
            "function next() { showSlide(index + 1); }\n"
            "function prev() { showSlide(index - 1); }\n\n"
            "document.querySelector('#next').addEventListener('click', next);\n"
            "document.querySelector('#prev').addEventListener('click', prev);\n"
            "setInterval(next, 3000);\n"
        ),
        "check": {
            "type": "patterns",
            "require": [
                {"label": "коллекция слайдов", "pattern": r"querySelectorAll\(\s*[\"']\.slide|(const|let|var)\s+slides\s*=\s*\["},
                {"label": "функция показа слайда", "pattern": r"function\s+showSlide|showSlide\s*=\s*\("},
                {"label": "classList", "pattern": r"classList\.(toggle|add|remove)"},
                {"label": "is-active", "pattern": r"is-active"},
                {"label": "кнопки next/prev", "pattern": r"#next|#prev|nextButton|prevButton"},
                {"label": "setInterval 3000", "pattern": r"setInterval\([^,]+,\s*3000\s*\)"},
            ],
        },
    },
    {
        "id": "web-git-flow",
        "module": 2,
        "step": 6,
        "topic": "Git",
        "title": "Git-сценарий проекта",
        "level": "лёгкое",
        "language": "git",
        "task": (
            "Запиши команды: инициализация репозитория, добавление файлов, первый "
            "коммит, создание ветки feature, переключение на неё, привязка remote "
            "origin и публикация ветки."
        ),
        "requirements": [
            "git init",
            "git add .",
            "git commit -m \"...\"",
            "git branch feature",
            "git checkout feature",
            "git remote add origin <url>",
            "git push -u origin feature",
        ],
        "starter": "# Запиши команды по одной в строке\n",
        "hint": (
            "Порядок: init → add → commit → branch feature → checkout feature → "
            "remote add origin … → push -u origin feature."
        ),
        "solution": (
            "git init\n"
            "git add .\n"
            "git commit -m \"Каркас проекта\"\n"
            "git branch feature\n"
            "git checkout feature\n"
            "git remote add origin https://github.com/user/project.git\n"
            "git push -u origin feature\n"
        ),
        "check": {
            "type": "patterns",
            "require": [
                {"label": "git init", "pattern": r"\bgit\s+init\b"},
                {"label": "git add .", "pattern": r"\bgit\s+add\s+\.\s*$"},
                {"label": "git commit -m", "pattern": r"\bgit\s+commit\s+-m\b"},
                {"label": "git branch feature", "pattern": r"\bgit\s+branch\s+feature\b"},
                {"label": "git checkout feature", "pattern": r"\bgit\s+(checkout|switch)\s+feature\b"},
                {"label": "git remote add origin", "pattern": r"\bgit\s+remote\s+add\s+origin\b"},
                {"label": "git push -u origin feature", "pattern": r"\bgit\s+push\s+-u\s+origin\s+feature\b"},
            ],
        },
    },
    {
        "id": "web-flask-route",
        "module": 3,
        "step": 2,
        "topic": "Flask",
        "title": "Маршрут каталога",
        "level": "среднее",
        "language": "python",
        "task": (
            "Создай Flask-приложение с маршрутом GET /courses. Маршрут должен "
            "отдавать шаблон courses.html и передавать в него список курсов. "
            "Добавь запуск приложения."
        ),
        "requirements": [
            "from flask import Flask, render_template",
            "app = Flask(__name__)",
            "@app.route('/courses')",
            "render_template('courses.html', courses=courses)",
            "app.run(...) в блоке __main__",
        ],
        "starter": (
            "from flask import Flask, render_template\n\n"
            "app = Flask(__name__)\n\n"
            "COURSES = [\n"
            "    {'title': 'Веб и мультимедиа'},\n"
            "    {'title': 'Программист'},\n"
            "]\n\n"
            "# добавь маршрут /courses\n"
        ),
        "hint": (
            "@app.route('/courses')\ndef courses():\n    return "
            "render_template('courses.html', courses=COURSES)\n\n"
            "if __name__ == '__main__':\n    app.run(debug=True)"
        ),
        "solution": (
            "from flask import Flask, render_template\n\n"
            "app = Flask(__name__)\n\n"
            "COURSES = [\n"
            "    {'title': 'Веб и мультимедиа'},\n"
            "    {'title': 'Программист'},\n"
            "]\n\n"
            "@app.route('/courses')\n"
            "def courses():\n"
            "    return render_template('courses.html', courses=COURSES)\n\n"
            "if __name__ == '__main__':\n"
            "    app.run(debug=True)\n"
        ),
        "check": {
            "type": "patterns",
            "language": "python",
            "require": [
                {"label": "импорт Flask", "pattern": r"from\s+flask\s+import\s+.*Flask"},
                {"label": "создание приложения", "pattern": r"Flask\s*\(\s*__name__\s*\)"},
                {"label": "маршрут /courses", "pattern": r"@app\.route\(\s*[\"']/courses[\"']"},
                {"label": "функция courses", "pattern": r"def\s+courses\s*\("},
                {"label": "render_template", "pattern": r"render_template\(\s*[\"']courses\.html[\"']"},
                {"label": "передача courses", "pattern": r"courses\s*=\s*COURSES|courses\s*=\s*courses"},
                {"label": "запуск app.run", "pattern": r"app\.run\s*\("},
            ],
            "forbid": [
                {"label": "пароль в коде", "pattern": r"password\s*=\s*[\"'][^\"']+[\"']"},
            ],
        },
    },
    {
        "id": "web-flask-form",
        "module": 3,
        "step": 4,
        "topic": "Flask",
        "title": "POST-обработка заявки",
        "level": "сложное",
        "language": "python",
        "task": (
            "Добавь маршрут /apply, который принимает GET и POST. На POST прочитай "
            "поля формы, проверь обязательные значения, покажи flash-сообщение и "
            "перенаправь пользователя на каталог."
        ),
        "requirements": [
            "@app.route('/apply', methods=['GET', 'POST'])",
            "request.form.get(...)",
            "Проверка обязательных полей",
            "flash('...', 'success'/'error')",
            "redirect(url_for('courses'))",
        ],
        "starter": (
            "from flask import Flask, render_template, request, flash, redirect, url_for\n\n"
            "app = Flask(__name__)\n"
            "app.secret_key = 'change-me'\n\n"
            "# добавь маршрут /apply\n"
        ),
        "hint": (
            "Внутри POST: full_name = request.form.get('full_name', '').strip(); "
            "if not full_name: flash('Заполните ФИО', 'error'); return redirect(url_for('courses'))."
        ),
        "solution": (
            "from flask import Flask, render_template, request, flash, redirect, url_for\n\n"
            "app = Flask(__name__)\n"
            "app.secret_key = 'change-me'\n\n"
            "@app.route('/apply', methods=['GET', 'POST'])\n"
            "def apply():\n"
            "    if request.method == 'POST':\n"
            "        full_name = request.form.get('full_name', '').strip()\n"
            "        email = request.form.get('email', '').strip()\n"
            "        if not full_name or not email:\n"
            "            flash('Заполните ФИО и e-mail', 'error')\n"
            "            return redirect(url_for('courses'))\n"
            "        flash('Заявка отправлена', 'success')\n"
            "        return redirect(url_for('courses'))\n"
            "    return render_template('apply.html')\n"
        ),
        "check": {
            "type": "patterns",
            "language": "python",
            "require": [
                {"label": "маршрут /apply", "pattern": r"@app\.route\(\s*[\"']/apply[\"']"},
                {"label": "methods с POST", "pattern": r"methods\s*=\s*\[[^\]]*[\"']POST[\"']"},
                {"label": "request.form", "pattern": r"request\.form(\.get)?\("},
                {"label": "проверка обязательных полей", "pattern": r"if\s+not\s+\w+|if\s+\w+\s*==\s*[\"']{2}"},
                {"label": "flash", "pattern": r"flash\s*\("},
                {"label": "redirect", "pattern": r"redirect\s*\("},
                {"label": "url_for", "pattern": r"url_for\s*\("},
            ],
        },
    },
    {
        "id": "web-sql-courses",
        "module": 4,
        "step": 7,
        "topic": "SQL",
        "title": "Курсы и количество заявок",
        "level": "сложное",
        "language": "sql",
        "task": (
            "Выведи название курса и количество заявок на него. Курсы без заявок "
            "тоже должны попасть в результат с нулём. Сортировка: по количеству "
            "по убыванию, затем по названию."
        ),
        "requirements": [
            "LEFT JOIN applications",
            "GROUP BY курс",
            "COUNT(a.application_id)",
            "ORDER BY количество DESC, название",
        ],
        "starter": "SELECT\n  c.title,\n  COUNT(a.application_id) AS cnt\nFROM courses c\n-- добавь JOIN и группировку\n",
        "hint": (
            "LEFT JOIN applications a ON a.course_id = c.course_id, затем "
            "GROUP BY c.course_id, c.title ORDER BY cnt DESC, c.title."
        ),
        "solution": (
            "SELECT c.title, COUNT(a.application_id) AS cnt\n"
            "FROM courses c\n"
            "LEFT JOIN applications a ON a.course_id = c.course_id\n"
            "GROUP BY c.course_id, c.title\n"
            "ORDER BY cnt DESC, c.title;"
        ),
        "check": {
            "type": "sql",
            "expected": (
                "SELECT c.title, COUNT(a.application_id) AS cnt "
                "FROM courses c "
                "LEFT JOIN applications a ON a.course_id = c.course_id "
                "GROUP BY c.course_id, c.title "
                "ORDER BY cnt DESC, c.title;"
            ),
        },
    },
    {
        "id": "web-security-hash",
        "module": 5,
        "step": 2,
        "topic": "Безопасность",
        "title": "Хеширование пароля",
        "level": "сложное",
        "language": "python",
        "task": (
            "Реализуй hash_password(password, salt) на PBKDF2-HMAC-SHA256 с 100 000 "
            "итераций и verify_password(password, salt, digest) через сравнение, "
            "устойчивое к timing-атакам."
        ),
        "requirements": [
            "hashlib.pbkdf2_hmac('sha256', ...)",
            "100_000 итераций",
            "Возврат hex-строки",
            "hmac.compare_digest в verify_password",
            "Пароль не хранится в открытом виде",
        ],
        "starter": (
            "import hashlib\nimport hmac\n\n"
            "def hash_password(password: str, salt: str) -> str:\n"
            "    # верни hex-дайджест\n"
            "    ...\n\n"
            "def verify_password(password: str, salt: str, digest: str) -> bool:\n"
            "    # сравни безопасно\n"
            "    ...\n"
        ),
        "hint": (
            "hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), "
            "100_000).hex(). В verify_password сравни результат с digest через "
            "hmac.compare_digest."
        ),
        "solution": (
            "import hashlib\nimport hmac\n\n"
            "def hash_password(password: str, salt: str) -> str:\n"
            "    return hashlib.pbkdf2_hmac(\n"
            "        'sha256', password.encode('utf-8'), salt.encode('utf-8'), 100_000\n"
            "    ).hex()\n\n"
            "def verify_password(password: str, salt: str, digest: str) -> bool:\n"
            "    return hmac.compare_digest(hash_password(password, salt), digest)\n"
        ),
        "check": {
            "type": "python",
            "offline_require": [
                {"label": "PBKDF2-HMAC-SHA256", "pattern": r"pbkdf2_hmac\(\s*[\"']sha256[\"']"},
                {"label": "100 000 итераций", "pattern": r"100[_\s]?000"},
                {"label": "hex-дайджест", "pattern": r"\.hex\s*\(\s*\)"},
                {"label": "hmac.compare_digest", "pattern": r"compare_digest\s*\("},
                {"label": "две функции", "pattern": r"def\s+hash_password[\s\S]*def\s+verify_password"},
            ],
            "tests": (
                "digest = hash_password('password123', 'demo-salt')\n"
                "print(len(digest))\n"
                "print(verify_password('password123', 'demo-salt', digest))\n"
                "print(verify_password('wrong', 'demo-salt', digest))\n"
            ),
            "expected_output": "64\nTrue\nFalse",
        },
    },
    {
        "id": "web-security-status",
        "module": 5,
        "step": 4,
        "topic": "Экзамен",
        "title": "Смена статуса заявки",
        "level": "сложное",
        "language": "python",
        "task": (
            "Напиши set_status(conn, application_id, status_id), которая меняет "
            "статус заявки параметризованным UPDATE, фиксирует изменения и "
            "возвращает True, если строка обновилась."
        ),
        "requirements": [
            "Параметризованный запрос с ?",
            "UPDATE applications SET status_id = ? WHERE application_id = ?",
            "conn.commit()",
            "Возврат cur.rowcount > 0",
            "Никакой f-string со значениями в SQL",
        ],
        "starter": (
            "def set_status(conn, application_id: int, status_id: int) -> bool:\n"
            "    # обнови статус и верни результат\n"
            "    ...\n"
        ),
        "hint": (
            "cur = conn.execute('UPDATE applications SET status_id = ? WHERE "
            "application_id = ?', (status_id, application_id)); conn.commit(); "
            "return cur.rowcount > 0."
        ),
        "solution": (
            "def set_status(conn, application_id: int, status_id: int) -> bool:\n"
            "    cur = conn.execute(\n"
            "        'UPDATE applications SET status_id = ? WHERE application_id = ?',\n"
            "        (status_id, application_id),\n"
            "    )\n"
            "    conn.commit()\n"
            "    return cur.rowcount > 0\n"
        ),
        "check": {
            "type": "python",
            "offline_require": [
                {"label": "UPDATE applications", "pattern": r"UPDATE\s+applications\s+SET\s+status_id\s*=\s*\?"},
                {"label": "WHERE application_id = ?", "pattern": r"WHERE\s+application_id\s*=\s*\?"},
                {"label": "параметры кортежем", "pattern": r"\(\s*status_id\s*,\s*application_id\s*\)|\(\s*application_id\s*,\s*status_id\s*\)"},
                {"label": "commit", "pattern": r"\.commit\s*\(\s*\)"},
                {"label": "rowcount", "pattern": r"rowcount\s*>\s*0"},
            ],
            "tests": (
                "import sqlite3\n"
                "con = sqlite3.connect(':memory:')\n"
                "con.execute('CREATE TABLE applications (application_id INTEGER PRIMARY KEY, status_id INTEGER)')\n"
                "con.execute('INSERT INTO applications VALUES (1, 1), (2, 2)')\n"
                "print(set_status(con, 1, 3))\n"
                "print(con.execute('SELECT status_id FROM applications WHERE application_id = 1').fetchone()[0])\n"
                "print(set_status(con, 99, 3))\n"
            ),
            "expected_output": "True\n3\nFalse",
        },
    },
    {
        "id": "web-design-tokens",
        "module": 5,
        "step": 6,
        "topic": "Дизайн",
        "title": "Дизайн-токены и доступность",
        "level": "среднее",
        "language": "css",
        "task": (
            "Собери мини-дизайн-систему: CSS-переменные для цветов и радиуса, "
            "кнопка использует их через var(), у кнопки виден фокус с клавиатуры, "
            "анимации отключаются при prefers-reduced-motion."
        ),
        "requirements": [
            ":root с переменными --brand, --radius",
            "var(--brand) внутри .btn",
            ":focus-visible с outline",
            "@media (prefers-reduced-motion: reduce)",
        ],
        "starter": ":root {\n  /* токены */\n}\n\n.btn {\n  /* кнопка */\n}\n",
        "hint": (
            ":root { --brand:#00a36c; --radius:10px; } .btn { background: var(--brand); "
            "border-radius: var(--radius); } .btn:focus-visible { outline: 3px solid ... }"
        ),
        "solution": (
            ":root {\n"
            "  --brand: #00a36c;\n"
            "  --brand-dark: #00875a;\n"
            "  --radius: 10px;\n"
            "}\n\n"
            ".btn {\n"
            "  background: var(--brand);\n"
            "  color: #fff;\n"
            "  border-radius: var(--radius);\n"
            "  padding: 10px 16px;\n"
            "  transition: transform .15s ease;\n"
            "}\n\n"
            ".btn:hover { background: var(--brand-dark); }\n\n"
            ".btn:focus-visible {\n"
            "  outline: 3px solid #1d4ed8;\n"
            "  outline-offset: 2px;\n"
            "}\n\n"
            "@media (prefers-reduced-motion: reduce) {\n"
            "  .btn { transition: none; }\n"
            "}\n"
        ),
        "check": {
            "type": "patterns",
            "require": [
                {"label": ":root с переменными", "pattern": r":root\s*\{[^}]*--[a-z-]+\s*:"},
                {"label": "var(--brand)", "pattern": r"var\(\s*--brand\s*\)"},
                {"label": "border-radius через var", "pattern": r"border-radius\s*:\s*var\("},
                {"label": ":focus-visible", "pattern": r":focus-visible\s*\{"},
                {"label": "outline в фокусе", "pattern": r":focus-visible\s*\{[^}]*outline\s*:"},
                {"label": "prefers-reduced-motion", "pattern": r"@media\s*\([^)]*prefers-reduced-motion\s*:\s*reduce"},
            ],
        },
    },
    {
        "id": "web-final-application",
        "module": 5,
        "step": 8,
        "topic": "Экзамен",
        "title": "Итог: заявка с записью в БД",
        "level": "сложное",
        "language": "python",
        "task": (
            "Собери итоговый обработчик заявки: маршрут /apply с GET и POST, "
            "чтение полей формы, проверка, параметризованный INSERT в SQLite, "
            "commit, flash и редирект. Это уменьшенная копия модуля 3 экзамена."
        ),
        "requirements": [
            "Flask, request, flash, redirect, url_for",
            "@app.route('/apply', methods=['GET', 'POST'])",
            "request.form.get(...) и проверка",
            "conn.execute('INSERT ... VALUES (?, ?)', (...))",
            "conn.commit() и flash",
            "redirect(url_for('courses'))",
        ],
        "starter": (
            "import sqlite3\n"
            "from flask import Flask, request, render_template, flash, redirect, url_for\n\n"
            "app = Flask(__name__)\n"
            "app.secret_key = 'change-me'\n"
            "conn = sqlite3.connect('applications.db', check_same_thread=False)\n\n"
            "# добавь маршрут /apply\n"
        ),
        "hint": (
            "Сначала проверь поля, затем выполни INSERT с ?-параметрами: "
            "conn.execute('INSERT INTO applications (full_name, email) VALUES (?, ?)', "
            "(full_name, email)); conn.commit()."
        ),
        "solution": (
            "import sqlite3\n"
            "from flask import Flask, request, render_template, flash, redirect, url_for\n\n"
            "app = Flask(__name__)\n"
            "app.secret_key = 'change-me'\n"
            "conn = sqlite3.connect('applications.db', check_same_thread=False)\n\n"
            "@app.route('/apply', methods=['GET', 'POST'])\n"
            "def apply():\n"
            "    if request.method == 'POST':\n"
            "        full_name = request.form.get('full_name', '').strip()\n"
            "        email = request.form.get('email', '').strip()\n"
            "        course_id = request.form.get('course_id', '').strip()\n"
            "        if not (full_name and email and course_id):\n"
            "            flash('Заполните все поля', 'error')\n"
            "            return redirect(url_for('apply'))\n"
            "        conn.execute(\n"
            "            'INSERT INTO applications (full_name, email, course_id) VALUES (?, ?, ?)',\n"
            "            (full_name, email, course_id),\n"
            "        )\n"
            "        conn.commit()\n"
            "        flash('Заявка сохранена', 'success')\n"
            "        return redirect(url_for('courses'))\n"
            "    return render_template('apply.html')\n"
        ),
        "check": {
            "type": "patterns",
            "language": "python",
            "require": [
                {"label": "маршрут /apply", "pattern": r"@app\.route\(\s*[\"']/apply[\"']"},
                {"label": "methods GET/POST", "pattern": r"methods\s*=\s*\[[^\]]*[\"']POST[\"']"},
                {"label": "request.form.get", "pattern": r"request\.form\.get\("},
                {"label": "проверка полей", "pattern": r"if\s+not\s+\(|if\s+not\s+\w+"},
                {"label": "параметризованный INSERT", "pattern": r"INSERT\s+INTO[\s\S]*VALUES\s*\([^)]*\?"},
                {"label": "commit", "pattern": r"\.commit\s*\(\s*\)"},
                {"label": "flash", "pattern": r"flash\s*\("},
                {"label": "redirect", "pattern": r"redirect\s*\("},
                {"label": "url_for", "pattern": r"url_for\s*\("},
            ],
            "forbid": [
                {"label": "конкатенация значений в SQL", "pattern": r"INSERT[\s\S]*\+\s*(full_name|email)|f[\"']INSERT"},
            ],
        },
    },
]

# ---------------------------------------------------------------------------
# ПРОГРАММИСТ · 09.02.07-2
# ---------------------------------------------------------------------------
PROGRAMMER = [
    {
        "id": "prog-exam-score",
        "module": 1,
        "step": 2,
        "topic": "Экзамен",
        "title": "Подсчёт баллов экзамена",
        "level": "лёгкое",
        "language": "python",
        "task": (
            "Напиши total_score(invariant, variant): инвариант даёт 0–75 баллов, "
            "вариативная часть — 0–25. Функция возвращает сумму, а при выходе за "
            "границы выбрасывает ValueError."
        ),
        "requirements": [
            "Проверка 0 <= invariant <= 75",
            "Проверка 0 <= variant <= 25",
            "При ошибке — ValueError",
            "Возврат суммы баллов",
        ],
        "starter": (
            "def total_score(invariant: int, variant: int) -> int:\n"
            "    # проверь диапазоны и верни сумму\n"
            "    ...\n"
        ),
        "hint": (
            "if not 0 <= invariant <= 75: raise ValueError('...'). Затем то же для "
            "variant и return invariant + variant."
        ),
        "solution": (
            "def total_score(invariant: int, variant: int) -> int:\n"
            "    if not 0 <= invariant <= 75:\n"
            "        raise ValueError('Инвариант: 0–75 баллов')\n"
            "    if not 0 <= variant <= 25:\n"
            "        raise ValueError('Вариативная часть: 0–25 баллов')\n"
            "    return invariant + variant\n"
        ),
        "check": {
            "type": "python",
            "offline_require": [
                {"label": "def total_score", "pattern": r"def\s+total_score\s*\("},
                {"label": "проверка инварианта", "pattern": r"invariant\s*>=\s*0|0\s*<=\s*invariant"},
                {"label": "проверка варианта", "pattern": r"variant\s*>=\s*0|0\s*<=\s*variant"},
                {"label": "ValueError", "pattern": r"raise\s+ValueError"},
                {"label": "возврат суммы", "pattern": r"return\s+invariant\s*\+\s*variant"},
            ],
            "tests": (
                "print(total_score(60, 20))\n"
                "print(total_score(0, 0))\n"
                "try:\n"
                "    total_score(80, 0)\n"
                "except ValueError:\n"
                "    print('ValueError')\n"
                "try:\n"
                "    total_score(50, -1)\n"
                "except ValueError:\n"
                "    print('ValueError')\n"
            ),
            "expected_output": "80\n0\nValueError\nValueError",
        },
    },
    {
        "id": "prog-types-card",
        "module": 1,
        "step": 4,
        "topic": "Python",
        "title": "Карточка товара",
        "level": "лёгкое",
        "language": "python",
        "task": (
            "Функция product_card(name, price, discount=0) возвращает строку "
            "«Название — итоговая цена ₽» с двумя знаками после точки. Скидка "
            "задаётся долей от 0 до 1."
        ),
        "requirements": [
            "Параметр discount по умолчанию 0",
            "Итоговая цена = price * (1 - discount)",
            "Формат цены с двумя знаками",
            "Строка содержит название и знак ₽",
        ],
        "starter": (
            "def product_card(name: str, price: float, discount: float = 0) -> str:\n"
            "    # рассчитай цену и собери строку\n"
            "    ...\n"
        ),
        "hint": (
            "final = price * (1 - discount); return f\"{name} — {final:.2f} ₽\"."
        ),
        "solution": (
            "def product_card(name: str, price: float, discount: float = 0) -> str:\n"
            "    final = price * (1 - discount)\n"
            "    return f\"{name} — {final:.2f} ₽\"\n"
        ),
        "check": {
            "type": "python",
            "offline_require": [
                {"label": "def product_card", "pattern": r"def\s+product_card\s*\("},
                {"label": "discount по умолчанию", "pattern": r"discount\s*[:=].*0|discount\s*=\s*0"},
                {"label": "расчёт скидки", "pattern": r"\*\s*\(\s*1\s*-\s*discount\s*\)"},
                {"label": "два знака после точки", "pattern": r":\.2f"},
                {"label": "return", "pattern": r"return\s+"},
            ],
            "tests": (
                "print(product_card('Кроссовки City Run', 4590))\n"
                "print(product_card('Ботинки Classic', 7890, 0.1))\n"
                "print(product_card('Туфли Office', 6290, 0.2))\n"
            ),
            "expected_output": (
                "Кроссовки City Run — 4590.00 ₽\n"
                "Ботинки Classic — 7101.00 ₽\n"
                "Туфли Office — 5032.00 ₽"
            ),
        },
    },
    {
        "id": "prog-collections-filter",
        "module": 1,
        "step": 6,
        "topic": "Python",
        "title": "Фильтр каталога",
        "level": "среднее",
        "language": "python",
        "task": (
            "Реализуй filter_products(products, manufacturer=None, max_price=None). "
            "Функция фильтрует список словарей по производителю и максимальной цене "
            "и возвращает результат, отсортированный по цене."
        ),
        "requirements": [
            "Учёт manufacturer, если он передан",
            "Учёт max_price, если он передан",
            "Сортировка по ключу price",
            "Исходный список не изменяется",
        ],
        "starter": (
            "def filter_products(products, manufacturer=None, max_price=None):\n"
            "    # отфильтруй и отсортируй\n"
            "    ...\n"
        ),
        "hint": (
            "result = [p for p in products if (manufacturer is None or "
            "p['manufacturer'] == manufacturer) and (max_price is None or "
            "p['price'] <= max_price)]; return sorted(result, key=lambda p: p['price'])."
        ),
        "solution": (
            "def filter_products(products, manufacturer=None, max_price=None):\n"
            "    result = [\n"
            "        p for p in products\n"
            "        if (manufacturer is None or p['manufacturer'] == manufacturer)\n"
            "        and (max_price is None or p['price'] <= max_price)\n"
            "    ]\n"
            "    return sorted(result, key=lambda p: p['price'])\n"
        ),
        "check": {
            "type": "python",
            "offline_require": [
                {"label": "def filter_products", "pattern": r"def\s+filter_products\s*\("},
                {"label": "фильтр по manufacturer", "pattern": r"manufacturer"},
                {"label": "фильтр по max_price", "pattern": r"max_price"},
                {"label": "сортировка sorted", "pattern": r"sorted\s*\("},
                {"label": "ключ price", "pattern": r"key\s*=.*price"},
                {"label": "return", "pattern": r"return\s+"},
            ],
            "tests": (
                "items = [\n"
                "    {'name': 'A', 'manufacturer': 'Азимут', 'price': 4590},\n"
                "    {'name': 'B', 'manufacturer': 'Марко', 'price': 7890},\n"
                "    {'name': 'C', 'manufacturer': 'Азимут', 'price': 3290},\n"
                "]\n"
                "print([p['name'] for p in filter_products(items)])\n"
                "print([p['name'] for p in filter_products(items, manufacturer='Азимут')])\n"
                "print([p['name'] for p in filter_products(items, max_price=5000)])\n"
            ),
            "expected_output": "['C', 'A', 'B']\n['C', 'A']\n['C', 'A']",
        },
    },
    {
        "id": "prog-exceptions-file",
        "module": 1,
        "step": 8,
        "topic": "Python",
        "title": "Безопасное чтение файла",
        "level": "среднее",
        "language": "python",
        "task": (
            "Напиши read_text(path, default='') — читает UTF-8 файл и возвращает "
            "текст. Если файла нет или он недоступен, возвращает default, а не "
            "роняет программу."
        ),
        "requirements": [
            "Открытие с encoding='utf-8'",
            "Обработка FileNotFoundError/OSError",
            "Возврат default при ошибке",
            "with open(...) для закрытия файла",
        ],
        "starter": (
            "def read_text(path: str, default: str = '') -> str:\n"
            "    # прочитай файл безопасно\n"
            "    ...\n"
        ),
        "hint": (
            "try:\n    with open(path, encoding='utf-8') as f:\n        return f.read()\n"
            "except OSError:\n    return default"
        ),
        "solution": (
            "def read_text(path: str, default: str = '') -> str:\n"
            "    try:\n"
            "        with open(path, encoding='utf-8') as f:\n"
            "            return f.read()\n"
            "    except OSError:\n"
            "        return default\n"
        ),
        "check": {
            "type": "python",
            "offline_require": [
                {"label": "def read_text", "pattern": r"def\s+read_text\s*\("},
                {"label": "try/except", "pattern": r"try\s*:[\s\S]*except\s+(OSError|FileNotFoundError)"},
                {"label": "encoding='utf-8'", "pattern": r"encoding\s*=\s*[\"']utf-8[\"']"},
                {"label": "with open", "pattern": r"with\s+open\s*\("},
                {"label": "возврат default", "pattern": r"return\s+default"},
            ],
            "tests": (
                "import tempfile, pathlib\n"
                "p = pathlib.Path(tempfile.gettempdir()) / 'demo_read_text.txt'\n"
                "p.write_text('привет', encoding='utf-8')\n"
                "print(read_text(str(p)))\n"
                "print(read_text(str(p) + '.nope', 'нет файла'))\n"
                "print(read_text(str(p) + '.nope'))\n"
            ),
            "expected_output": "привет\nнет файла\n",
        },
    },
    {
        "id": "prog-db-ddl",
        "module": 2,
        "step": 2,
        "topic": "БД",
        "title": "DDL: таблица товаров",
        "level": "сложное",
        "language": "sql",
        "task": (
            "Создай три таблицы: categories, manufacturers и products. В products "
            "нужны первичный ключ, название NOT NULL, цена с CHECK >= 0, количество "
            "с DEFAULT 0, скидка с CHECK от 0 до 1 и внешние ключи на справочники."
        ),
        "requirements": [
            "CREATE TABLE categories и manufacturers",
            "products с PRIMARY KEY",
            "name TEXT NOT NULL",
            "price REAL CHECK (price >= 0)",
            "quantity INTEGER DEFAULT 0",
            "discount CHECK (discount BETWEEN 0 AND 1)",
            "FOREIGN KEY на category_id и manufacturer_id",
        ],
        "starter": (
            "CREATE TABLE categories (\n"
            "  category_id INTEGER PRIMARY KEY,\n"
            "  category_name TEXT NOT NULL UNIQUE\n"
            ");\n\n"
            "-- добавь manufacturers и products\n"
        ),
        "hint": (
            "Для products: product_id INTEGER PRIMARY KEY, name TEXT NOT NULL, "
            "price REAL NOT NULL CHECK (price >= 0), quantity INTEGER DEFAULT 0, "
            "discount REAL DEFAULT 0 CHECK (discount BETWEEN 0 AND 1), "
            "FOREIGN KEY (category_id) REFERENCES categories(category_id)."
        ),
        "solution": (
            "CREATE TABLE categories (\n"
            "  category_id INTEGER PRIMARY KEY,\n"
            "  category_name TEXT NOT NULL UNIQUE\n"
            ");\n\n"
            "CREATE TABLE manufacturers (\n"
            "  manufacturer_id INTEGER PRIMARY KEY,\n"
            "  manufacturer_name TEXT NOT NULL UNIQUE\n"
            ");\n\n"
            "CREATE TABLE products (\n"
            "  product_id INTEGER PRIMARY KEY,\n"
            "  name TEXT NOT NULL,\n"
            "  price REAL NOT NULL CHECK (price >= 0),\n"
            "  quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),\n"
            "  discount REAL NOT NULL DEFAULT 0 CHECK (discount BETWEEN 0 AND 1),\n"
            "  category_id INTEGER NOT NULL,\n"
            "  manufacturer_id INTEGER NOT NULL,\n"
            "  FOREIGN KEY (category_id) REFERENCES categories(category_id),\n"
            "  FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(manufacturer_id)\n"
            ");\n"
        ),
        "check": {
            "type": "ddl",
            "schema_sql": "",
            "expected": (
                "CREATE TABLE categories (category_id INTEGER PRIMARY KEY, category_name TEXT NOT NULL UNIQUE);\n"
                "CREATE TABLE manufacturers (manufacturer_id INTEGER PRIMARY KEY, manufacturer_name TEXT NOT NULL UNIQUE);\n"
                "CREATE TABLE products ("
                "product_id INTEGER PRIMARY KEY, name TEXT NOT NULL, "
                "price REAL NOT NULL CHECK (price >= 0), "
                "quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0), "
                "discount REAL NOT NULL DEFAULT 0 CHECK (discount BETWEEN 0 AND 1), "
                "category_id INTEGER NOT NULL, manufacturer_id INTEGER NOT NULL, "
                "FOREIGN KEY (category_id) REFERENCES categories(category_id), "
                "FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(manufacturer_id));"
            ),
            "verify": (
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;"
            ),
            "require": [
                {"label": "PRIMARY KEY", "pattern": r"PRIMARY\s+KEY"},
                {"label": "NOT NULL", "pattern": r"NOT\s+NULL"},
                {"label": "CHECK для цены", "pattern": r"CHECK\s*\(\s*price\s*>=\s*0"},
                {"label": "DEFAULT 0", "pattern": r"DEFAULT\s+0"},
                {"label": "CHECK для скидки", "pattern": r"discount[\s\S]*CHECK\s*\(\s*discount\s*(BETWEEN\s+0\s+AND\s+1|>=\s*0[\s\S]*<=\s*1)"},
                {"label": "FOREIGN KEY", "pattern": r"FOREIGN\s+KEY"},
            ],
        },
    },
    {
        "id": "prog-db-3nf",
        "module": 2,
        "step": 4,
        "topic": "БД",
        "title": "Нормализация заказов",
        "level": "сложное",
        "language": "sql",
        "task": (
            "Приведи заказы к 3НФ: отдельная таблица products, orders и "
            "order_items со составным первичным ключом (order_id, product_id). "
            "Количество и цена хранятся в позиции заказа, а не в orders."
        ),
        "requirements": [
            "CREATE TABLE products",
            "CREATE TABLE orders",
            "CREATE TABLE order_items",
            "Составной PRIMARY KEY (order_id, product_id)",
            "FOREIGN KEY на orders и products",
            "quantity INTEGER CHECK (quantity > 0)",
        ],
        "starter": (
            "CREATE TABLE products (\n"
            "  product_id INTEGER PRIMARY KEY,\n"
            "  name TEXT NOT NULL,\n"
            "  price REAL NOT NULL CHECK (price >= 0)\n"
            ");\n\n"
            "-- добавь orders и order_items\n"
        ),
        "hint": (
            "order_items: order_id INTEGER, product_id INTEGER, quantity INTEGER "
            "CHECK (quantity > 0), PRIMARY KEY (order_id, product_id), "
            "FOREIGN KEY (order_id) REFERENCES orders(order_id), "
            "FOREIGN KEY (product_id) REFERENCES products(product_id)."
        ),
        "solution": (
            "CREATE TABLE products (\n"
            "  product_id INTEGER PRIMARY KEY,\n"
            "  name TEXT NOT NULL,\n"
            "  price REAL NOT NULL CHECK (price >= 0)\n"
            ");\n\n"
            "CREATE TABLE orders (\n"
            "  order_id INTEGER PRIMARY KEY,\n"
            "  customer_name TEXT NOT NULL,\n"
            "  order_date TEXT NOT NULL\n"
            ");\n\n"
            "CREATE TABLE order_items (\n"
            "  order_id INTEGER NOT NULL,\n"
            "  product_id INTEGER NOT NULL,\n"
            "  quantity INTEGER NOT NULL CHECK (quantity > 0),\n"
            "  price REAL NOT NULL CHECK (price >= 0),\n"
            "  PRIMARY KEY (order_id, product_id),\n"
            "  FOREIGN KEY (order_id) REFERENCES orders(order_id),\n"
            "  FOREIGN KEY (product_id) REFERENCES products(product_id)\n"
            ");\n"
        ),
        "check": {
            "type": "ddl",
            "schema_sql": "",
            "expected": (
                "CREATE TABLE products (product_id INTEGER PRIMARY KEY, name TEXT NOT NULL, price REAL NOT NULL CHECK (price >= 0));\n"
                "CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_name TEXT NOT NULL, order_date TEXT NOT NULL);\n"
                "CREATE TABLE order_items (order_id INTEGER NOT NULL, product_id INTEGER NOT NULL, "
                "quantity INTEGER NOT NULL CHECK (quantity > 0), price REAL NOT NULL CHECK (price >= 0), "
                "PRIMARY KEY (order_id, product_id), "
                "FOREIGN KEY (order_id) REFERENCES orders(order_id), "
                "FOREIGN KEY (product_id) REFERENCES products(product_id));"
            ),
            "verify": (
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;"
            ),
            "require": [
                {"label": "products", "pattern": r"CREATE\s+TABLE\s+products"},
                {"label": "orders", "pattern": r"CREATE\s+TABLE\s+orders"},
                {"label": "order_items", "pattern": r"CREATE\s+TABLE\s+order_items"},
                {"label": "составной ключ", "pattern": r"PRIMARY\s+KEY\s*\(\s*order_id\s*,\s*product_id\s*\)"},
                {"label": "FOREIGN KEY на orders", "pattern": r"FOREIGN\s+KEY\s*\(\s*order_id\s*\)\s*REFERENCES\s+orders"},
                {"label": "FOREIGN KEY на products", "pattern": r"FOREIGN\s+KEY\s*\(\s*product_id\s*\)\s*REFERENCES\s+products"},
                {"label": "CHECK quantity", "pattern": r"quantity[\s\S]*CHECK\s*\(\s*quantity\s*>\s*0"},
            ],
        },
    },
    {
        "id": "prog-algorithm-discount",
        "module": 2,
        "step": 6,
        "topic": "Экзамен",
        "title": "Алгоритм расчёта скидки",
        "level": "среднее",
        "language": "python",
        "task": (
            "Опиши алгоритм discount_percent(amount): до 2000 — 0%, от 2000 — 5%, "
            "от 5000 — 10%. Добавь docstring с шагами алгоритма, как требуют "
            "критерии блок-схемы."
        ),
        "requirements": [
            "Docstring с описанием шагов",
            "Ветка amount >= 5000 → 10",
            "Ветка amount >= 2000 → 5",
            "Иначе 0",
            "Отрицательная сумма → ValueError",
        ],
        "starter": (
            "def discount_percent(amount: float) -> int:\n"
            "    \"\"\"Вернуть скидку в процентах.\n\n"
            "    Шаги:\n"
            "    1. ...\n"
            "    \"\"\"\n"
            "    # реализуй ветвления\n"
            "    ...\n"
        ),
        "hint": (
            "Сначала проверь отрицательное значение, затем иди от большего порога "
            "к меньшему: if amount >= 5000: return 10; if amount >= 2000: return 5; return 0."
        ),
        "solution": (
            "def discount_percent(amount: float) -> int:\n"
            "    \"\"\"Вернуть скидку в процентах.\n\n"
            "    Шаги:\n"
            "    1. Если сумма отрицательная — ошибка.\n"
            "    2. Если сумма >= 5000 — скидка 10%.\n"
            "    3. Если сумма >= 2000 — скидка 5%.\n"
            "    4. Иначе скидка 0%.\n"
            "    \"\"\"\n"
            "    if amount < 0:\n"
            "        raise ValueError('Сумма не может быть отрицательной')\n"
            "    if amount >= 5000:\n"
            "        return 10\n"
            "    if amount >= 2000:\n"
            "        return 5\n"
            "    return 0\n"
        ),
        "check": {
            "type": "python",
            "offline_require": [
                {"label": "def discount_percent", "pattern": r"def\s+discount_percent\s*\("},
                {"label": "docstring", "pattern": r"def\s+discount_percent[\s\S]*?[\"']{3}"},
                {"label": "порог 5000", "pattern": r"amount\s*>=\s*5000"},
                {"label": "порог 2000", "pattern": r"amount\s*>=\s*2000"},
                {"label": "возврат 10/5/0", "pattern": r"return\s+10[\s\S]*return\s+5[\s\S]*return\s+0"},
                {"label": "ValueError", "pattern": r"raise\s+ValueError"},
            ],
            "tests": (
                "print(discount_percent(1999))\n"
                "print(discount_percent(2000))\n"
                "print(discount_percent(5000))\n"
                "print(discount_percent(9999))\n"
                "try:\n"
                "    discount_percent(-1)\n"
                "except ValueError:\n"
                "    print('ValueError')\n"
                "print(bool(discount_percent.__doc__))\n"
            ),
            "expected_output": "0\n5\n10\n10\nValueError\nTrue",
        },
    },
    {
        "id": "prog-tkinter-catalog",
        "module": 3,
        "step": 2,
        "topic": "UI",
        "title": "Окно каталога на tkinter",
        "level": "среднее",
        "language": "python",
        "task": (
            "Собери окно каталога: заголовок, таблица Treeview с колонками "
            "«Артикул», «Название», «Цена», полоса прокрутки и кнопка "
            "«Обновить». Используй ttk."
        ),
        "requirements": [
            "import tkinter as tk и from tkinter import ttk",
            "Tk() и title(...)",
            "ttk.Treeview с columns",
            "heading для каждой колонки",
            "ttk.Scrollbar или pack/grid",
            "mainloop()",
        ],
        "starter": (
            "import tkinter as tk\n"
            "from tkinter import ttk\n\n"
            "root = tk.Tk()\n"
            "root.title('Каталог товаров')\n\n"
            "# добавь таблицу и кнопку\n\n"
            "root.mainloop()\n"
        ),
        "hint": (
            "tree = ttk.Treeview(root, columns=('article', 'name', 'price'), "
            "show='headings'); tree.heading('article', text='Артикул'); ...; "
            "tree.pack(fill='both', expand=True)."
        ),
        "solution": (
            "import tkinter as tk\n"
            "from tkinter import ttk\n\n"
            "root = tk.Tk()\n"
            "root.title('Каталог товаров')\n"
            "root.geometry('900x500')\n\n"
            "tree = ttk.Treeview(root, columns=('article', 'name', 'price'), show='headings')\n"
            "tree.heading('article', text='Артикул')\n"
            "tree.heading('name', text='Название')\n"
            "tree.heading('price', text='Цена')\n"
            "tree.column('price', anchor='e', width=100)\n"
            "tree.pack(fill='both', expand=True, padx=12, pady=12)\n\n"
            "scroll = ttk.Scrollbar(root, orient='vertical', command=tree.yview)\n"
            "tree.configure(yscrollcommand=scroll.set)\n\n"
            "ttk.Button(root, text='Обновить').pack(pady=(0, 12))\n\n"
            "root.mainloop()\n"
        ),
        "check": {
            "type": "patterns",
            "language": "python",
            "require": [
                {"label": "import tkinter", "pattern": r"import\s+tkinter\s+as\s+tk"},
                {"label": "from tkinter import ttk", "pattern": r"from\s+tkinter\s+import\s+.*ttk"},
                {"label": "Tk()", "pattern": r"\bTk\s*\(\s*\)"},
                {"label": "title(...)", "pattern": r"\.title\s*\("},
                {"label": "ttk.Treeview", "pattern": r"ttk\.Treeview\s*\("},
                {"label": "columns", "pattern": r"columns\s*="},
                {"label": "heading", "pattern": r"\.heading\s*\("},
                {"label": "Scrollbar", "pattern": r"Scrollbar\s*\("},
                {"label": "mainloop", "pattern": r"\.mainloop\s*\(\s*\)"},
            ],
        },
    },
    {
        "id": "prog-sql-products",
        "module": 3,
        "step": 4,
        "topic": "Экзамен",
        "title": "SQL: товары и производители",
        "level": "среднее",
        "language": "sql",
        "task": (
            "Выведи название товара, производителя, цену и остаток для товаров "
            "с остатком больше нуля. Сортировка по цене по убыванию, затем по "
            "названию."
        ),
        "requirements": [
            "JOIN manufacturers",
            "WHERE quantity > 0",
            "ORDER BY price DESC, name",
            "Нужные столбцы: name, manufacturer_name, price, quantity",
        ],
        "starter": (
            "SELECT p.name, m.manufacturer_name, p.price, p.quantity\n"
            "FROM products p\n"
            "-- добавь JOIN, WHERE и ORDER BY\n"
        ),
        "hint": (
            "JOIN manufacturers m ON m.manufacturer_id = p.manufacturer_id, "
            "WHERE p.quantity > 0, ORDER BY p.price DESC, p.name."
        ),
        "solution": (
            "SELECT p.name, m.manufacturer_name, p.price, p.quantity\n"
            "FROM products p\n"
            "JOIN manufacturers m ON m.manufacturer_id = p.manufacturer_id\n"
            "WHERE p.quantity > 0\n"
            "ORDER BY p.price DESC, p.name;"
        ),
        "check": {
            "type": "sql",
            "expected": (
                "SELECT p.name, m.manufacturer_name, p.price, p.quantity "
                "FROM products p "
                "JOIN manufacturers m ON m.manufacturer_id = p.manufacturer_id "
                "WHERE p.quantity > 0 ORDER BY p.price DESC, p.name;"
            ),
        },
    },
    {
        "id": "prog-crud-add",
        "module": 4,
        "step": 2,
        "topic": "Экзамен",
        "title": "Добавление товара в БД",
        "level": "сложное",
        "language": "python",
        "task": (
            "Напиши add_product(conn, data): параметризованный INSERT в products "
            "(name, price, quantity), commit и возврат нового product_id."
        ),
        "requirements": [
            "INSERT с ?-параметрами",
            "Значения из словаря data",
            "conn.commit()",
            "Возврат lastrowid",
            "Никакой конкатенации SQL",
        ],
        "starter": (
            "def add_product(conn, data: dict) -> int:\n"
            "    # вставь товар и верни id\n"
            "    ...\n"
        ),
        "hint": (
            "cur = conn.execute('INSERT INTO products (name, price, quantity) "
            "VALUES (?, ?, ?)', (data['name'], data['price'], data.get('quantity', 0))); "
            "conn.commit(); return cur.lastrowid."
        ),
        "solution": (
            "def add_product(conn, data: dict) -> int:\n"
            "    cur = conn.execute(\n"
            "        'INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)',\n"
            "        (data['name'], data['price'], data.get('quantity', 0)),\n"
            "    )\n"
            "    conn.commit()\n"
            "    return cur.lastrowid\n"
        ),
        "check": {
            "type": "python",
            "offline_require": [
                {"label": "def add_product", "pattern": r"def\s+add_product\s*\("},
                {"label": "INSERT INTO products", "pattern": r"INSERT\s+INTO\s+products"},
                {"label": "VALUES с ?", "pattern": r"VALUES\s*\([^)]*\?[^)]*\?[^)]*\?\)"},
                {"label": "commit", "pattern": r"\.commit\s*\(\s*\)"},
                {"label": "lastrowid", "pattern": r"lastrowid"},
            ],
            "tests": (
                "import sqlite3\n"
                "con = sqlite3.connect(':memory:')\n"
                "con.execute('CREATE TABLE products (product_id INTEGER PRIMARY KEY, name TEXT, price REAL, quantity INTEGER)')\n"
                "new_id = add_product(con, {'name': 'Кроссовки City Run', 'price': 4590})\n"
                "print(new_id)\n"
                "print(con.execute('SELECT name, price, quantity FROM products').fetchall())\n"
                "print(add_product(con, {'name': 'Туфли Office', 'price': 6290, 'quantity': 12}))\n"
            ),
            "expected_output": "1\n[('Кроссовки City Run', 4590.0, 0)]\n2",
        },
    },
    {
        "id": "prog-final-order",
        "module": 4,
        "step": 4,
        "topic": "Экзамен",
        "title": "Итог: стоимость заказа",
        "level": "сложное",
        "language": "python",
        "task": (
            "Реализуй order_total(items, discount=0): items — список словарей "
            "с price и quantity. Нужно посчитать сумму, применить скидку 0–1 и "
            "округлить до копеек. Пустой заказ даёт 0."
        ),
        "requirements": [
            "Сумма price * quantity по всем позициям",
            "Скидка discount от 0 до 1",
            "Округление до 2 знаков",
            "Пустой список → 0.0",
            "Некорректная скидка → ValueError",
        ],
        "starter": (
            "def order_total(items, discount: float = 0) -> float:\n"
            "    # посчитай итог заказа\n"
            "    ...\n"
        ),
        "hint": (
            "if not 0 <= discount <= 1: raise ValueError(...); total = sum("
            "item['price'] * item['quantity'] for item in items); "
            "return round(total * (1 - discount), 2)."
        ),
        "solution": (
            "def order_total(items, discount: float = 0) -> float:\n"
            "    if not 0 <= discount <= 1:\n"
            "        raise ValueError('Скидка должна быть от 0 до 1')\n"
            "    total = sum(item['price'] * item['quantity'] for item in items)\n"
            "    return round(total * (1 - discount), 2)\n"
        ),
        "check": {
            "type": "python",
            "offline_require": [
                {"label": "def order_total", "pattern": r"def\s+order_total\s*\("},
                {"label": "сумма по позициям", "pattern": r"sum\s*\("},
                {"label": "price * quantity", "pattern": r"price[\s\S]{0,20}\*[\s\S]{0,20}quantity|quantity[\s\S]{0,20}\*[\s\S]{0,20}price"},
                {"label": "скидка 0..1", "pattern": r"discount"},
                {"label": "округление", "pattern": r"round\s*\("},
                {"label": "ValueError", "pattern": r"raise\s+ValueError"},
            ],
            "tests": (
                "items = [\n"
                "    {'price': 4590, 'quantity': 1},\n"
                "    {'price': 6290, 'quantity': 2},\n"
                "]\n"
                "print(order_total(items))\n"
                "print(order_total(items, 0.1))\n"
                "print(order_total([]))\n"
                "try:\n"
                "    order_total(items, 1.5)\n"
                "except ValueError:\n"
                "    print('ValueError')\n"
            ),
            "expected_output": "17170.0\n15453.0\n0\nValueError",
        },
    },
]

# ---------------------------------------------------------------------------
# ИНФОРМАЦИОННЫЕ СИСТЕМЫ · 09.02.07-5
# ---------------------------------------------------------------------------
IS = [
    {
        "id": "is-exam-json",
        "module": 1,
        "step": 2,
        "topic": "Экзамен",
        "title": "JSON-план экзамена",
        "level": "лёгкое",
        "language": "json",
        "task": (
            "Составь JSON-план профильного экзамена: квалификация, максимальный "
            "балл 100 и массив из шести заданий. У каждого задания есть id, "
            "title и score, а сумма score равна 100."
        ),
        "requirements": [
            "Валидный JSON",
            "Ключи qualification, max_score, tasks",
            "max_score = 100",
            "В tasks ровно 6 объектов",
            "У каждого задания id, title, score",
            "Сумма score = 100",
        ],
        "starter": (
            "{\n"
            "  \"qualification\": \"\",\n"
            "  \"max_score\": 100,\n"
            "  \"tasks\": []\n"
            "}\n"
        ),
        "hint": (
            "Шесть заданий можно оценить так: 10, 15, 20, 20, 20, 15. "
            "Проверь, что сумма действительно 100."
        ),
        "solution": (
            "{\n"
            "  \"qualification\": \"Специалист по информационным системам\",\n"
            "  \"max_score\": 100,\n"
            "  \"tasks\": [\n"
            "    {\"id\": 1, \"title\": \"ER-диаграмма\", \"score\": 10},\n"
            "    {\"id\": 2, \"title\": \"Импорт JSON\", \"score\": 15},\n"
            "    {\"id\": 3, \"title\": \"SQL-стоимость заказа\", \"score\": 20},\n"
            "    {\"id\": 4, \"title\": \"Авторизация и капча\", \"score\": 20},\n"
            "    {\"id\": 5, \"title\": \"API и Postman\", \"score\": 20},\n"
            "    {\"id\": 6, \"title\": \"Документация\", \"score\": 15}\n"
            "  ]\n"
            "}\n"
        ),
        "check": {
            "type": "json",
            "keys": ["qualification", "max_score", "tasks"],
            "list_len": {"tasks": 6},
            "sum": {"tasks[].score": 100},
            "item_keys": {"tasks": ["id", "title", "score"]},
        },
    },
    {
        "id": "is-er-orders",
        "module": 1,
        "step": 4,
        "topic": "БД",
        "title": "ER: заказы и позиции",
        "level": "сложное",
        "language": "sql",
        "task": (
            "Добавь в существующую БД таблицы sales_orders и sales_items. Заказ "
            "ссылается на customers, позиция — на заказ и products. У позиции "
            "составной ключ и CHECK на количество."
        ),
        "requirements": [
            "sales_orders с PRIMARY KEY и FK на customers",
            "sales_items с FK на sales_orders и products",
            "Составной PRIMARY KEY (order_id, product_id)",
            "quantity INTEGER CHECK (quantity > 0)",
            "Дата заказа в sales_orders",
        ],
        "starter": (
            "CREATE TABLE sales_orders (\n"
            "  order_id INTEGER PRIMARY KEY,\n"
            "  -- добавь customer_id, order_date\n"
            ");\n\n"
            "-- добавь sales_items\n"
        ),
        "hint": (
            "sales_items: order_id INTEGER NOT NULL, product_id INTEGER NOT NULL, "
            "quantity INTEGER NOT NULL CHECK (quantity > 0), "
            "PRIMARY KEY (order_id, product_id), "
            "FOREIGN KEY (order_id) REFERENCES sales_orders(order_id), "
            "FOREIGN KEY (product_id) REFERENCES products(product_id)."
        ),
        "solution": (
            "CREATE TABLE sales_orders (\n"
            "  order_id INTEGER PRIMARY KEY,\n"
            "  customer_id INTEGER NOT NULL,\n"
            "  order_date TEXT NOT NULL,\n"
            "  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)\n"
            ");\n\n"
            "CREATE TABLE sales_items (\n"
            "  order_id INTEGER NOT NULL,\n"
            "  product_id INTEGER NOT NULL,\n"
            "  quantity INTEGER NOT NULL CHECK (quantity > 0),\n"
            "  PRIMARY KEY (order_id, product_id),\n"
            "  FOREIGN KEY (order_id) REFERENCES sales_orders(order_id),\n"
            "  FOREIGN KEY (product_id) REFERENCES products(product_id)\n"
            ");\n"
        ),
        "check": {
            "type": "ddl",
            "expected": (
                "CREATE TABLE sales_orders (order_id INTEGER PRIMARY KEY, "
                "customer_id INTEGER NOT NULL, order_date TEXT NOT NULL, "
                "FOREIGN KEY (customer_id) REFERENCES customers(customer_id));\n"
                "CREATE TABLE sales_items (order_id INTEGER NOT NULL, "
                "product_id INTEGER NOT NULL, quantity INTEGER NOT NULL CHECK (quantity > 0), "
                "PRIMARY KEY (order_id, product_id), "
                "FOREIGN KEY (order_id) REFERENCES sales_orders(order_id), "
                "FOREIGN KEY (product_id) REFERENCES products(product_id));"
            ),
            "verify": (
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name LIKE 'sales_%' ORDER BY name;"
            ),
            "require": [
                {"label": "sales_orders", "pattern": r"CREATE\s+TABLE\s+sales_orders"},
                {"label": "sales_items", "pattern": r"CREATE\s+TABLE\s+sales_items"},
                {"label": "FK на customers", "pattern": r"REFERENCES\s+customers"},
                {"label": "FK на sales_orders", "pattern": r"REFERENCES\s+sales_orders"},
                {"label": "FK на products", "pattern": r"REFERENCES\s+products"},
                {"label": "составной ключ", "pattern": r"PRIMARY\s+KEY\s*\(\s*order_id\s*,\s*product_id\s*\)"},
                {"label": "CHECK количества", "pattern": r"quantity[\s\S]*CHECK\s*\(\s*quantity\s*>\s*0"},
            ],
        },
    },
    {
        "id": "is-constraints",
        "module": 1,
        "step": 6,
        "topic": "БД",
        "title": "Ограничения целостности",
        "level": "среднее",
        "language": "sql",
        "task": (
            "Создай таблицу app_users: первичный ключ, уникальный логин и e-mail, "
            "флаг блокировки только 0/1, счётчик неудачных попыток не меньше нуля, "
            "дата создания по умолчанию."
        ),
        "requirements": [
            "user_id INTEGER PRIMARY KEY",
            "login TEXT NOT NULL UNIQUE",
            "email TEXT NOT NULL UNIQUE",
            "is_blocked CHECK (is_blocked IN (0, 1))",
            "failed_attempts CHECK (failed_attempts >= 0)",
            "created_at DEFAULT CURRENT_TIMESTAMP",
        ],
        "starter": (
            "CREATE TABLE app_users (\n"
            "  user_id INTEGER PRIMARY KEY,\n"
            "  login TEXT NOT NULL,\n"
            "  -- добавь ограничения\n"
            ");\n"
        ),
        "hint": (
            "UNIQUE ставь после типа: email TEXT NOT NULL UNIQUE. Для флага — "
            "is_blocked INTEGER NOT NULL DEFAULT 0 CHECK (is_blocked IN (0, 1))."
        ),
        "solution": (
            "CREATE TABLE app_users (\n"
            "  user_id INTEGER PRIMARY KEY,\n"
            "  login TEXT NOT NULL UNIQUE,\n"
            "  email TEXT NOT NULL UNIQUE,\n"
            "  is_blocked INTEGER NOT NULL DEFAULT 0 CHECK (is_blocked IN (0, 1)),\n"
            "  failed_attempts INTEGER NOT NULL DEFAULT 0 CHECK (failed_attempts >= 0),\n"
            "  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP\n"
            ");\n"
        ),
        "check": {
            "type": "ddl",
            "expected": (
                "CREATE TABLE app_users (user_id INTEGER PRIMARY KEY, "
                "login TEXT NOT NULL UNIQUE, email TEXT NOT NULL UNIQUE, "
                "is_blocked INTEGER NOT NULL DEFAULT 0 CHECK (is_blocked IN (0, 1)), "
                "failed_attempts INTEGER NOT NULL DEFAULT 0 CHECK (failed_attempts >= 0), "
                "created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);"
            ),
            "verify": "SELECT name FROM sqlite_master WHERE type='table' AND name='app_users';",
            "require": [
                {"label": "PRIMARY KEY", "pattern": r"PRIMARY\s+KEY"},
                {"label": "UNIQUE login", "pattern": r"login\s+TEXT[^,]*UNIQUE|UNIQUE\s*\(\s*login\s*\)"},
                {"label": "UNIQUE email", "pattern": r"email\s+TEXT[^,]*UNIQUE|UNIQUE\s*\(\s*email\s*\)"},
                {"label": "CHECK is_blocked", "pattern": r"is_blocked[\s\S]*CHECK\s*\(\s*is_blocked\s+IN\s*\(\s*0\s*,\s*1\s*\)"},
                {"label": "CHECK failed_attempts", "pattern": r"failed_attempts[\s\S]*CHECK\s*\(\s*failed_attempts\s*>=\s*0"},
                {"label": "DEFAULT CURRENT_TIMESTAMP", "pattern": r"DEFAULT\s+CURRENT_TIMESTAMP"},
            ],
        },
    },
    {
        "id": "is-sql-roles",
        "module": 3,
        "step": 2,
        "topic": "ИС",
        "title": "SQL: пользователи и роли",
        "level": "среднее",
        "language": "sql",
        "task": (
            "Выведи пользователей с названием роли и признаком блокировки. "
            "Сначала заблокированные, затем по user_id."
        ),
        "requirements": [
            "JOIN roles",
            "Столбцы user_id, login, full_name, role_name, is_blocked",
            "ORDER BY is_blocked DESC, user_id",
        ],
        "starter": (
            "SELECT u.user_id, u.login, u.full_name,\n"
            "       r.role_name, u.is_blocked\n"
            "FROM users u\n"
            "-- добавь JOIN и сортировку\n"
        ),
        "hint": (
            "JOIN roles r ON r.role_id = u.role_id; ORDER BY u.is_blocked DESC, u.user_id."
        ),
        "solution": (
            "SELECT u.user_id, u.login, u.full_name, r.role_name, u.is_blocked\n"
            "FROM users u\n"
            "JOIN roles r ON r.role_id = u.role_id\n"
            "ORDER BY u.is_blocked DESC, u.user_id;"
        ),
        "check": {
            "type": "sql",
            "expected": (
                "SELECT u.user_id, u.login, u.full_name, r.role_name, u.is_blocked "
                "FROM users u JOIN roles r ON r.role_id = u.role_id "
                "ORDER BY u.is_blocked DESC, u.user_id;"
            ),
        },
    },
    {
        "id": "is-blocking",
        "module": 3,
        "step": 4,
        "topic": "ИС",
        "title": "Блокировка после трёх попыток",
        "level": "среднее",
        "language": "python",
        "task": (
            "Реализуй after_login(attempts, success): при успешном входе счётчик "
            "сбрасывается, при неудаче увеличивается; после третьей неудачи "
            "возвращается флаг блокировки."
        ),
        "requirements": [
            "Успешный вход → (0, False)",
            "Неудача увеличивает счётчик на 1",
            "Флаг True при attempts >= 3",
            "Функция возвращает кортеж (attempts, blocked)",
        ],
        "starter": (
            "def after_login(attempts: int, success: bool) -> tuple[int, bool]:\n"
            "    # обнови счётчик и флаг\n"
            "    ...\n"
        ),
        "hint": (
            "if success: return 0, False. attempts += 1; return attempts, attempts >= 3."
        ),
        "solution": (
            "def after_login(attempts: int, success: bool) -> tuple[int, bool]:\n"
            "    if success:\n"
            "        return 0, False\n"
            "    attempts += 1\n"
            "    return attempts, attempts >= 3\n"
        ),
        "check": {
            "type": "python",
            "offline_require": [
                {"label": "def after_login", "pattern": r"def\s+after_login\s*\("},
                {"label": "сброс при успехе", "pattern": r"if\s+success\s*:\s*[\s\S]*?return\s+0\s*,\s*False"},
                {"label": "увеличение счётчика", "pattern": r"attempts\s*\+=\s*1|attempts\s*=\s*attempts\s*\+\s*1"},
                {"label": "порог 3", "pattern": r"attempts\s*>=\s*3"},
                {"label": "возврат кортежа", "pattern": r"return\s+attempts\s*,"},
            ],
            "tests": (
                "print(after_login(0, False))\n"
                "print(after_login(1, False))\n"
                "print(after_login(2, False))\n"
                "print(after_login(2, True))\n"
                "print(after_login(5, False))\n"
            ),
            "expected_output": "(1, False)\n(2, False)\n(3, True)\n(0, False)\n(6, True)",
        },
    },
    {
        "id": "is-api-response",
        "module": 3,
        "step": 6,
        "topic": "API",
        "title": "JSON-ответ API",
        "level": "среднее",
        "language": "python",
        "task": (
            "Напиши api_response(items) для API заказов: верни словарь с count "
            "(количество записей) и items (исходный список). Ответ должен "
            "сериализоваться в JSON без ошибок."
        ),
        "requirements": [
            "Возврат dict, а не строки",
            "Ключ count — длина списка",
            "Ключ items — сам список",
            "json.dumps(..., ensure_ascii=False) работает",
        ],
        "starter": (
            "def api_response(items: list) -> dict:\n"
            "    # собери ответ API\n"
            "    ...\n"
        ),
        "hint": (
            "return {'count': len(items), 'items': items}. Проверка сериализации "
            "будет в тестах через json.dumps."
        ),
        "solution": (
            "def api_response(items: list) -> dict:\n"
            "    return {'count': len(items), 'items': items}\n"
        ),
        "check": {
            "type": "python",
            "offline_require": [
                {"label": "def api_response", "pattern": r"def\s+api_response\s*\("},
                {"label": "count", "pattern": r"[\"']count[\"']\s*:"},
                {"label": "len(items)", "pattern": r"len\s*\(\s*items\s*\)"},
                {"label": "items в ответе", "pattern": r"[\"']items[\"']\s*:"},
            ],
            "tests": (
                "import json\n"
                "data = [{'order_id': 1, 'status': 'Новый'}, {'order_id': 2, 'status': 'Выполнен'}]\n"
                "result = api_response(data)\n"
                "print(result['count'])\n"
                "print(result['items'] == data)\n"
                "print(json.dumps(api_response([]), ensure_ascii=False))\n"
            ),
            "expected_output": "2\nTrue\n{\"count\": 0, \"items\": []}",
        },
    },
    {
        "id": "is-postman",
        "module": 4,
        "step": 2,
        "topic": "API",
        "title": "Коллекция Postman",
        "level": "сложное",
        "language": "json",
        "task": (
            "Собери минимальную коллекцию Postman: имя, один GET-запрос к "
            "{{baseUrl}}/api/orders и тест pm.test, проверяющий статус 200 и "
            "наличие поля count."
        ),
        "requirements": [
            "Валидный JSON",
            "info.name",
            "item[0].request.method = GET",
            "URL {{baseUrl}}/api/orders",
            "Блок event с pm.test",
            "Проверки pm.response.code === 200 и json().count",
        ],
        "starter": (
            "{\n"
            "  \"info\": {\"name\": \"\"},\n"
            "  \"item\": []\n"
            "}\n"
        ),
        "hint": (
            "В item[0] положи name, request (method, url) и event: [{listen:'test', "
            "script:{exec:[\"pm.test('status 200', () => pm.response.to.have.status(200));\", "
            "\"pm.test('count', () => pm.expect(pm.response.json()).to.have.property('count'));\"]}}]."
        ),
        "solution": (
            "{\n"
            "  \"info\": {\"name\": \"Orders API\"},\n"
            "  \"item\": [\n"
            "    {\n"
            "      \"name\": \"Список заказов\",\n"
            "      \"request\": {\n"
            "        \"method\": \"GET\",\n"
            "        \"header\": [{\"key\": \"Accept\", \"value\": \"application/json\"}],\n"
            "        \"url\": \"{{baseUrl}}/api/orders\"\n"
            "      },\n"
            "      \"event\": [\n"
            "        {\n"
            "          \"listen\": \"test\",\n"
            "          \"script\": {\n"
            "            \"exec\": [\n"
            "              \"pm.test('status 200', () => pm.response.to.have.status(200));\",\n"
            "              \"pm.test('count', () => pm.expect(pm.response.json()).to.have.property('count'));\"\n"
            "            ]\n"
            "          }\n"
            "        }\n"
            "      ]\n"
            "    }\n"
            "  ]\n"
            "}\n"
        ),
        "check": {
            "type": "json",
            "keys": ["info", "item"],
            "list_len": {"item": 1},
            "require": [
                {"label": "GET-запрос", "pattern": r"\"method\"\s*:\s*\"GET\""},
                {"label": "URL с baseUrl", "pattern": r"\{\{baseUrl\}\}/api/orders"},
                {"label": "pm.test", "pattern": r"pm\.test\s*\("},
                {"label": "статус 200", "pattern": r"status\s*\(\s*200\s*\)|code\s*===?\s*200"},
                {"label": "поле count", "pattern": r"property\(\s*['\"]count|\.count"},
            ],
        },
    },
    {
        "id": "is-docs",
        "module": 4,
        "step": 4,
        "topic": "Документы",
        "title": "Документация API",
        "level": "среднее",
        "language": "text",
        "task": (
            "Опиши endpoint GET /api/orders в Markdown: назначение, параметры "
            "запроса, успешный ответ 200 с примером JSON, ошибки 400 и 401."
        ),
        "requirements": [
            "Заголовок документа",
            "Метод и URL GET /api/orders",
            "Раздел параметров",
            "Пример JSON-ответа",
            "Коды 200, 400, 401",
        ],
        "starter": "# API заказов\n\n## GET /api/orders\n\n",
        "hint": (
            "Структура: назначение → параметры (limit, offset) → пример ответа "
            "в ```json``` → таблица ошибок 400/401."
        ),
        "solution": (
            "# API заказов\n\n"
            "## GET /api/orders\n\n"
            "Возвращает список заказов.\n\n"
            "### Параметры\n\n"
            "| Имя | Тип | Обязательный | Описание |\n"
            "|---|---|---|---|\n"
            "| limit | int | нет | Размер страницы |\n"
            "| offset | int | нет | Смещение |\n\n"
            "### Ответ 200\n\n"
            "```json\n"
            "{\"count\": 2, \"items\": [{\"order_id\": 1, \"status\": \"Новый\"}]}\n"
            "```\n\n"
            "### Ошибки\n\n"
            "- 400 — неверные параметры.\n"
            "- 401 — пользователь не авторизован.\n"
        ),
        "check": {
            "type": "patterns",
            "require": [
                {"label": "заголовок Markdown", "pattern": r"^#\s+\S"},
                {"label": "GET /api/orders", "pattern": r"GET\s+/api/orders"},
                {"label": "раздел параметров", "pattern": r"параметр"},
                {"label": "JSON-пример", "pattern": r"```json[\s\S]*\{"},
                {"label": "код 200", "pattern": r"\b200\b"},
                {"label": "код 400", "pattern": r"\b400\b"},
                {"label": "код 401", "pattern": r"\b401\b"},
            ],
        },
    },
    {
        "id": "is-final-order",
        "module": 4,
        "step": 9,
        "topic": "API",
        "title": "Итог: создание заказа",
        "level": "сложное",
        "language": "python",
        "task": (
            "Реализуй create_order(conn, customer_id, items): вставь заказ, затем "
            "все позиции, зафиксируй транзакцию и верни order_id. Позиции — "
            "список словарей с product_id и quantity."
        ),
        "requirements": [
            "INSERT INTO orders",
            "lastrowid как order_id",
            "Цикл по items с INSERT INTO order_items",
            "Параметризованные запросы",
            "conn.commit()",
            "Возврат order_id",
        ],
        "starter": (
            "def create_order(conn, customer_id: int, items: list) -> int:\n"
            "    # создай заказ и позиции\n"
            "    ...\n"
        ),
        "hint": (
            "cur = conn.execute('INSERT INTO orders (customer_id, status) VALUES (?, ?)', "
            "(customer_id, 'Новый')); order_id = cur.lastrowid; затем цикл по items "
            "с INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)."
        ),
        "solution": (
            "def create_order(conn, customer_id: int, items: list) -> int:\n"
            "    cur = conn.execute(\n"
            "        'INSERT INTO orders (customer_id, status) VALUES (?, ?)',\n"
            "        (customer_id, 'Новый'),\n"
            "    )\n"
            "    order_id = cur.lastrowid\n"
            "    for item in items:\n"
            "        conn.execute(\n"
            "            'INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)',\n"
            "            (order_id, item['product_id'], item['quantity']),\n"
            "        )\n"
            "    conn.commit()\n"
            "    return order_id\n"
        ),
        "check": {
            "type": "python",
            "offline_require": [
                {"label": "def create_order", "pattern": r"def\s+create_order\s*\("},
                {"label": "INSERT INTO orders", "pattern": r"INSERT\s+INTO\s+orders"},
                {"label": "lastrowid", "pattern": r"lastrowid"},
                {"label": "INSERT INTO order_items", "pattern": r"INSERT\s+INTO\s+order_items"},
                {"label": "цикл по items", "pattern": r"for\s+\w+\s+in\s+items"},
                {"label": "commit", "pattern": r"\.commit\s*\(\s*\)"},
                {"label": "возврат order_id", "pattern": r"return\s+order_id"},
            ],
            "tests": (
                "import sqlite3\n"
                "con = sqlite3.connect(':memory:')\n"
                "con.execute('CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, status TEXT)')\n"
                "con.execute('CREATE TABLE order_items (order_id INTEGER, product_id INTEGER, quantity INTEGER)')\n"
                "order_id = create_order(con, 7, [{'product_id': 1, 'quantity': 2}, {'product_id': 3, 'quantity': 1}])\n"
                "print(order_id)\n"
                "print(con.execute('SELECT customer_id, status FROM orders').fetchall())\n"
                "print(con.execute('SELECT order_id, product_id, quantity FROM order_items ORDER BY product_id').fetchall())\n"
            ),
            "expected_output": (
                "1\n"
                "[(7, 'Новый')]\n"
                "[(1, 1, 2), (1, 3, 1)]"
            ),
        },
    },
    {
        "id": "is-auth-login",
        "module": 3,
        "step": 2,
        "topic": "ИС",
        "title": "Вход с ролями и блокировкой",
        "level": "сложное",
        "language": "python",
        "task": (
            "Реализуй login(conn, login, password) для экзаменационного модуля: "
            "найди пользователя, проверь блокировку и пароль. При успехе сбрось "
            "счётчик ошибок и верни роль, при ошибке увеличь счётчик, а после "
            "третьей неудачи заблокируй учётную запись."
        ),
        "requirements": [
            "Поиск пользователя по login",
            "Заблокированный пользователь → ('blocked', None)",
            "Неверный пароль → ('error', None) и failed_attempts += 1",
            "Третья ошибка ставит is_blocked = 1",
            "Успех → ('ok', role_name) и сброс счётчика",
            "commit после изменений",
        ],
        "starter": (
            "def login(conn, login: str, password: str):\n"
            "    # верни ('ok', роль), ('error', None) или ('blocked', None)\n"
            "    ...\n"
        ),
        "hint": (
            "Выбери password, is_blocked, failed_attempts, role_name из users "
            "WHERE login = ?. Если строки нет — ('error', None). Если is_blocked — "
            "('blocked', None). После третьей ошибки выполни UPDATE ... SET is_blocked = 1."
        ),
        "solution": (
            "def login(conn, login: str, password: str):\n"
            "    row = conn.execute(\n"
            "        'SELECT password, is_blocked, failed_attempts, role_name '\n"
            "        'FROM users WHERE login = ?',\n"
            "        (login,),\n"
            "    ).fetchone()\n"
            "    if row is None:\n"
            "        return 'error', None\n"
            "    stored, blocked, attempts, role = row\n"
            "    if blocked:\n"
            "        return 'blocked', None\n"
            "    if stored == password:\n"
            "        conn.execute(\n"
            "            'UPDATE users SET failed_attempts = 0 WHERE login = ?',\n"
            "            (login,),\n"
            "        )\n"
            "        conn.commit()\n"
            "        return 'ok', role\n"
            "    attempts += 1\n"
            "    now_blocked = attempts >= 3\n"
            "    conn.execute(\n"
            "        'UPDATE users SET failed_attempts = ?, is_blocked = ? WHERE login = ?',\n"
            "        (attempts, int(now_blocked), login),\n"
            "    )\n"
            "    conn.commit()\n"
            "    return ('blocked' if now_blocked else 'error'), None\n"
        ),
        "check": {
            "type": "python",
            "offline_require": [
                {"label": "def login", "pattern": r"def\s+login\s*\("},
                {"label": "SELECT из users", "pattern": r"SELECT[\s\S]*FROM\s+users"},
                {"label": "проверка блокировки", "pattern": r"is_blocked"},
                {"label": "счётчик ошибок", "pattern": r"failed_attempts"},
                {"label": "порог 3", "pattern": r">=\s*3"},
                {"label": "UPDATE и commit", "pattern": r"UPDATE\s+users[\s\S]*commit\s*\("},
                {"label": "возврат роли", "pattern": r"return\s+[\"']ok[\"']"},
            ],
            "tests": (
                "import sqlite3\n"
                "con = sqlite3.connect(':memory:')\n"
                "con.execute('CREATE TABLE users (login TEXT PRIMARY KEY, password TEXT, role_name TEXT, is_blocked INTEGER, failed_attempts INTEGER)')\n"
                "con.execute(\"INSERT INTO users VALUES ('admin', 'admin123', 'Администратор', 0, 0)\")\n"
                "con.execute(\"INSERT INTO users VALUES ('user1', 'user123', 'Пользователь', 1, 3)\")\n"
                "print(login(con, 'admin', 'admin123'))\n"
                "print(login(con, 'admin', 'wrong'))\n"
                "print(login(con, 'admin', 'wrong'))\n"
                "print(login(con, 'admin', 'wrong'))\n"
                "print(login(con, 'admin', 'admin123'))\n"
                "print(login(con, 'user1', 'user123'))\n"
                "print(login(con, 'nobody', 'x'))\n"
            ),
            "expected_output": (
                "('ok', 'Администратор')\n"
                "('error', None)\n"
                "('error', None)\n"
                "('blocked', None)\n"
                "('blocked', None)\n"
                "('blocked', None)\n"
                "('error', None)"
            ),
        },
    },
    {
        "id": "is-captcha-puzzle",
        "module": 3,
        "step": 4,
        "topic": "ИС",
        "title": "Капча-пазл и попытки",
        "level": "среднее",
        "language": "python",
        "task": (
            "Реализуй проверку капчи-пазла: puzzle_solved(user_order, correct_order) "
            "сравнивает последовательность фрагментов, а captcha_attempt(attempts, solved) "
            "сбрасывает счётчик при успехе и блокирует после трёх неудач."
        ),
        "requirements": [
            "puzzle_solved сравнивает порядок фрагментов",
            "Успешная сборка → (0, True)",
            "Неудача увеличивает счётчик",
            "Флаг блокировки при attempts >= 3",
            "Возврат кортежа (attempts, allowed)",
        ],
        "starter": (
            "def puzzle_solved(user_order, correct_order) -> bool:\n"
            "    # сравни последовательности\n"
            "    ...\n\n"
            "def captcha_attempt(attempts: int, solved: bool):\n"
            "    # верни (новое число попыток, доступ разрешён)\n"
            "    ...\n"
        ),
        "hint": (
            "list(user_order) == list(correct_order). В captcha_attempt: "
            "if solved: return 0, True; затем attempts += 1; return attempts, attempts < 3."
        ),
        "solution": (
            "def puzzle_solved(user_order, correct_order) -> bool:\n"
            "    return list(user_order) == list(correct_order)\n\n"
            "def captcha_attempt(attempts: int, solved: bool):\n"
            "    if solved:\n"
            "        return 0, True\n"
            "    attempts += 1\n"
            "    return attempts, attempts < 3\n"
        ),
        "check": {
            "type": "python",
            "offline_require": [
                {"label": "def puzzle_solved", "pattern": r"def\s+puzzle_solved\s*\("},
                {"label": "сравнение последовательностей", "pattern": r"list\s*\(\s*user_order\s*\)\s*==\s*list\s*\(\s*correct_order\s*\)"},
                {"label": "def captcha_attempt", "pattern": r"def\s+captcha_attempt\s*\("},
                {"label": "сброс при успехе", "pattern": r"if\s+solved\s*:\s*[\s\S]*?return\s+0\s*,\s*True"},
                {"label": "увеличение попыток", "pattern": r"attempts\s*\+=\s*1"},
                {"label": "порог 3", "pattern": r"attempts\s*<\s*3|attempts\s*>=\s*3"},
            ],
            "tests": (
                "print(puzzle_solved([1, 2, 3, 4], [1, 2, 3, 4]))\n"
                "print(puzzle_solved([1, 2, 4, 3], [1, 2, 3, 4]))\n"
                "print(captcha_attempt(0, True))\n"
                "print(captcha_attempt(0, False))\n"
                "print(captcha_attempt(2, False))\n"
                "print(captcha_attempt(5, False))\n"
            ),
            "expected_output": "True\nFalse\n(0, True)\n(1, True)\n(3, False)\n(6, False)",
        },
    },
    {
        "id": "is-api-mask",
        "module": 3,
        "step": 6,
        "topic": "API",
        "title": "Маскирование персональных данных",
        "level": "сложное",
        "language": "python",
        "task": (
            "Перед отдачей API нельзя показывать персональные данные в исходном "
            "виде. Реализуй mask_phone, mask_email и mask_inn по образцу: "
            "+7(495)***-**-11, i***@mebelplus.ru, ***4567."
        ),
        "requirements": [
            "mask_phone сохраняет код +7(495) и последние 2 цифры",
            "mask_email оставляет первую букву и домен",
            "mask_inn оставляет последние 4 цифры",
            "Некорректные значения не должны ронять программу",
        ],
        "starter": (
            "import re\n\n"
            "def mask_phone(phone: str) -> str:\n"
            "    # +7(495)111-11-11 → +7(495)***-**-11\n"
            "    ...\n\n"
            "def mask_email(email: str) -> str:\n"
            "    # info@mebelplus.ru → i***@mebelplus.ru\n"
            "    ...\n\n"
            "def mask_inn(inn: str) -> str:\n"
            "    # 7701234567 → ***4567\n"
            "    ...\n"
        ),
        "hint": (
            "Для телефона удобно выражение r'(\\+7\\(\\d{3}\\))\\d{3}-\\d{2}-(\\d{2})'. "
            "Для email: local, domain = email.split('@', 1); local[0] + '***@' + domain. "
            "Для ИНН: '***' + inn[-4:]."
        ),
        "solution": (
            "import re\n\n"
            "def mask_phone(phone: str) -> str:\n"
            "    match = re.match(r'(\\+7\\(\\d{3}\\))\\d{3}-\\d{2}-(\\d{2})', phone)\n"
            "    if not match:\n"
            "        return phone\n"
            "    return f'{match.group(1)}***-**-{match.group(2)}'\n\n"
            "def mask_email(email: str) -> str:\n"
            "    if '@' not in email or not email.split('@', 1)[0]:\n"
            "        return email\n"
            "    local, domain = email.split('@', 1)\n"
            "    return f'{local[0]}***@{domain}'\n\n"
            "def mask_inn(inn: str) -> str:\n"
            "    return '***' + inn[-4:] if inn else inn\n"
        ),
        "check": {
            "type": "python",
            "offline_require": [
                {"label": "def mask_phone", "pattern": r"def\s+mask_phone\s*\("},
                {"label": "def mask_email", "pattern": r"def\s+mask_email\s*\("},
                {"label": "def mask_inn", "pattern": r"def\s+mask_inn\s*\("},
                {"label": "маска телефона ***", "pattern": r"\*\*\*-\*\*-"},
                {"label": "домен email", "pattern": r"@\{?domain|@.*domain|split\s*\(\s*[\"']@[\"']"},
                {"label": "последние 4 цифры ИНН", "pattern": r"\[-4:\]"},
            ],
            "tests": (
                "print(mask_phone('+7(495)111-11-11'))\n"
                "print(mask_phone('+7(812)222-22-22'))\n"
                "print(mask_email('info@mebelplus.ru'))\n"
                "print(mask_email('smirnov@mail.ru'))\n"
                "print(mask_inn('7701234567'))\n"
            ),
            "expected_output": (
                "+7(495)***-**-11\n"
                "+7(812)***-**-22\n"
                "i***@mebelplus.ru\n"
                "s***@mail.ru\n"
                "***4567"
            ),
        },
    },
    {
        "id": "is-postman-tests",
        "module": 4,
        "step": 2,
        "topic": "API",
        "title": "Postman: коллекция с негативными тестами",
        "level": "сложное",
        "language": "json",
        "task": (
            "Собери коллекцию Postman из трёх запросов: список заказчиков, "
            "карточка заказчика и несуществующий id. Добавь тесты на 200, JSON, "
            "маскирование телефона и 404."
        ),
        "requirements": [
            "Валидный JSON коллекции",
            "Три GET-запроса: /api/customers, /1, /999",
            "Тест статуса 200 и JSON",
            "Проверка маски *** в теле телефона",
            "Тест 404 для несуществующего id",
        ],
        "starter": (
            "{\n"
            "  \"info\": {\"name\": \"IS API\"},\n"
            "  \"item\": []\n"
            "}\n"
        ),
        "hint": (
            "В item положи три объекта. В event.listen='test' используй "
            "pm.test('status 200', () => pm.response.to.have.status(200)); "
            "pm.test('masked', () => pm.expect(pm.response.json()[0].phone).to.include('***')); "
            "и отдельный тест status 404 для /api/customers/999."
        ),
        "solution": (
            "{\n"
            "  \"info\": {\"name\": \"IS API customers\"},\n"
            "  \"item\": [\n"
            "    {\n"
            "      \"name\": \"Список заказчиков\",\n"
            "      \"request\": {\"method\": \"GET\", \"url\": \"{{baseUrl}}/api/customers\"},\n"
            "      \"event\": [{\"listen\": \"test\", \"script\": {\"exec\": [\n"
            "        \"pm.test('status 200', () => pm.response.to.have.status(200));\",\n"
            "        \"pm.test('JSON', () => pm.response.to.be.json);\",\n"
            "        \"pm.test('masked phone', () => pm.expect(pm.response.json()[0].phone).to.include('***'));\"\n"
            "      ]}}]\n"
            "    },\n"
            "    {\n"
            "      \"name\": \"Заказчик 1\",\n"
            "      \"request\": {\"method\": \"GET\", \"url\": \"{{baseUrl}}/api/customers/1\"},\n"
            "      \"event\": [{\"listen\": \"test\", \"script\": {\"exec\": [\n"
            "        \"pm.test('status 200', () => pm.response.to.have.status(200));\"\n"
            "      ]}}]\n"
            "    },\n"
            "    {\n"
            "      \"name\": \"Несуществующий заказчик\",\n"
            "      \"request\": {\"method\": \"GET\", \"url\": \"{{baseUrl}}/api/customers/999\"},\n"
            "      \"event\": [{\"listen\": \"test\", \"script\": {\"exec\": [\n"
            "        \"pm.test('status 404', () => pm.response.to.have.status(404));\"\n"
            "      ]}}]\n"
            "    }\n"
            "  ]\n"
            "}\n"
        ),
        "check": {
            "type": "json",
            "keys": ["info", "item"],
            "list_len": {"item": 3},
            "require": [
                {"label": "три GET-запроса", "pattern": r"\"method\"\s*:\s*\"GET\""},
                {"label": "URL списка", "pattern": r"/api/customers(?![0-9/])"},
                {"label": "URL заказчика 1", "pattern": r"/api/customers/1\b"},
                {"label": "URL 999", "pattern": r"/api/customers/999"},
                {"label": "pm.test", "pattern": r"pm\.test\s*\("},
                {"label": "статус 200", "pattern": r"status\s*\(\s*200\s*\)"},
                {"label": "статус 404", "pattern": r"status\s*\(\s*404\s*\)"},
                {"label": "проверка маски", "pattern": r"include\(\s*['\"]\*\*\*"},
                {"label": "JSON-ответ", "pattern": r"to\.be\.json|response\.json\("},
            ],
        },
    },
    {
        "id": "is-testcases",
        "module": 4,
        "step": 4,
        "topic": "Документы",
        "title": "Тест-кейсы для приёмки",
        "level": "среднее",
        "language": "text",
        "task": (
            "Оформи тест-кейсы для сдачи экзаменационного проекта: вход, "
            "капча, блокировка после трёх ошибок, API 200 с маскированием, "
            "API 404 и создание заказа. Укажи действие, ожидаемый и фактический "
            "результат, статус."
        ),
        "requirements": [
            "Заголовок и таблица тест-кейсов",
            "Колонки: действие, ожидаемый результат, фактический результат, статус",
            "Минимум 6 сценариев",
            "Есть вход, капча и блокировка",
            "Есть API 200 и 404",
            "Есть создание заказа",
        ],
        "starter": "# Тест-кейсы\n\n| № | Действие | Ожидаемый результат | Фактический результат | Статус |\n|---|---|---|---|---|\n",
        "hint": (
            "Для каждого сценария опиши конкретное действие: «Ввести неверный пароль "
            "3 раза», «Открыть GET /api/customers/999». В фактическом результате "
            "напиши «Совпадает» или «Пройден»."
        ),
        "solution": (
            "# Тест-кейсы\n\n"
            "| № | Действие | Ожидаемый результат | Фактический результат | Статус |\n"
            "|---|---|---|---|---|\n"
            "| 1 | Ввести верный логин и пароль | Открывается главная страница, роль сохранена | Совпадает | Пройден |\n"
            "| 2 | Собрать капчу-пазл верно | Доступ к форме входа разрешён | Совпадает | Пройден |\n"
            "| 3 | Ввести неверный пароль 3 раза | Учётная запись заблокирована | Совпадает | Пройден |\n"
            "| 4 | GET /api/customers | 200, телефон и email замаскированы | Совпадает | Пройден |\n"
            "| 5 | GET /api/customers/999 | 404 и JSON с ошибкой | Совпадает | Пройден |\n"
            "| 6 | Создать заказ с двумя позициями | Заказ и позиции сохранены в БД | Совпадает | Пройден |\n"
        ),
        "check": {
            "type": "patterns",
            "require": [
                {"label": "заголовок", "pattern": r"^#\s+\S"},
                {"label": "колонка «Действие»", "pattern": r"Действие"},
                {"label": "колонка «Ожидаемый результат»", "pattern": r"Ожидаемый\s+результат"},
                {"label": "колонка «Фактический результат»", "pattern": r"Фактический\s+результат"},
                {"label": "колонка «Статус»", "pattern": r"Статус"},
                {"label": "вход", "pattern": r"логин|вход|пароль"},
                {"label": "капча", "pattern": r"капч"},
                {"label": "блокировка", "pattern": r"блокир"},
                {"label": "API 200", "pattern": r"\b200\b"},
                {"label": "API 404", "pattern": r"\b404\b"},
                {"label": "создание заказа", "pattern": r"заказ"},
            ],
        },
    },
    {
        "id": "is-import-json",
        "module": 4,
        "step": 9,
        "topic": "API",
        "title": "Импорт заказчиков из JSON",
        "level": "сложное",
        "language": "python",
        "task": (
            "Реализуй import_customers(conn, data): загрузи список заказчиков "
            "из JSON в SQLite. Повторяющийся ИНН пропускай через INSERT OR IGNORE, "
            "фиксируй транзакцию и верни число добавленных записей."
        ),
        "requirements": [
            "Цикл по списку словарей",
            "INSERT OR IGNORE INTO customers",
            "Параметризованный запрос с 5 полями",
            "conn.commit()",
            "Возврат количества вставленных строк",
        ],
        "starter": (
            "def import_customers(conn, data: list) -> int:\n"
            "    # вставь заказчиков и верни количество\n"
            "    ...\n"
        ),
        "hint": (
            "cur = conn.execute('INSERT OR IGNORE INTO customers "
            "(name, inn, address, phone, email) VALUES (?, ?, ?, ?, ?)', (...)); "
            "добавляй cur.rowcount к счётчику. В конце commit и return."
        ),
        "solution": (
            "def import_customers(conn, data: list) -> int:\n"
            "    inserted = 0\n"
            "    for item in data:\n"
            "        cur = conn.execute(\n"
            "            'INSERT OR IGNORE INTO customers '\n"
            "            '(name, inn, address, phone, email) VALUES (?, ?, ?, ?, ?)',\n"
            "            (item['name'], item['inn'], item['address'],\n"
            "             item['phone'], item['email']),\n"
            "        )\n"
            "        inserted += cur.rowcount\n"
            "    conn.commit()\n"
            "    return inserted\n"
        ),
        "check": {
            "type": "python",
            "offline_require": [
                {"label": "def import_customers", "pattern": r"def\s+import_customers\s*\("},
                {"label": "INSERT OR IGNORE", "pattern": r"INSERT\s+OR\s+IGNORE\s+INTO\s+customers"},
                {"label": "5 параметров", "pattern": r"VALUES\s*\(\s*\?[\s\S]*\?[\s\S]*\?[\s\S]*\?[\s\S]*\?"},
                {"label": "цикл по data", "pattern": r"for\s+\w+\s+in\s+data"},
                {"label": "rowcount", "pattern": r"rowcount"},
                {"label": "commit", "pattern": r"\.commit\s*\(\s*\)"},
                {"label": "возврат счётчика", "pattern": r"return\s+inserted"},
            ],
            "tests": (
                "import sqlite3\n"
                "con = sqlite3.connect(':memory:')\n"
                "con.execute('CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, name TEXT, inn TEXT UNIQUE, address TEXT, phone TEXT, email TEXT)')\n"
                "data = [\n"
                "    {'name': 'ООО «Мебель Плюс»', 'inn': '7701234567', 'address': 'Москва', 'phone': '+7(495)111-11-11', 'email': 'info@mebelplus.ru'},\n"
                "    {'name': 'ИП Смирнов', 'inn': '770234567890', 'address': 'СПб', 'phone': '+7(812)222-22-22', 'email': 'smirnov@mail.ru'},\n"
                "    {'name': 'Дубль', 'inn': '7701234567', 'address': 'Москва', 'phone': '+7(495)000-00-00', 'email': 'dup@mail.ru'},\n"
                "]\n"
                "print(import_customers(con, data))\n"
                "print(con.execute('SELECT COUNT(*) FROM customers').fetchone()[0])\n"
            ),
            "expected_output": "2\n2",
        },
    },
]

COURSES = {
    "web": WEB,
    "programmer": PROGRAMMER,
    "is": IS,
}


def all_for(course: str) -> list[dict]:
    """Все задания курса."""
    return COURSES.get(course, [])


def for_step(course: str, module_no: int, step_no: int) -> list[dict]:
    """Задания, привязанные к конкретному шагу теста."""
    return [
        task for task in all_for(course)
        if task["module"] == module_no and task["step"] == step_no
    ]


def for_topic(course: str, topic: str) -> list[dict]:
    """Задания по теме вопроса (для тренажёра и офлайн-сайта)."""
    tasks = [task for task in all_for(course) if task["topic"] == topic]
    return tasks or all_for(course)


def by_id(course: str, task_id: str) -> dict | None:
    return next((task for task in all_for(course) if task["id"] == task_id), None)


def summary() -> dict[str, int]:
    return {course: len(tasks) for course, tasks in COURSES.items()}
