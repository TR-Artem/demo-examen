# -*- coding: utf-8 -*-
"""
Содержание курса под ДЭ-2027, квалификация
«Разработчик веб и мультимедийных приложений» (09.02.07-3-2027).

База: КОД 09.02.07-3-2026 (последний завершённый экзамен), профильный уровень:
3 модуля, 75 баллов инвариант + 25 баллов вариативная часть, 4 часа.
Предметная область: портал онлайн-курсов «Корочки.есть».
Стек: Python + Flask + SQLite + HTML/CSS/JavaScript.

Файл подключается в конце trainer.py и заменяет данные старой версии
для квалификации «Программист».
"""
from __future__ import annotations

MAX_SCORE = 100
COURSE_ID = "web"
COURSE_TITLE = "Веб и мультимедиа (09.02.07-3)"
COURSE_SUBTITLE = "Flask + SQLite + HTML/CSS/JS · 3 модуля"
EXAM_TITLE = ("ДЭ 09.02.07-3-2027 «Разработчик веб и мультимедийных "
              "приложений» · профильный уровень")

# ---------------------------------------------------------------------------
# 1. БАЗА ДАННЫХ: 6 таблиц портала «Корочки.есть»
# ---------------------------------------------------------------------------
SCHEMA_SQL = """
CREATE TABLE roles (
    role_id   INTEGER PRIMARY KEY,
    role_name TEXT NOT NULL UNIQUE
);

CREATE TABLE users (
    user_id       INTEGER PRIMARY KEY,
    login         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    full_name     TEXT NOT NULL,
    phone         TEXT NOT NULL,
    email         TEXT NOT NULL UNIQUE,
    role_id       INTEGER NOT NULL REFERENCES roles(role_id),
    created_at    TEXT NOT NULL DEFAULT (date('now'))
);

CREATE TABLE courses (
    course_id      INTEGER PRIMARY KEY,
    title          TEXT NOT NULL UNIQUE,
    description    TEXT,
    duration_hours INTEGER NOT NULL CHECK (duration_hours > 0),
    price          REAL NOT NULL CHECK (price >= 0)
);

CREATE TABLE application_statuses (
    status_id   INTEGER PRIMARY KEY,
    status_name TEXT NOT NULL UNIQUE
);

CREATE TABLE applications (
    application_id INTEGER PRIMARY KEY,
    user_id        INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    course_id      INTEGER NOT NULL REFERENCES courses(course_id) ON DELETE RESTRICT,
    start_date     TEXT NOT NULL,
    payment_method TEXT NOT NULL CHECK (payment_method IN ('cash', 'phone_transfer')),
    status_id      INTEGER NOT NULL REFERENCES application_statuses(status_id),
    cancel_reason  TEXT,
    created_at     TEXT NOT NULL DEFAULT (date('now'))
);

CREATE TABLE reviews (
    review_id      INTEGER PRIMARY KEY,
    application_id INTEGER NOT NULL UNIQUE
                   REFERENCES applications(application_id) ON DELETE CASCADE,
    user_id        INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    rating         INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review_text    TEXT,
    created_at     TEXT NOT NULL DEFAULT (date('now'))
);

CREATE INDEX idx_applications_user   ON applications(user_id);
CREATE INDEX idx_applications_course ON applications(course_id);
CREATE INDEX idx_applications_status ON applications(status_id);
CREATE INDEX idx_reviews_rating      ON reviews(rating);

INSERT INTO roles (role_id, role_name) VALUES
    (1, 'Администратор'),
    (2, 'Пользователь');

INSERT INTO users
    (user_id, login, password_hash, full_name, phone, email, role_id, created_at)
VALUES
    (1, 'Admin', 'hash_admin_demo', 'Администратор портала',
     '8(900)000-00-00', 'admin@korochki.ru', 1, date('now', '-200 days')),
    (2, 'ivanov01', 'hash_demo_2', 'Иванов Иван Иванович',
     '8(921)111-11-11', 'ivanov@example.ru', 2, date('now', '-180 days')),
    (3, 'petrova02', 'hash_demo_3', 'Петрова Анна Сергеевна',
     '8(921)222-22-22', 'petrova@example.ru', 2, date('now', '-170 days')),
    (4, 'sidorov03', 'hash_demo_4', 'Сидоров Пётр Алексеевич',
     '8(812)333-33-33', 'sidorov@example.ru', 2, date('now', '-160 days')),
    (5, 'kuznetsova04', 'hash_demo_5', 'Кузнецова Мария Андреевна',
     '8(921)444-44-44', 'kuznetsova@example.ru', 2, date('now', '-150 days')),
    (6, 'smirnov05', 'hash_demo_6', 'Смирнов Алексей Дмитриевич',
     '8(812)555-55-55', 'smirnov@example.ru', 2, date('now', '-140 days')),
    (7, 'popova06', 'hash_demo_7', 'Попова Ольга Игоревна',
     '8(921)666-66-66', 'popova@example.ru', 2, date('now', '-130 days')),
    (8, 'morozov07', 'hash_demo_8', 'Морозов Кирилл Олегович',
     '8(812)777-77-77', 'morozov@example.ru', 2, date('now', '-120 days'));

INSERT INTO courses (course_id, title, description, duration_hours, price) VALUES
    (1, 'Основы алгоритмизации и программирования',
     'Логика, блок-схемы, базовые конструкции и первые программы.', 72, 12000),
    (2, 'Основы веб-дизайна',
     'Композиция, цвет, типографика, макеты и адаптивные интерфейсы.', 48, 9000),
    (3, 'Основы проектирования баз данных',
     'Модели данных, нормализация, ER-диаграммы, SQL и ограничения.', 64, 11000),
    (4, 'Python для анализа данных',
     'Структуры данных, файлы, pandas, визуализация и отчёты.', 80, 15000),
    (5, 'UX/UI-дизайн мобильных приложений',
     'Исследование, прототипы, мобильные паттерны и дизайн-система.', 40, 8000),
    (6, 'Основы кибербезопасности',
     'Пароли, шифрование, веб-уязвимости и базовая защита приложений.', 56, 10000),
    (7, 'Основы работы с графикой',
     'Растровая и векторная графика, подготовка изображений для веба.', 32, 7000);

INSERT INTO application_statuses (status_id, status_name) VALUES
    (1, 'Новая'),
    (2, 'Идет обучение'),
    (3, 'Обучение завершено'),
    (4, 'Отменена');

INSERT INTO applications
    (application_id, user_id, course_id, start_date, payment_method,
     status_id, cancel_reason, created_at)
VALUES
    (1, 2, 1, date('now', '+14 days'), 'cash', 1, NULL, date('now', '-75 days')),
    (2, 3, 2, date('now', '+7 days'),  'phone_transfer', 2, NULL, date('now', '-70 days')),
    (3, 4, 3, date('now', '-20 days'), 'cash', 3, NULL, date('now', '-45 days')),
    (4, 5, 1, date('now', '-60 days'), 'phone_transfer', 3, NULL, date('now', '-40 days')),
    (5, 6, 4, date('now', '-10 days'), 'cash', 4, 'Не подошло расписание', date('now', '-20 days')),
    (6, 7, 5, date('now', '+21 days'), 'cash', 1, NULL, date('now', '-15 days')),
    (7, 8, 2, date('now', '-5 days'),  'cash', 3, NULL, date('now', '-10 days')),
    (8, 2, 3, date('now', '+3 days'),  'phone_transfer', 2, NULL, date('now', '-5 days')),
    (9, 3, 6, date('now', '-30 days'), 'phone_transfer', 3, NULL, date('now', '-2 days')),
    (10, 4, 4, date('now', '+30 days'), 'cash', 1, NULL, date('now')),
    (11, 5, 5, date('now', '-45 days'), 'cash', 4, 'Нет свободных мест', date('now', '-50 days')),
    (12, 6, 6, date('now', '-15 days'), 'cash', 3, NULL, date('now', '-25 days')),
    (13, 7, 1, date('now', '+10 days'), 'phone_transfer', 2, NULL, date('now', '-35 days')),
    (14, 8, 3, date('now', '-2 days'),  'cash', 1, NULL, date('now', '-12 days'));

INSERT INTO reviews
    (review_id, application_id, user_id, rating, review_text, created_at)
VALUES
    (1, 3, 4, 5, 'Отличный курс, много практики по проектированию БД.', date('now', '-15 days')),
    (2, 4, 5, 4, 'Понятно объясняют алгоритмы, но мало домашних заданий.', date('now', '-20 days')),
    (3, 7, 8, 5, 'Веб-дизайн — лучший курс, сразу применил на проекте.', date('now', '-3 days')),
    (4, 9, 3, 3, 'Материал полезный, однако темп слишком быстрый.', date('now', '-1 days')),
    (5, 12, 6, 4, 'Хорошее введение в безопасность, пригодилось на работе.', date('now', '-8 days'));
"""

# ---------------------------------------------------------------------------
# 2. ПЛАН НА 12 НЕДЕЛЬ (60 занятий, 60–120 минут)
# ---------------------------------------------------------------------------
WEEKS = [
    ("Неделя 1. Как устроен веб и HTML", [
        ("Клиент, сервер, HTTP", "URL, запрос/ответ, методы GET/POST, коды 200/302/404/500, DevTools → Network.", 60),
        ("Каркас HTML-документа", "DOCTYPE, html/head/body, meta charset, viewport, title, подключение CSS/JS.", 60),
        ("Семантика и контент", "header/nav/main/section/footer, заголовки h1–h3, списки, ссылки, изображения и alt.", 70),
        ("Формы", "form, label, input, select, textarea, button, required, type=email/date/tel, autocomplete.", 80),
        ("Мини-страница портала", "Собери статическую страницу «Корочки.есть»: шапка, курсы, форма заявки.", 90),
    ]),
    ("Неделя 2. CSS и адаптивная вёрстка", [
        ("Селекторы и каскад", "Классы, id, псевдоклассы, специфичность, наследование, CSS-переменные.", 70),
        ("Box model и типографика", "margin/padding/border, box-sizing, размеры, шрифты, межстрочный интервал.", 70),
        ("Flexbox", "display:flex, направление, выравнивание, gap, перенос, шапка и карточки.", 80),
        ("Grid и компоненты", "grid-template-columns, auto-fit/minmax, карточки курсов, кнопки, поля.", 80),
        ("Адаптив 390×844", "Mobile-first, media queries, мобильная навигация, проверка в DevTools.", 90),
    ]),
    ("Неделя 3. JavaScript и интерактив", [
        ("DOM и функции", "querySelector, textContent, classList, addEventListener, стрелочные функции.", 80),
        ("События и формы", "submit, preventDefault, ввод, клики, делегирование, работа с data-атрибутами.", 80),
        ("Валидация на клиенте", "Проверка логина, пароля, телефона, email; сообщения под полем; regex.", 90),
        ("Слайдер", "4 изображения, автопереключение раз в 3 секунды, кнопки назад/вперёд, пауза.", 90),
        ("Анимации", "transition, transform, keyframes, микроанимации, prefers-reduced-motion.", 80),
    ]),
    ("Неделя 4. Git и проектная работа", [
        ("Git: основы", "git init, status, add, commit -m, log, diff; осмысленные коммиты.", 60),
        ("Удалённый репозиторий", "remote, push, pull, ветки, конфликты, .gitignore для venv и *.db.", 70),
        ("Структура проекта", "Папки templates/static/src, README.md, requirements.txt, .env.example.", 70),
        ("Отладка в браузере", "Console, Elements, Network, Sources, breakpoints, чтение ошибок Flask.", 70),
        ("Статический прототип + git", "Собери 3 страницы прототипа, сделай 5+ коммитов и README.", 100),
    ]),
    ("Неделя 5. Python и Flask", [
        ("Python для web", "Типы, функции, модули, исключения, list/dict, чтение JSON, виртуальное окружение.", 80),
        ("Первый Flask-проект", "venv, pip install flask, app.py, маршрут /, debug, запуск на localhost.", 80),
        ("Маршруты и Jinja2", "route, переменные в URL, render_template, циклы/условия, фильтры, escape.", 90),
        ("Формы GET/POST", "request.args, request.form, валидация, redirect после POST (PRG).", 90),
        ("Сессии и flash", "session, secret_key, вход/выход, flash + get_flashed_messages, сообщения.", 90),
    ]),
    ("Неделя 6. SQL и проектирование БД", [
        ("Реляционная модель", "Таблицы, строки, PK, FK, UNIQUE, CHECK, 1:M, 3НФ.", 80),
        ("SELECT и фильтры", "SELECT, WHERE, AND/OR, ORDER BY, LIMIT, LIKE, NULL, COALESCE.", 80),
        ("JOIN и агрегаты", "INNER/LEFT JOIN, COUNT, SUM, AVG, GROUP BY, HAVING.", 90),
        ("Даты и подзапросы", "date(), strftime(), CASE, EXISTS, коррелированные подзапросы.", 90),
        ("ER и DDL «Корочки.есть»", "6 таблиц, связи, ограничения, ER-диаграмма, schema.sql с данными.", 100),
    ]),
    ("Неделя 7. Бэкенд и безопасность", [
        ("sqlite3 во Flask", "connect, row_factory, параметризованные запросы, commit, закрытие соединения.", 90),
        ("Регистрация", "Валидация всех полей, уникальный логин, хеширование пароля, ошибки на форме.", 90),
        ("Вход и сессии", "check_password_hash, session['user_id'], logout, защита маршрутов.", 80),
        ("Роли и доступ", "Пользователь/администратор, декоратор login_required, проверка role_id.", 80),
        ("SQL-инъекции, XSS, CSRF", "Параметры вместо конкатенации, autoescape, CSRF-токен, безопасные cookie.", 100),
    ]),
    ("Неделя 8. Модуль 1: full-stack приложение", [
        ("Каркас проекта", "app factory, конфиг, БД, шаблоны, статика, обработчики 404/500.", 90),
        ("Регистрация и вход", "Полный сценарий: форма → валидация → БД → вход → личный кабинет.", 100),
        ("Личный кабинет", "Свои заявки, статусы, пустое состояние, кнопка новой заявки.", 90),
        ("Создание заявки", "Курс из списка, дата ДД.ММ.ГГГГ, способ оплаты, валидация, запись в БД.", 100),
        ("Статусы и отзывы", "Новая → Идет обучение → Завершено; отзыв только после завершения.", 100),
    ]),
    ("Неделя 9. Модуль 2: дизайн", [
        ("Дизайн-концепция", "ЦА, сценарии, корпоративный стиль, палитра, шрифты, логотип.", 80),
        ("Прототип и компоненты", "Сетка, карточки, кнопки, поля, состояния hover/focus/error/empty.", 90),
        ("Мобильная версия", "390×844, мобильное меню, крупные зоны нажатия, читаемость, контраст.", 90),
        ("Слайдер и галерея", "4 одинаковых изображения, 3 секунды, кнопки, точки, пауза при наведении.", 90),
        ("Анимации и доступность", "Плавные переходы, skeleton, focus-visible, alt, aria-label, reduced-motion.", 90),
    ]),
    ("Неделя 10. Модуль 3: админка и оптимизация", [
        ("Админ-панель", "Все заявки: ФИО, телефон, курс, дата, оплата, статус.", 100),
        ("Фильтр и поиск", "Фильтр по статусу, поиск по ФИО/курсу, сортировка по дате, сброс фильтров.", 90),
        ("Пагинация и сообщения", "По 5–10 строк, номера страниц, flash после действий, пустой результат.", 90),
        ("Смена статусов", "«Идет обучение» и «Обучение завершено» (КОД 2026); проверка роли администратора.", 90),
        ("Оптимизация", "Индексы, отсутствие N+1, LIMIT, кэш, сжатие, ленивая загрузка изображений.", 100),
    ]),
    ("Неделя 11. Документы и вариативная часть", [
        ("README и ER", "Описание, стек, запуск, структура, схема БД, скриншоты, автор.", 80),
        ("Руководство пользователя", "1–2 страницы, 4+ скриншота: регистрация, заявка, админка, отзыв.", 90),
        ("JSON API", "GET/POST /api/applications, JSON, коды ответов, проверка авторизации.", 90),
        ("Тесты", "unittest/pytest: регистрация, вход, создание заявки, запрет админки.", 90),
        ("Деплой и бэкап", ".env, debug=False, миграции, резервная копия SQLite, чек-лист запуска.", 80),
    ]),
    ("Неделя 12. Пробники и экзаменационный день", [
        ("Пробник №1: Модуль 1", "Таймер 1:30. БД, регистрация, вход, заявки, статусы, git.", 100),
        ("Разбор ошибок №1", "Чек-лист 100 баллов, слабые критерии, повтор теории и SQL.", 70),
        ("Пробник №2: Модули 1–2", "Таймер 3:00. Плюс дизайн, адаптив 390×844, слайдер, анимации.", 180),
        ("Пробник №3: все модули", "Таймер 4:00. Полный сценарий + вариативная часть.", 240),
        ("Экзаменационный день", "Тайминг, git-коммиты, скриншоты, документы, типичные потери баллов.", 80),
    ]),
]

PLAN = []
for _w, (_theme, _days) in enumerate(WEEKS, start=1):
    for _d, (_title, _task, _minutes) in enumerate(_days, start=1):
        PLAN.append({
            "id": f"d{(_w - 1) * 5 + _d}",
            "n": (_w - 1) * 5 + _d,
            "week": _w,
            "theme": _theme,
            "title": _title,
            "task": _task,
            "minutes": _minutes,
        })

# ---------------------------------------------------------------------------
# 3. ТЕОРИЯ
# ---------------------------------------------------------------------------
LESSONS = [
    ("l01", "Экзамен", "ДЭ-2027 для веб-квалификации: что изменилось", 12, """
Ориентир — последний завершённый экзамен: КОД 09.02.07-3-2026,
квалификация «Разработчик веб и мультимедийных приложений»,
профильный уровень. На 2027 год структура с высокой вероятностью
сохранится: 3 модуля, 4 часа, 100 баллов.

ВАЖНО: на 23.11.2026 спецификация КИМ 09.02.07-3-2027 в открытом
доступе не подтверждена. Перед экзаменом скачай финальный документ
с bom.firpo.ru/Public/y/2027 и сверь модули, время и баллы.

МОДУЛИ И ВРЕМЯ
• Модуль 1. Проектирование и разработка информационных систем — 1 ч 30 мин.
• Модуль 2. Разработка дизайна веб-приложений — 1 ч 30 мин.
• Модуль 3. Проектирование, разработка и оптимизация веб-приложений — 1 ч 00 мин.

БАЛЛЫ (инвариант 75 + вариатив 25)
• Модуль 1 — 25: безопасность 18, разработка модулей 4, современные средства 3.
• Модуль 2 — 25: дизайн-концепция 13, требования к дизайну 4, современные тенденции 8.
• Модуль 3 — 25: веб-приложение 14, интерфейс пользователя 11.
• Вариативная часть — 25: определяет колледж (API, тесты, документация, деплой).

ПРЕДМЕТНАЯ ОБЛАСТЬ 2026
Портал «Корочки.есть» — запись на онлайн-курсы дополнительного
профессионального образования. Пользователь регистрируется, входит,
создаёт заявку на курс, указывает дату начала и способ оплаты.
Администратор (Admin / KorokNET) видит все заявки и меняет статусы:
«Новая» → «Идет обучение» → «Обучение завершено» (это требует КОД 2026)
с обязательной причиной.

ЧТО ПРОВЕРЯЮТ
• Полный стек: фронтенд, бэкенд, БД, ООП, библиотеки/фреймворки.
• Регистрация с валидацией и уникальным логином.
• Вход/выход, сессии, роли, защита админ-маршрутов.
• Заявки: создание, список, статусы, отзыв после завершения.
• Адаптивный дизайн 390×844, слайдер 4 изображения / 3 секунды.
• Анимации и микроанимации, аккуратный интерфейс.
• Git-репозиторий: исходники папкой, скрипт БД, README, документы.

ГЛАВНОЕ ОТЛИЧИЕ ОТ «ПРОГРАММИСТА»
Там был Python + SQLite + tkinter и 5 заданий «Чудо Обувь».
Здесь — веб-приложение: HTML/CSS/JS + серверный язык + БД + git.
Старый курс для «Программиста» лежит в legacy/ и больше не является
основным.
"""),
    ("l02", "HTML", "HTML: каркас, семантика, формы", 12, """
Минимальный каркас:

<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Корочки.есть — онлайн-курсы</title>
  <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
  <header class="site-header">...</header>
  <nav class="main-nav">...</nav>
  <main>...</main>
  <footer>...</footer>
  <script src="/static/js/app.js"></script>
</body>
</html>

СЕМАНТИКА
• header — шапка, nav — навигация, main — основное содержимое;
• section/article — смысловые блоки, footer — подвал;
• один h1 на страницу, дальше h2/h3 без пропуска уровней;
• изображения всегда с alt, декоративные — alt="".

ФОРМА РЕГИСТРАЦИИ
<form method="post" novalidate>
  <label for="login">Логин</label>
  <input id="login" name="login" required minlength="6"
         pattern="[A-Za-z0-9]{6,}" autocomplete="username">

  <label for="password">Пароль</label>
  <input id="password" name="password" type="password"
         required minlength="8" autocomplete="new-password">

  <label for="phone">Телефон</label>
  <input id="phone" name="phone" type="tel"
         placeholder="8(921)111-11-11" required>

  <label for="email">E-mail</label>
  <input id="email" name="email" type="email" required>

  <button type="submit">Зарегистрироваться</button>
</form>

ПРАВИЛА ЭКЗАМЕНА
• логин — латиница и цифры, не менее 6 символов, уникальный;
• пароль — минимум 8 символов;
• ФИО — кириллица и пробелы;
• телефон — 8(XXX)XXX-XX-XX;
• email — формат электронной почты;
• все поля обязательны, ошибки показываются на форме.
"""),
    ("l03", "CSS", "CSS: каскад, Flexbox, Grid", 12, """
ПОДКЛЮЧЕНИЕ И ПЕРЕМЕННЫЕ

:root {
  --brand: #2563eb;
  --brand-dark: #1e40af;
  --bg: #f8fafc;
  --ink: #0f172a;
  --muted: #64748b;
  --danger: #dc2626;
  --radius: 14px;
}

* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: system-ui, "Segoe UI", sans-serif;
  color: var(--ink);
  background: var(--bg);
  line-height: 1.5;
}

FLEXBOX: ШАПКА

.site-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 16px 24px;
}

GRID: КАРТОЧКИ КУРСОВ

.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px;
}
.course-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: var(--radius);
  padding: 20px;
  transition: transform .2s ease, box-shadow .2s ease;
}
.course-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(15, 23, 42, .12);
}

СОСТОЯНИЯ
• :hover — наведение;
• :focus-visible — видимый фокус с клавиатуры;
• .is-error — красная рамка и текст ошибки;
• .is-disabled — сниженная прозрачность, cursor: not-allowed.

ПРАВИЛА
• не больше 2–3 основных цветов;
• отступы кратны 4/8 px;
• контраст текста не ниже 4.5:1;
• никаких фиксированных высот, из-за которых ломается мобильная версия.
"""),
    ("l04", "CSS", "Адаптивность: 390×844 и mobile-first", 10, """
МОБИЛЬНЫЙ ЭКРАН ЭКЗАМЕНА — 390×844 px.
Проектируем сначала мобильную версию, затем расширяем.

/* база — мобильная */
.container { width: min(100% - 32px, 1120px); margin-inline: auto; }
.course-grid { grid-template-columns: 1fr; }
.main-nav { display: none; }
.main-nav.is-open { display: flex; flex-direction: column; }

/* планшет */
@media (min-width: 640px) {
  .course-grid { grid-template-columns: repeat(2, 1fr); }
}

/* десктоп */
@media (min-width: 960px) {
  .course-grid { grid-template-columns: repeat(3, 1fr); }
  .main-nav { display: flex; flex-direction: row; gap: 18px; }
  .nav-toggle { display: none; }
}

МОБИЛЬНЫЕ ПРАВИЛА
• зона нажатия — не меньше 44×44 px;
• шрифт полей — не меньше 16 px, иначе iOS зумит;
• таблицы превращаются в карточки или получают горизонтальный скролл;
• меню — кнопка-гамбургер с aria-expanded;
• изображения — max-width: 100%; height: auto;
• проверяй в DevTools: iPhone 12/13/14 (390×844).

ЧАСТЫЕ ОШИБКИ
• горизонтальный скролл из-за width: 100vw;
• текст, вылезающий из кнопки;
• фиксированная ширина 1200 px;
• мелкие ссылки в подвале;
• слайдер выше экрана и перекрывает контент.
"""),
    ("l05", "JavaScript", "JavaScript: DOM, события, валидация", 12, """
ПОИСК ЭЛЕМЕНТОВ

const form = document.querySelector('#register-form');
const login = document.querySelector('#login');
const error = document.querySelector('#login-error');

СОБЫТИЕ ОТПРАВКИ

form.addEventListener('submit', (event) => {
  let ok = true;
  if (!/^[A-Za-z0-9]{6,}$/.test(login.value.trim())) {
    error.textContent = 'Логин: латиница и цифры, минимум 6 символов';
    ok = false;
  } else {
    error.textContent = '';
  }
  if (!ok) event.preventDefault();
});

РЕГУЛЯРНЫЕ ВЫРАЖЕНИЯ ЭКЗАМЕНА

const LOGIN_RE = /^[A-Za-z0-9]{6,}$/;
const FIO_RE = /^[А-Яа-яЁё\\s-]+$/;
const PHONE_RE = /^8\\(\\d{3}\\)\\d{3}-\\d{2}-\\d{2}$/;
const EMAIL_RE = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;

СООБЩЕНИЯ
• ошибка — под конкретным полем, а не одним alert;
• цвет + текст, не только цвет;
• после исправления ошибка исчезает;
• серверная валидация всё равно обязательна: клиентскую легко обойти.

ПОЛЕЗНО
element.classList.toggle('is-error', !ok);
element.setAttribute('aria-invalid', String(!ok));
"""),
    ("l06", "JavaScript", "Слайдер 4 изображения / 3 секунды", 12, """
ТРЕБОВАНИЕ КОД 2026
Слайдер автоматически сменяет 4 изображения одинакового размера
с интервалом 3 секунды, имеет кнопки «назад/вперёд» и вписан в дизайн.

РАЗМЕТКА

<div class="slider" data-slider>
  <button class="slider__btn" data-prev aria-label="Назад">‹</button>
  <img class="slider__img" src="/static/img/slide-1.svg" alt="Курс 1">
  <button class="slider__btn" data-next aria-label="Вперёд">›</button>
  <div class="slider__dots"></div>
</div>

JS

const root = document.querySelector('[data-slider]');
const img = root.querySelector('.slider__img');
const slides = [
  '/static/img/slide-1.svg',
  '/static/img/slide-2.svg',
  '/static/img/slide-3.svg',
  '/static/img/slide-4.svg',
];
let index = 0;
let timer = null;

function show(i) {
  index = (i + slides.length) % slides.length;
  img.src = slides[index];
  img.alt = `Курс ${index + 1}`;
}
function start() {
  stop();
  timer = setInterval(() => show(index + 1), 3000);
}
function stop() { if (timer) clearInterval(timer); timer = null; }

root.querySelector('[data-prev]').addEventListener('click', () => { show(index - 1); start(); });
root.querySelector('[data-next]').addEventListener('click', () => { show(index + 1); start(); });
root.addEventListener('mouseenter', stop);
root.addEventListener('mouseleave', start);
start();

ПРОВЕРКА
• 4 изображения одного размера (object-fit: cover);
• смена ровно через 3 секунды;
• кнопки работают и сбрасывают таймер;
• на мобильном слайдер не ломает сетку;
• при prefers-reduced-motion автопрокрутку можно отключить.
"""),
    ("l07", "Git", "Git: репозиторий, коммиты, сдача", 10, """
ПЕРВЫЙ РЕПОЗИТОРИЙ

git init
git add .
git commit -m "feat: каркас проекта и схема БД"
git branch -M main
git remote add origin <url>
git push -u origin main

ЕЖЕДНЕВНЫЙ ЦИКЛ

git status
git diff
git add app.py templates/ static/
git commit -m "feat: регистрация и вход"
git push

ЧТО ПРОВЕРЯЕТ ЭКСПЕРТ
• исходники лежат папкой, а не одним архивом;
• есть README.md с описанием и запуском;
• есть скрипт БД (schema.sql) и данные;
• коммиты в начале и конце каждого модуля;
• нет venv/, __pycache__/, *.db, .env с секретами.

.gitignore

venv/
__pycache__/
*.pyc
*.db
.env
.DS_Store

СООБЩЕНИЯ КОММИТОВ
feat: ... — новая функциональность
fix: ... — исправление
docs: ... — документация
style: ... — вёрстка/оформление
refactor: ... — переработка кода

ЕСЛИ ЗАБЫЛ ЗАКОММИТИТЬ
Недосданный файл = 0 баллов за критерий. Коммить после каждого
законченного сценария, а не один раз в конце.
"""),
    ("l08", "Flask", "Flask: маршруты, шаблоны, статика", 12, """
УСТАНОВКА

python -m venv venv
# Windows: venv\\Scripts\\activate
# macOS/Linux: source venv/bin/activate
pip install flask
pip freeze > requirements.txt

МИНИМАЛЬНОЕ ПРИЛОЖЕНИЕ

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-me'

@app.get('/')
def index():
    return render_template('index.html')

@app.route('/applications/new', methods=['GET', 'POST'])
def new_application():
    if request.method == 'POST':
        course_id = request.form.get('course_id')
        # валидация и запись в БД
        return redirect(url_for('dashboard'))
    return render_template('application_new.html')

if __name__ == '__main__':
    app.run(debug=True)

СТРУКТУРА

project/
  app.py
  db.py
  schema.sql
  requirements.txt
  templates/
    base.html
    index.html
    register.html
    login.html
    dashboard.html
    admin.html
  static/
    css/style.css
    js/app.js
    img/

JINJA2

{% extends 'base.html' %}
{% block content %}
  <h1>{{ course.title }}</h1>
  {% for course in courses %}
    <article class="course-card">{{ course.title }}</article>
  {% endfor %}
{% endblock %}

{{ ... }} экранирует HTML автоматически — это защита от XSS.
"""),
    ("l09", "Flask", "Формы, сессии, flash и PRG", 12, """
ПОЛУЧЕНИЕ ДАННЫХ

login = request.form.get('login', '').strip()
password = request.form.get('password', '')
course_id = request.form.get('course_id', type=int)

ПОСЛЕ POST — REDIRECT (PRG)
redirect после успешной записи защищает от повторной отправки формы
при обновлении страницы.

return redirect(url_for('dashboard'))

СЕССИЯ

from flask import session

session['user_id'] = user['user_id']
session['role_id'] = user['role_id']
session.clear()          # выход

app.config['SECRET_KEY'] — обязателен, иначе сессия не работает.
Cookie: HttpOnly, SameSite=Lax, Secure при HTTPS.

FLASH-СООБЩЕНИЯ

flash('Заявка создана', 'success')
flash('Неверный логин или пароль', 'error')

{% with messages = get_flashed_messages(with_categories=true) %}
  {% for category, message in messages %}
    <div class="alert alert--{{ category }}">{{ message }}</div>
  {% endfor %}
{% endwith %}

ЗАЩИТА МАРШРУТОВ

def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Сначала войдите', 'error')
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapper

ОШИБКИ ВАЛИДАЦИИ
Сохраняй введённые значения и показывай ошибки под полями,
а не переводи пользователя на пустую форму.
"""),
    ("l10", "SQL", "SQL: SELECT, JOIN, GROUP BY, даты", 12, """
ВЫБОРКА

SELECT application_id, start_date, payment_method
FROM applications
WHERE status_id = 1
ORDER BY start_date
LIMIT 10;

ПОИСК

SELECT user_id, full_name, phone
FROM users
WHERE full_name LIKE '%Иван%'
   OR phone LIKE '8(921)%'
ORDER BY full_name;

JOIN

SELECT a.application_id, u.full_name, c.title, s.status_name
FROM applications a
JOIN users u ON u.user_id = a.user_id
JOIN courses c ON c.course_id = a.course_id
JOIN application_statuses s ON s.status_id = a.status_id
ORDER BY a.application_id;

АГРЕГАТЫ

SELECT c.title, COUNT(*) AS applications_count
FROM applications a
JOIN courses c ON c.course_id = a.course_id
GROUP BY c.course_id, c.title
HAVING COUNT(*) > 1
ORDER BY applications_count DESC;

ДАТЫ

SELECT date('now');
SELECT strftime('%Y-%m', created_at) AS month, COUNT(*)
FROM applications
GROUP BY month
ORDER BY month;

CASE

SELECT application_id,
       CASE WHEN status_id = 3 THEN 'завершено' ELSE 'в работе' END AS state
FROM applications;

ПАРАМЕТРЫ — ТОЛЬКО ТАК

cur.execute('SELECT * FROM users WHERE login = ?', (login,))

Никогда не склеивай SQL строками: это SQL-инъекция.
"""),
    ("l11", "БД", "БД «Корочки.есть»: 6 таблиц и 3НФ", 12, """
СУЩНОСТИ
• roles — роли (администратор, пользователь);
• users — пользователи: логин, хеш пароля, ФИО, телефон, email, роль;
• courses — курсы: название, описание, длительность, цена;
• application_statuses — справочник статусов;
• applications — заявки: пользователь, курс, дата начала, оплата, статус;
• reviews — отзывы: заявка, пользователь, оценка 1–5, текст.

СВЯЗИ
users 1:M applications
courses 1:M applications
application_statuses 1:M applications
applications 1:1 reviews
users 1:M reviews

ПОЧЕМУ 3НФ
• 1НФ — атомарные значения, нет списков в ячейке;
• 2НФ — нет зависимости части ключа от неключа;
• 3НФ — нет транзитивных зависимостей: статус и курс вынесены
  в справочники, а не хранятся текстом в заявке.

ОГРАНИЧЕНИЯ
• users.login UNIQUE;
• applications.payment_method CHECK IN ('cash','phone_transfer');
• reviews.rating CHECK BETWEEN 1 AND 5;
• reviews.application_id UNIQUE — один отзыв на заявку;
• FK с ON DELETE CASCADE/RESTRICT.

ER-ДИАГРАММА
Нарисуй 6 прямоугольников, атрибуты, PK/FK и линии связей.
Подпиши кардинальности 1 и M. Сохрани в PDF/PNG и приложи к README.

СКРИПТ БД
schema.sql должен содержать CREATE TABLE + INSERT с демо-данными,
чтобы эксперт мог поднять базу одной командой.
"""),
    ("l12", "Безопасность", "Регистрация, вход, роли, защита", 14, """
РЕГИСТРАЦИЯ — ПРОВЕРКИ НА СЕРВЕРЕ
• логин: ^[A-Za-z0-9]{6,}$, проверить уникальность;
• пароль: не короче 8 символов;
• ФИО: кириллица и пробелы;
• телефон: 8(XXX)XXX-XX-XX;
• email: формат почты + уникальность;
• все поля обязательны.

ХЕШИРОВАНИЕ

from werkzeug.security import generate_password_hash, check_password_hash

password_hash = generate_password_hash(password)
# при входе:
if user and check_password_hash(user['password_hash'], password):
    session['user_id'] = user['user_id']

Никогда не храни пароль в открытом виде.

РОЛИ
role_id = 1 — администратор, 2 — пользователь.
Админ-маршруты проверяют и сессию, и роль:

if session.get('role_id') != 1:
    abort(403)

ДОСТУП АДМИНИСТРАТОРА
Логин Admin, пароль KorokNET — создать при инициализации БД.
Прямой заход на /admin без входа должен перенаправлять на вход
или отдавать 403, а не показывать данные.

SQL-ИНЪЕКЦИИ
Плохо:  f"SELECT * FROM users WHERE login = '{login}'"
Хорошо: cur.execute('SELECT * FROM users WHERE login = ?', (login,))

XSS
Jinja2 экранирует {{ }}. Не используй |safe для пользовательских данных.

CSRF
Для POST-форм добавляй скрытый токен, сравнивай его в сессии.
SameSite=Lax на cookie — базовая дополнительная защита.

ОШИБКИ
Сообщение «Неверный логин или пароль» не раскрывает, что именно неверно.
Не показывай traceback и пути к файлам в production (debug=False).
"""),
    ("l13", "Flask", "Заявки, статусы, отзывы, админка", 14, """
СОЗДАНИЕ ЗАЯВКИ
1. Пользователь выбирает курс из выпадающего списка.
2. Указывает дату начала в формате ДД.ММ.ГГГГ.
3. Выбирает оплату: наличными или переводом по номеру телефона.
4. Сервер проверяет поля и пишет заявку со статусом «Новая».

СПИСОК ЗАЯВОК ПОЛЬЗОВАТЕЛЯ
SELECT a.application_id, c.title, a.start_date, a.payment_method,
       s.status_name, a.cancel_reason
FROM applications a
JOIN courses c ON c.course_id = a.course_id
JOIN application_statuses s ON s.status_id = a.status_id
WHERE a.user_id = ?
ORDER BY a.created_at DESC;

СТАТУСЫ
1 «Новая» → 2 «Идет обучение» → 3 «Обучение завершено».
4 «Отменена» — дополнительная функция из КОД 2025 (с причиной); в КОД 2026 не требуется.
Администратор меняет статус через POST и видит flash-подтверждение.

ОТЗЫВ
Кнопка «Оставить отзыв» доступна только для заявки со статусом
«Обучение завершено» и только один раз.
Оценка 1–5 + текст. После сохранения отзыв виден в карточке курса
или в личном кабинете.

АДМИН-ПАНЕЛЬ
• таблица всех заявок: ФИО, телефон, курс, дата, оплата, статус;
• фильтр по статусу;
• поиск по ФИО и названию курса;
• сортировка по дате;
• пагинация по 5–10 записей;
• пустое состояние «Заявок не найдено».

ПРОВЕРКА ПРАВ
Каждый POST в админке проверяет роль. Нельзя менять статус
через прямой запрос, если пользователь не администратор.
"""),
    ("l14", "Дизайн", "Дизайн, адаптив, анимации, документы", 12, """
МОДУЛЬ 2 — ЭТО НЕ ТОЛЬКО КРАСИВО
Эксперт смотрит: корпоративный стиль, требования к дизайну,
современные тенденции. Сделай мини-дизайн-систему.

ПАЛИТРА И ТИПОГРАФИКА
• 1 основной цвет, 1 акцент, нейтральные оттенки;
• шрифт system-ui или один подключённый;
• размеры 14/16/20/28/36, межстрочный 1.4–1.6;
• отступы 4/8/12/16/24/32.

КОМПОНЕНТЫ
кнопка (primary/secondary/danger), поле (обычное/фокус/ошибка),
карточка курса, бейдж статуса, alert, пагинация, пустое состояние.

АДАПТИВ 390×844
Проверь: меню, формы, таблицу заявок, админку, слайдер.
Ничего не должно вылезать за экран.

СЛАЙДЕР
4 изображения одного размера, автопереключение 3 секунды,
кнопки назад/вперёд, пауза при наведении.

АНИМАЦИИ
• появление карточек: opacity + translateY 8–12 px;
• hover кнопок: смена цвета и лёгкий подъём;
• flash: плавное появление;
• skeleton при загрузке;
• @media (prefers-reduced-motion: reduce) — отключить автодвижение.

ДОКУМЕНТЫ
• README.md: назначение, стек, запуск, структура, схема БД;
• ER-диаграмма;
• Руководство_пользователя: 1–2 страницы, 4+ скриншота
  (регистрация, заявка, личный кабинет, админка);
• скриншоты мобильной версии 390×844.

МОДУЛЬ 3
Собери всё вместе, добавь оптимизацию: индексы, отсутствие N+1,
LIMIT, кэш, сжатые изображения, аккуратные коммиты.
"""),
    ("l15", "Экзамен", "Стратегия: тайминг и 100 баллов", 12, """
ЦЕЛЬ «5» — 90+ из 100. Нельзя «потерять» целый модуль.

ТАЙМИНГ
• 1:30 — Модуль 1: БД, регистрация, вход, заявки, статусы, git.
• 1:30 — Модуль 2: дизайн, адаптив 390×844, слайдер, анимации.
• 1:00 — Модуль 3: интеграция, админка, оптимизация, финальный коммит.

ПОРЯДОК РАБОТЫ
1. Создай репозиторий и коммит «start» в первые 2 минуты.
2. Подними БД и минимальный каркас.
3. Сделай вертикальный срез: регистрация → вход → заявка → админка.
4. Только потом красота и дополнительные функции.
5. В конце каждого модуля — commit + push.

ЧЕК-ЛИСТ ПЕРЕД СДАЧЕЙ
• Все страницы открываются без 500.
• Регистрация: ошибки на форме, уникальный логин.
• Вход/выход, прямой заход в /admin запрещён.
• Заявка создаётся, видна в кабинете и админке.
• Статусы меняются; отмена — дополнительно, в КОД 2026 не требуется.
• Отзыв только после завершения.
• Мобильная версия 390×844 без горизонтального скролла.
• Слайдер: 4 изображения, 3 секунды, кнопки.
• README, schema.sql, ER, руководство, скриншоты.
• Нет venv, *.db, паролей и мусора в репозитории.

ТИПИЧНЫЕ ПОТЕРИ БАЛЛОВ
• пароль хранится открытым текстом;
• нет серверной валидации;
• админка доступна по прямой ссылке;
• слайдер не 3 секунды или не 4 изображения;
• нет мобильной версии;
• один коммит в конце;
• нет README/руководства.

ЕСЛИ НЕ УСПЕВАЕШЬ
Сначала закрой дешёвые и обязательные критерии: валидация, роли,
заявки, статусы, адаптив, git. Красивые анимации — в конце.
"""),
]

# ---------------------------------------------------------------------------
# 4. ТЕСТЫ
# ---------------------------------------------------------------------------
def q(text, opts, ans, expl, topic):
    return {"q": text, "opts": opts, "ans": ans, "explain": expl, "topic": topic}


QUIZ = [
    q("Какой КОД взят за основу курса?",
      ["09.02.07-2-2026 (Программист)", "09.02.07-3-2026 (веб)", "09.02.07-1-2025 (БД)", "09.02.07-5-2026"],
      1, "Последний завершённый экзамен для веб-квалификации — КОД 09.02.07-3-2026.", "Экзамен"),
    q("Сколько модулей на ДЭ веб-квалификации?",
      ["2", "3", "4", "5"], 1, "Три модуля: информационные системы, дизайн, разработка и оптимизация.", "Экзамен"),
    q("Сколько времени даётся на все модули?",
      ["3 ч", "4 ч", "4 ч 30 мин", "5 ч"], 1, "1:30 + 1:30 + 1:00 = 4 часа.", "Экзамен"),
    q("Как распределены баллы?",
      ["50 + 50", "75 инвариант + 25 вариатив", "80 + 20", "100 инвариант"],
      1, "Инвариантная часть — 75, вариативная — 25, всего 100.", "Экзамен"),
    q("Сколько баллов даёт Модуль 1?",
      ["20", "25", "30", "50"], 1, "Модуль 1 — 25 баллов: безопасность 18, модули 4, средства 3.", "Экзамен"),
    q("Сколько времени на Модуль 2?",
      ["1 ч", "1 ч 30 мин", "2 ч", "30 мин"], 1, "Модуль 2 — 1 час 30 минут.", "Экзамен"),
    q("Предметная область образца 2026 года?",
      ["«Чудо Обувь»", "«Корочки.есть»", "«Мой Не Сам»", "«СпортОпт»"],
      1, "Портал онлайн-курсов «Корочки.есть».", "Экзамен"),
    q("Логин и пароль администратора в образце 2026?",
      ["admin / admin", "Admin / KorokNET", "adminka / password", "root / root"],
      1, "В КОД 09.02.07-3-2026 — Admin / KorokNET.", "Экзамен"),

    q("Зачем нужен <!DOCTYPE html>?",
      ["Для стилей", "Включает стандартный режим браузера", "Подключает JS", "Задаёт кодировку"],
      1, "Без DOCTYPE браузер может включить quirks mode.", "HTML"),
    q("Какой meta-тег нужен для мобильной версии?",
      ["charset", "viewport", "description", "refresh"], 1,
      "meta name=viewport width=device-width, initial-scale=1.", "HTML"),
    q("Семантический тег для навигации?",
      ["<div>", "<nav>", "<menu>", "<aside>"], 1, "<nav> описывает блок навигации.", "HTML"),
    q("Как связать label с полем ввода?",
      ["name", "for + id", "class", "placeholder"], 1,
      "Атрибут for у label совпадает с id поля.", "HTML"),
    q("Какой type у поля телефона?",
      ["text", "tel", "phone", "number"], 1, "type=tel даёт телефонную клавиатуру на мобильном.", "HTML"),
    q("Зачем нужен alt у изображения?",
      ["Для SEO", "Для доступности и случая, когда картинка не загрузилась", "Для стилей", "Для JS"],
      1, "alt описывает изображение для скринридеров и при сбое загрузки.", "HTML"),

    q("Что делает box-sizing: border-box?",
      ["Добавляет рамку", "Включает padding и border в width", "Убирает margin", "Делает блок flex"],
      1, "Ширина включает содержимое, padding и border — удобнее считать сетку.", "CSS"),
    q("Какое свойство выравнивает по главной оси Flexbox?",
      ["align-items", "justify-content", "gap", "flex-wrap"], 1,
      "justify-content — главная ось, align-items — поперечная.", "CSS"),
    q("Как задать три колонки Grid?",
      ["grid: 3", "grid-template-columns: repeat(3, 1fr)", "columns: 3", "display: columns"],
      1, "repeat(3, 1fr) создаёт три равные колонки.", "CSS"),
    q("Mobile-first media query использует…",
      ["max-width", "min-width", "only screen", "orientation"], 1,
      "Сначала мобильные стили, затем расширяем через min-width.", "CSS"),
    q("Как объявить CSS-переменную?",
      ["$brand: #fff", "--brand: #fff", "var(--brand)", "@brand: #fff"], 1,
      "Переменная объявляется как --brand, используется через var(--brand).", "CSS"),
    q("Что важнее по специфичности?",
      ["класс", "id", "тег", "universal"], 1, "id > класс > тег > *.", "CSS"),
    q("Зачем нужен :focus-visible?",
      ["Для мыши", "Для видимого фокуса с клавиатуры", "Для печати", "Для анимации"],
      1, "Помогает сохранить доступность, не показывая рамку при клике мышью.", "CSS"),

    q("Как найти элемент по id?",
      ["document.getId", "document.querySelector('#id')", "document.byId", "document.find"],
      1, "querySelector принимает CSS-селектор.", "JS"),
    q("Как отменить стандартную отправку формы?",
      ["event.stop()", "event.preventDefault()", "return false", "form.cancel()"],
      1, "preventDefault останавливает переход и позволяет проверить поля.", "JS"),
    q("Что делает setInterval(fn, 3000)?",
      ["Вызывает fn один раз", "Вызывает fn каждые 3 секунды", "Ждёт 3 секунды", "Останавливает таймер"],
      1, "Интервал 3000 мс = 3 секунды — то, что нужно слайдеру.", "JS"),
    q("Как переключить класс элемента?",
      ["element.class = ...", "classList.toggle('is-open')", "style.class", "setClass()"],
      1, "classList.toggle добавляет или убирает класс.", "JS"),
    q("Что возвращает fetch()?",
      ["JSON", "Promise", "Строку", "Массив"], 1, "fetch возвращает Promise; далее response.json().", "JS"),

    q("Какой декоратор задаёт маршрут во Flask?",
      ["@app.router", "@app.route", "@route", "@get"], 1,
      "Современный вариант: @app.get/post; классический — @app.route.", "Flask"),
    q("Как вывести переменную в Jinja2?",
      ["{ user }", "{{ user }}", "<%= user %>", "${user}"], 1,
      "Двойные фигурные скобки, HTML экранируется автоматически.", "Flask"),
    q("Как наследовать шаблон?",
      ["{% include %}", "{% extends 'base.html' %}", "{% import %}", "{% block %}"],
      1, "extends подключает базовый шаблон, block заполняет его части.", "Flask"),
    q("Как получить поле формы?",
      ["request.args", "request.form.get()", "request.json", "session.get()"], 1,
      "request.form — данные POST-формы.", "Flask"),
    q("Что обязательно для сессии Flask?",
      ["DEBUG=True", "SECRET_KEY", "SQLALCHEMY", "CSRF"], 1,
      "Без SECRET_KEY Flask не сможет подписать cookie сессии.", "Flask"),
    q("Зачем redirect после успешного POST?",
      ["Для красоты", "Чтобы обновление страницы не отправило форму повторно", "Для SEO", "Для кэша"],
      1, "Паттерн Post/Redirect/Get.", "Flask"),

    q("Что такое первичный ключ?",
      ["Любой столбец", "Уникальный идентификатор строки", "Внешняя ссылка", "Индекс для поиска"],
      1, "PRIMARY KEY уникален и не может быть NULL.", "SQL"),
    q("Что делает INNER JOIN?",
      ["Возвращает все строки", "Только строки с совпадением в обеих таблицах", "Удаляет дубли", "Сортирует"],
      1, "INNER JOIN оставляет только совпавшие записи.", "SQL"),
    q("Какая функция считает количество строк?",
      ["SUM", "COUNT", "AVG", "MAX"], 1, "COUNT(*) считает строки.", "SQL"),
    q("Чем HAVING отличается от WHERE?",
      ["Ничем", "HAVING фильтрует группы после GROUP BY", "HAVING быстрее", "WHERE только для чисел"],
      1, "WHERE фильтрует строки до группировки, HAVING — группы после.", "SQL"),
    q("Как безопасно передать логин в SQL?",
      ["Склеить строкой", "Через параметр ? и кортеж", "Через f-строку", "Через %"],
      1, "Параметризованный запрос защищает от SQL-инъекций.", "SQL"),
    q("Что обеспечивает 3НФ?",
      ["Скорость", "Отсутствие транзитивных зависимостей", "Шифрование", "Резервное копирование"],
      1, "Каждый неключевой атрибут зависит только от ключа.", "БД"),
    q("Зачем UNIQUE на login?",
      ["Для сортировки", "Чтобы логины не повторялись", "Для связи таблиц", "Для индекса"],
      1, "Уникальность логина требуется по заданию.", "БД"),
    q("Как получить текущую дату в SQLite?",
      ["NOW()", "date('now')", "CURRENT_DATE()", "today()"], 1,
      "В SQLite — date('now'), в MySQL — CURDATE().", "SQL"),
    q("Зачем нужен индекс?",
      ["Для красоты", "Ускоряет поиск и фильтрацию", "Шифрует данные", "Создаёт связи"],
      1, "Индекс ускоряет SELECT/WHERE/JOIN, но замедляет запись.", "БД"),

    q("Как хранить пароль?",
      ["Открытым текстом", "В base64", "Хеш + соль", "В cookie"], 2,
      "werkzeug.security.generate_password_hash + check_password_hash.", "Безопасность"),
    q("Зачем нужен CSRF-токен?",
      ["Для кэша", "Чтобы чужая форма не отправила POST от имени пользователя", "Для SQL", "Для слайдера"],
      1, "CSRF-токен подтверждает, что запрос пришёл с нашей формы.", "Безопасность"),
    q("Что защищает от XSS в Jinja2?",
      ["autoescape", "debug", "session", "redirect"], 0,
      "Jinja2 экранирует {{ }} по умолчанию.", "Безопасность"),
    q("Что обязательно должно быть в git-репозитории?",
      ["Только архив", "Исходники папкой + schema.sql + README + документы", "Только .exe", "Только скриншоты"],
      1, "Эксперт должен увидеть структуру проекта и скрипт БД.", "Git"),
    q("Что стоит добавить в .gitignore?",
      ["templates/", "venv/, __pycache__/, *.db, .env", "README.md", "static/"],
      1, "Секреты, окружение и локальная БД не должны попадать в репозиторий.", "Git"),
    q("Какой размер мобильного макета в задании?",
      ["320×568", "375×667", "390×844", "414×896"], 2,
      "В КОД прямо указано 390×844 px.", "Дизайн"),
    q("Слайдер по заданию 2026: сколько изображений и интервал?",
      ["3 / 2 с", "4 / 3 с", "5 / 3 с", "4 / 5 с"], 1,
      "4 одинаковых изображения, автопереключение раз в 3 секунды.", "Дизайн"),
    q("Когда доступен отзыв о курсе?",
      ["Сразу после заявки", "После статуса «Обучение завершено»", "После оплаты", "Всегда"],
      1, "Дополнительный функционал 2026: отзыв только после прохождения курса.", "Экзамен"),
    q("Какой формат даты начала обучения в Модуле 2?",
      ["YYYY-MM-DD", "ДД.ММ.ГГГГ", "MM/DD/YYYY", "любой"], 1,
      "В дополнительном функционале указан формат ДД.ММ.ГГГГ.", "Экзамен"),
    q("Что должно быть в правом верхнем углу после входа?",
      ["Логин", "ФИО", "Роль", "Баланс"], 1,
      "По аналогии с заданиями ДЭ — ФИО пользователя и выход.", "Дизайн"),
    q("Что проверяет Модуль 3?",
      ["Только БД", "Интеграцию дизайна, адаптив, анимации и качество кода", "Только документы", "Только git"],
      1, "Модуль 3 — проектирование, разработка и оптимизация веб-приложения.", "Экзамен"),
    q("Сколько баллов у вариативной части?",
      ["10", "20", "25", "50"], 2, "В КОД 2026 — 25 баллов, всего 100.", "Экзамен"),
]

# ---------------------------------------------------------------------------
# 5. SQL-ПРАКТИКА (SQLite, портал «Корочки.есть»)
# ---------------------------------------------------------------------------
SQL_TASKS = [
    {"id": "s01", "title": "1. Каталог курсов", "level": "лёгкое",
     "task": "Выведите course_id, название, длительность в часах и цену всех курсов. Сортировка по course_id.",
     "hint": "SELECT ... FROM courses ORDER BY course_id",
     "expected": "SELECT course_id, title, duration_hours, price FROM courses ORDER BY course_id;"},
    {"id": "s02", "title": "2. Пользователи и роли", "level": "лёгкое",
     "task": "Выведите user_id, логин, ФИО и название роли. Сортировка по user_id.",
     "hint": "JOIN roles r ON r.role_id = u.role_id",
     "expected": "SELECT u.user_id, u.login, u.full_name, r.role_name "
                 "FROM users u JOIN roles r ON r.role_id = u.role_id ORDER BY u.user_id;"},
    {"id": "s03", "title": "3. Все заявки с расшифровкой", "level": "среднее",
     "task": "Выведите application_id, ФИО, название курса, дату начала и статус. Сортировка по application_id.",
     "hint": "Три JOIN: users, courses, application_statuses",
     "expected": "SELECT a.application_id, u.full_name, c.title, a.start_date, s.status_name "
                 "FROM applications a "
                 "JOIN users u ON u.user_id = a.user_id "
                 "JOIN courses c ON c.course_id = a.course_id "
                 "JOIN application_statuses s ON s.status_id = a.status_id "
                 "ORDER BY a.application_id;"},
    {"id": "s04", "title": "4. Заявки по статусам", "level": "среднее",
     "task": "Посчитайте количество заявок в каждом статусе. Выведите status_id, название статуса и количество. Сортировка по status_id.",
     "hint": "JOIN application_statuses + GROUP BY + COUNT(*)",
     "expected": "SELECT s.status_id, s.status_name, COUNT(a.application_id) "
                 "FROM application_statuses s "
                 "LEFT JOIN applications a ON a.status_id = s.status_id "
                 "GROUP BY s.status_id, s.status_name ORDER BY s.status_id;"},
    {"id": "s05", "title": "5. Популярность курсов", "level": "среднее",
     "task": "Для каждого курса выведите название и количество заявок. Сортировка по количеству по убыванию, затем по названию.",
     "hint": "LEFT JOIN applications + GROUP BY + ORDER BY COUNT(*) DESC",
     "expected": "SELECT c.title, COUNT(a.application_id) AS cnt "
                 "FROM courses c LEFT JOIN applications a ON a.course_id = c.course_id "
                 "GROUP BY c.course_id, c.title ORDER BY cnt DESC, c.title;"},
    {"id": "s06", "title": "6. Выручка по завершённым курсам", "level": "сложное",
     "task": "Посчитайте выручку по каждому курсу только по заявкам со статусом «Обучение завершено». Выведите название курса и сумму. Сортировка по сумме по убыванию, затем по названию.",
     "hint": "JOIN courses + WHERE status_name = 'Обучение завершено' + SUM(price)",
     "expected": "SELECT c.title, SUM(c.price) AS revenue "
                 "FROM applications a "
                 "JOIN courses c ON c.course_id = a.course_id "
                 "JOIN application_statuses s ON s.status_id = a.status_id "
                 "WHERE s.status_name = 'Обучение завершено' "
                 "GROUP BY c.course_id, c.title ORDER BY revenue DESC, c.title;"},
    {"id": "s07", "title": "7. Общая выручка и средний чек", "level": "сложное",
     "task": "По завершённым заявкам выведите количество заявок, общую выручку и средний чек. Округлите деньги до копеек.",
     "hint": "COUNT(*), SUM(c.price), ROUND(AVG(c.price), 2) + WHERE status_name",
     "expected": "SELECT COUNT(*) AS orders_count, ROUND(SUM(c.price), 2) AS revenue, "
                 "ROUND(AVG(c.price), 2) AS avg_check "
                 "FROM applications a "
                 "JOIN courses c ON c.course_id = a.course_id "
                 "JOIN application_statuses s ON s.status_id = a.status_id "
                 "WHERE s.status_name = 'Обучение завершено';"},
    {"id": "s08", "title": "8. Поиск пользователей", "level": "лёгкое",
     "task": "Найдите пользователей, у которых телефон начинается на 8(921) или email начинается на admin. Выведите user_id, ФИО, телефон, email. Сортировка по user_id.",
     "hint": "WHERE phone LIKE '8(921)%' OR email LIKE 'admin%'",
     "expected": "SELECT user_id, full_name, phone, email FROM users "
                 "WHERE phone LIKE '8(921)%' OR email LIKE 'admin%' ORDER BY user_id;"},
    {"id": "s09", "title": "9. Заявки пользователя ivanov01", "level": "среднее",
     "task": "Выведите application_id, название курса, дату начала и статус заявок пользователя с логином ivanov01. Сортировка по дате начала.",
     "hint": "JOIN users + WHERE u.login = 'ivanov01' + JOIN courses/statuses",
     "expected": "SELECT a.application_id, c.title, a.start_date, s.status_name "
                 "FROM applications a "
                 "JOIN users u ON u.user_id = a.user_id "
                 "JOIN courses c ON c.course_id = a.course_id "
                 "JOIN application_statuses s ON s.status_id = a.status_id "
                 "WHERE u.login = 'ivanov01' ORDER BY a.start_date, a.application_id;"},
    {"id": "s10", "title": "10. Отзывы с оценкой 4–5", "level": "среднее",
     "task": "Выведите review_id, ФИО автора, название курса, оценку и текст отзыва. Только оценки 4 и 5. Сортировка по оценке по убыванию, затем по review_id.",
     "hint": "JOIN reviews → users → applications → courses + WHERE rating >= 4",
     "expected": "SELECT r.review_id, u.full_name, c.title, r.rating, r.review_text "
                 "FROM reviews r "
                 "JOIN users u ON u.user_id = r.user_id "
                 "JOIN applications a ON a.application_id = r.application_id "
                 "JOIN courses c ON c.course_id = a.course_id "
                 "WHERE r.rating >= 4 ORDER BY r.rating DESC, r.review_id;"},
    {"id": "s11", "title": "11. Курсы без заявок", "level": "сложное",
     "task": "Выведите course_id и название курсов, на которые ещё нет ни одной заявки. Сортировка по course_id.",
     "hint": "LEFT JOIN applications + WHERE a.application_id IS NULL",
     "expected": "SELECT c.course_id, c.title FROM courses c "
                 "LEFT JOIN applications a ON a.course_id = c.course_id "
                 "WHERE a.application_id IS NULL ORDER BY c.course_id;"},
    {"id": "s12", "title": "12. Пользователи с 2+ заявками", "level": "сложное",
     "task": "Выведите user_id, ФИО и количество заявок для пользователей, у которых больше одной заявки. Сортировка по количеству по убыванию, затем по user_id.",
     "hint": "JOIN + GROUP BY + HAVING COUNT(*) > 1",
     "expected": "SELECT u.user_id, u.full_name, COUNT(a.application_id) AS cnt "
                 "FROM users u JOIN applications a ON a.user_id = u.user_id "
                 "GROUP BY u.user_id, u.full_name HAVING COUNT(*) > 1 "
                 "ORDER BY cnt DESC, u.user_id;"},
    {"id": "s13", "title": "13. Последняя заявка каждого пользователя", "level": "сложное",
     "task": "Для каждого пользователя, у которого есть заявки, выведите user_id, ФИО, application_id и дату создания последней заявки. Сортировка по user_id.",
     "hint": "Коррелированный подзапрос: a.application_id = (SELECT ... ORDER BY created_at DESC LIMIT 1)",
     "expected": "SELECT u.user_id, u.full_name, a.application_id, a.created_at "
                 "FROM users u JOIN applications a ON a.user_id = u.user_id "
                 "WHERE a.application_id = (SELECT a2.application_id FROM applications a2 "
                 "WHERE a2.user_id = u.user_id ORDER BY a2.created_at DESC, a2.application_id DESC LIMIT 1) "
                 "ORDER BY u.user_id;"},
    {"id": "s14", "title": "14. Причины отмены", "level": "лёгкое",
     "task": "Выведите application_id, ФИО и причину отмены для отменённых заявок. Сортировка по application_id.",
     "hint": "WHERE s.status_name = 'Отменена' AND a.cancel_reason IS NOT NULL",
     "expected": "SELECT a.application_id, u.full_name, a.cancel_reason "
                 "FROM applications a "
                 "JOIN users u ON u.user_id = a.user_id "
                 "JOIN application_statuses s ON s.status_id = a.status_id "
                 "WHERE s.status_name = 'Отменена' AND a.cancel_reason IS NOT NULL "
                 "ORDER BY a.application_id;"},
    {"id": "s15", "title": "15. Заявки по месяцам", "level": "сложное",
     "task": "Сгруппируйте заявки по месяцу создания. Выведите месяц в формате YYYY-MM и количество. Сортировка по месяцу.",
     "hint": "strftime('%Y-%m', created_at) + GROUP BY",
     "expected": "SELECT strftime('%Y-%m', created_at) AS month, COUNT(*) AS cnt "
                 "FROM applications GROUP BY month ORDER BY month;"},
    {"id": "s16", "title": "16. Средний рейтинг курсов", "level": "сложное",
     "task": "Для курсов, у которых есть отзывы, выведите название, средний рейтинг (округлить до 2 знаков) и количество отзывов. Сортировка по рейтингу по убыванию, затем по названию.",
     "hint": "JOIN reviews → applications → courses + AVG(rating) + GROUP BY",
     "expected": "SELECT c.title, ROUND(AVG(r.rating), 2) AS avg_rating, COUNT(*) AS reviews_count "
                 "FROM reviews r "
                 "JOIN applications a ON a.application_id = r.application_id "
                 "JOIN courses c ON c.course_id = a.course_id "
                 "GROUP BY c.course_id, c.title ORDER BY avg_rating DESC, c.title;"},
    {"id": "s17", "title": "17. Оплата: наличные и перевод", "level": "среднее",
     "task": "Посчитайте количество заявок и сумму курсов по каждому способу оплаты. Выведите payment_method, количество и сумму. Сортировка по payment_method.",
     "hint": "GROUP BY payment_method + COUNT(*) + SUM(c.price)",
     "expected": "SELECT a.payment_method, COUNT(*) AS cnt, ROUND(SUM(c.price), 2) AS total "
                 "FROM applications a JOIN courses c ON c.course_id = a.course_id "
                 "GROUP BY a.payment_method ORDER BY a.payment_method;"},
    {"id": "s18", "title": "18. Уже начавшиеся заявки", "level": "среднее",
     "task": "Выведите application_id, ФИО, название курса и дату начала для заявок, у которых дата начала раньше сегодняшней. Сортировка по дате начала, затем по application_id.",
     "hint": "WHERE a.start_date < date('now')",
     "expected": "SELECT a.application_id, u.full_name, c.title, a.start_date "
                 "FROM applications a "
                 "JOIN users u ON u.user_id = a.user_id "
                 "JOIN courses c ON c.course_id = a.course_id "
                 "WHERE a.start_date < date('now') "
                 "ORDER BY a.start_date, a.application_id;"},
    {"id": "s19", "title": "19. Новые заявки за месяц", "level": "среднее",
     "task": "Выведите application_id, ФИО, курс и дату создания заявок, созданных за последние 30 дней. Сортировка по дате создания, затем по application_id.",
     "hint": "WHERE a.created_at >= date('now','-30 days')",
     "expected": "SELECT a.application_id, u.full_name, c.title, a.created_at "
                 "FROM applications a "
                 "JOIN users u ON u.user_id = a.user_id "
                 "JOIN courses c ON c.course_id = a.course_id "
                 "WHERE a.created_at >= date('now','-30 days') "
                 "ORDER BY a.created_at, a.application_id;"},
]

# ---------------------------------------------------------------------------
# 6. КРИТЕРИИ ПРОБНОГО ЭКЗАМЕНА (100 баллов)
# ---------------------------------------------------------------------------
CRITERIA = [
    ("Модуль 1. Разработка подсистемы безопасности информационной системы — 18", [
        ("Регистрация: серверная валидация логина, пароля, ФИО, телефона, email", 4),
        ("Уникальный логин, пароль хранится только в виде хеша", 3),
        ("Вход/выход, сессия, понятные сообщения об ошибках", 3),
        ("Роли «пользователь/администратор», защита админ-маршрутов", 3),
        ("Защита от SQL-инъекций, XSS и CSRF", 3),
        ("Доступ администратора Admin/KorokNET, запрет прямого URL", 2),
    ]),
    ("Модуль 1. Разработка модулей информационной системы — 4", [
        ("Создание заявки: курс, дата, способ оплаты, запись в БД", 2),
        ("Статусы заявок и отзыв только после завершения курса", 2),
    ]),
    ("Модуль 1. Использование современных средств поиска и анализа информации — 3", [
        ("ER-диаграмма и schema.sql с демо-данными", 1),
        ("Git-репозиторий, осмысленные коммиты, README", 1),
        ("Фреймворк/библиотеки и аккуратная структура проекта", 1),
    ]),
    ("Модуль 2. Разработка дизайн-концепций веб-приложений — 13", [
        ("Корпоративный стиль: палитра, шрифты, логотип, единые отступы", 4),
        ("Компоненты: кнопки, поля, карточки, бейджи, состояния", 3),
        ("Адаптив 390×844, mobile-first, без горизонтального скролла", 3),
        ("Слайдер: 4 изображения, 3 секунды, кнопки назад/вперёд", 3),
    ]),
    ("Модуль 2. Формирование требований к дизайну веб-приложений — 4", [
        ("Анализ целевой аудитории и пользовательских сценариев", 2),
        ("Прототип/структура всех страниц и переходов", 2),
    ]),
    ("Модуль 2. Разработка дизайна с учётом современных тенденций — 8", [
        ("Flexbox/Grid, типографика, сетка и spacing", 3),
        ("Анимации и микроанимации, не мешающие работе", 3),
        ("Доступность: контраст, alt, focus-visible, aria", 2),
    ]),
    ("Модуль 3. Разработка веб-приложения в соответствии с техническим заданием — 14", [
        ("Полный стек: frontend + backend + БД", 4),
        ("Все сценарии: регистрация, вход, заявки, админка", 4),
        ("Корректная работа на мобильном 390×844", 2),
        ("Валидация, обработка ошибок, пустые состояния", 2),
        ("Структура проекта и коммиты по модулям", 2),
    ]),
    ("Модуль 3. Разработка интерфейса пользователя — 11", [
        ("Навигация, формы, обратная связь, сообщения", 3),
        ("Админ-панель: фильтр, поиск, сортировка, пагинация", 3),
        ("Смена статусов «Идет обучение» / «Обучение завершено», подтверждения", 2),
        ("Переходы и анимации, аккуратный UX", 2),
        ("Интегрированные адаптив и слайдер", 1),
    ]),
    ("Вариативная часть (тренировочная) — 25", [
        ("JSON API / AJAX-запрос без перезагрузки страницы", 5),
        ("Тесты: регистрация, вход, заявка, запрет админки", 5),
        ("Руководство пользователя 1–2 стр. с 4+ скриншотами", 5),
        ("Запуск/деплой, .env, резервная копия БД", 5),
        ("Оптимизация: индексы, отсутствие N+1, сжатие, кэш", 5),
    ]),
]

# ---------------------------------------------------------------------------
# 7. ШПАРГАЛКИ
# ---------------------------------------------------------------------------
SNIPPETS = [
    ("HTML: каркас страницы", """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Корочки.есть — онлайн-курсы</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
  <header class="site-header">
    <a class="logo" href="{{ url_for('index') }}">Корочки.есть</a>
    <nav class="main-nav">
      <a href="{{ url_for('index') }}">Курсы</a>
      {% if session.user_id %}
        <a href="{{ url_for('dashboard') }}">Мои заявки</a>
        <a href="{{ url_for('logout') }}">Выйти</a>
      {% else %}
        <a href="{{ url_for('login') }}">Вход</a>
        <a href="{{ url_for('register') }}">Регистрация</a>
      {% endif %}
    </nav>
  </header>
  <main class="container">
    {% block content %}{% endblock %}
  </main>
</body>
</html>"""),
    ("HTML: форма регистрации", """<form method="post" class="form" novalidate>
  <input type="hidden" name="csrf_token" value="{{ csrf_token }}">

  <label for="login">Логин</label>
  <input id="login" name="login" value="{{ form.login or '' }}"
         required minlength="6" pattern="[A-Za-z0-9]{6,}">
  {% if errors.login %}<p class="field-error">{{ errors.login }}</p>{% endif %}

  <label for="password">Пароль</label>
  <input id="password" name="password" type="password"
         required minlength="8" autocomplete="new-password">
  {% if errors.password %}<p class="field-error">{{ errors.password }}</p>{% endif %}

  <label for="full_name">ФИО</label>
  <input id="full_name" name="full_name" value="{{ form.full_name or '' }}" required>

  <label for="phone">Телефон</label>
  <input id="phone" name="phone" type="tel"
         placeholder="8(921)111-11-11" value="{{ form.phone or '' }}" required>

  <label for="email">E-mail</label>
  <input id="email" name="email" type="email" value="{{ form.email or '' }}" required>

  <button class="btn btn--primary" type="submit">Зарегистрироваться</button>
</form>"""),
    ("CSS: переменные и адаптив", """:root {
  --brand: #2563eb;
  --brand-dark: #1e40af;
  --bg: #f8fafc;
  --card: #ffffff;
  --ink: #0f172a;
  --muted: #64748b;
  --danger: #dc2626;
  --radius: 14px;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: system-ui, "Segoe UI", sans-serif;
  background: var(--bg);
  color: var(--ink);
  line-height: 1.5;
}
.container { width: min(100% - 32px, 1120px); margin-inline: auto; }

@media (min-width: 640px) {
  .course-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (min-width: 960px) {
  .course-grid { grid-template-columns: repeat(3, 1fr); }
}"""),
    ("CSS: карточки и кнопки", """.course-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}
.course-card {
  background: var(--card);
  border: 1px solid #e2e8f0;
  border-radius: var(--radius);
  padding: 20px;
  transition: transform .2s ease, box-shadow .2s ease;
}
.course-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(15, 23, 42, .12);
}
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  padding: 10px 18px;
  border: 0;
  border-radius: 10px;
  cursor: pointer;
}
.btn--primary { background: var(--brand); color: #fff; }
.btn--primary:hover { background: var(--brand-dark); }
.btn:focus-visible { outline: 3px solid #93c5fd; outline-offset: 2px; }"""),
    ("JavaScript: валидация формы", """const form = document.querySelector('#register-form');
const rules = {
  login: [/^[A-Za-z0-9]{6,}$/, 'Логин: латиница и цифры, минимум 6 символов'],
  password: [/^.{8,}$/, 'Пароль: минимум 8 символов'],
  full_name: [/^[А-Яа-яЁё\\s]+$/, 'ФИО: только кириллица и пробелы'],
  phone: [/^8\\(\\d{3}\\)\\d{3}-\\d{2}-\\d{2}$/, 'Телефон: 8(XXX)XXX-XX-XX'],
  email: [/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/, 'Введите корректный email'],
};

form.addEventListener('submit', (event) => {
  let valid = true;
  for (const [name, [re, message]] of Object.entries(rules)) {
    const input = form.elements[name];
    const box = document.querySelector(`#${name}-error`);
    const ok = re.test(input.value.trim());
    box.textContent = ok ? '' : message;
    input.classList.toggle('is-error', !ok);
    input.setAttribute('aria-invalid', String(!ok));
    if (!ok) valid = false;
  }
  if (!valid) event.preventDefault();
});"""),
    ("JavaScript: слайдер 4 / 3 секунды", """const root = document.querySelector('[data-slider]');
const img = root.querySelector('.slider__img');
const slides = [1, 2, 3, 4].map(n => `/static/img/slide-${n}.svg`);
let index = 0;
let timer = null;

function show(i) {
  index = (i + slides.length) % slides.length;
  img.src = slides[index];
  img.alt = `Курс ${index + 1}`;
}
function start() {
  stop();
  timer = setInterval(() => show(index + 1), 3000);
}
function stop() {
  if (timer) clearInterval(timer);
  timer = null;
}
root.querySelector('[data-prev]').addEventListener('click', () => { show(index - 1); start(); });
root.querySelector('[data-next]').addEventListener('click', () => { show(index + 1); start(); });
root.addEventListener('mouseenter', stop);
root.addEventListener('mouseleave', start);
start();"""),
    ("Flask: маршруты и Jinja", """from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-me'

@app.get('/')
def index():
    courses = get_courses()
    return render_template('index.html', courses=courses)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        errors = validate_registration(request.form)
        if not errors:
            create_user(request.form)
            flash('Регистрация успешна, войдите', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', errors=errors, form=request.form)
    return render_template('register.html', errors={}, form={})

@app.get('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', applications=get_user_applications(session['user_id']))

if __name__ == '__main__':
    app.run(debug=True)"""),
    ("Flask: сессия, роли, CSRF", """from functools import wraps
from flask import session, redirect, url_for, flash, abort, request
import secrets

def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Сначала войдите в систему', 'error')
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapper

def admin_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if session.get('role_id') != 1:
            abort(403)
        return view(*args, **kwargs)
    return wrapper

@app.before_request
def csrf_protect():
    if request.method == 'POST':
        token = session.get('csrf_token')
        if not token or token != request.form.get('csrf_token'):
            abort(400, 'CSRF token mismatch')

def make_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    return session['csrf_token']"""),
    ("SQLite: параметризованные запросы", """import sqlite3

conn = sqlite3.connect('instance/korochki.db')
conn.row_factory = sqlite3.Row
conn.execute('PRAGMA foreign_keys = ON')

# Чтение
rows = conn.execute(
    'SELECT application_id, course_id, start_date, status_id '
    'FROM applications WHERE user_id = ? ORDER BY created_at DESC',
    (user_id,)
).fetchall()

# Запись
cur = conn.execute(
    'INSERT INTO applications (user_id, course_id, start_date, payment_method, status_id) '
    'VALUES (?, ?, ?, ?, 1)',
    (user_id, course_id, start_date, payment_method)
)
conn.commit()
application_id = cur.lastrowid

# Изменение статуса (только администратор)
conn.execute(
    'UPDATE applications SET status_id = ?, cancel_reason = ? WHERE application_id = ?',
    (status_id, cancel_reason, application_id)
)
conn.commit()"""),
    ("БД: схема «Корочки.есть»", """CREATE TABLE users (
    user_id       INTEGER PRIMARY KEY,
    login         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    full_name     TEXT NOT NULL,
    phone         TEXT NOT NULL,
    email         TEXT NOT NULL UNIQUE,
    role_id       INTEGER NOT NULL REFERENCES roles(role_id),
    created_at    TEXT NOT NULL DEFAULT (date('now'))
);

CREATE TABLE applications (
    application_id INTEGER PRIMARY KEY,
    user_id        INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    course_id      INTEGER NOT NULL REFERENCES courses(course_id) ON DELETE RESTRICT,
    start_date     TEXT NOT NULL,
    payment_method TEXT NOT NULL CHECK (payment_method IN ('cash', 'phone_transfer')),
    status_id      INTEGER NOT NULL REFERENCES application_statuses(status_id),
    cancel_reason  TEXT,
    created_at     TEXT NOT NULL DEFAULT (date('now'))
);

CREATE TABLE reviews (
    review_id      INTEGER PRIMARY KEY,
    application_id INTEGER NOT NULL UNIQUE
                   REFERENCES applications(application_id) ON DELETE CASCADE,
    user_id        INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    rating         INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review_text    TEXT
);"""),
    ("Админка: фильтр и пагинация", """@app.get('/admin')
@admin_required
def admin():
    status_id = request.args.get('status', type=int)
    search = (request.args.get('q') or '').strip()
    page = max(request.args.get('page', 1, type=int), 1)
    per_page = 8

    where, params = [], []
    if status_id:
        where.append('a.status_id = ?')
        params.append(status_id)
    if search:
        where.append('(u.full_name LIKE ? OR c.title LIKE ?)')
        params += [f'%{search}%', f'%{search}%']
    clause = ('WHERE ' + ' AND '.join(where)) if where else ''

    total = conn.execute(
        f'SELECT COUNT(*) FROM applications a '
        f'JOIN users u ON u.user_id = a.user_id '
        f'JOIN courses c ON c.course_id = a.course_id {clause}', params
    ).fetchone()[0]

    rows = conn.execute(
        f'SELECT a.*, u.full_name, c.title, s.status_name '
        f'FROM applications a '
        f'JOIN users u ON u.user_id = a.user_id '
        f'JOIN courses c ON c.course_id = a.course_id '
        f'JOIN application_statuses s ON s.status_id = a.status_id '
        f'{clause} ORDER BY a.created_at DESC LIMIT ? OFFSET ?',
        params + [per_page, (page - 1) * per_page]
    ).fetchall()

    return render_template('admin.html', rows=rows, total=total,
                           page=page, per_page=per_page,
                           statuses=get_statuses())"""),
    ("Git: сдача работы", """git init
git add .
git commit -m "feat: каркас проекта, схема БД и регистрация"

git branch -M main
git remote add origin https://github.com/user/demoexam-web.git
git push -u origin main

# после каждого модуля
git add .
git commit -m "feat: заявки, статусы и админ-панель"
git push

# .gitignore
venv/
__pycache__/
*.pyc
*.db
.env
.DS_Store"""),
    ("Руководство пользователя: структура", """# Руководство пользователя «Корочки.есть»

## 1. Назначение
Портал записи на онлайн-курсы дополнительного профессионального образования.

## 2. Регистрация
Откройте «Регистрация», заполните логин, пароль, ФИО, телефон, email.
[Скриншот 1: форма регистрации]

## 3. Вход
Введите логин и пароль. Ошибки выводятся на форме.
[Скриншот 2: вход]

## 4. Новая заявка
Выберите курс, дату начала и способ оплаты, нажмите «Отправить».
[Скриншот 3: форма заявки]

## 5. Мои заявки
История заявок и статусы. После завершения курса можно оставить отзыв.
[Скриншот 4: личный кабинет]

## 6. Администратор
Вход Admin / KorokNET. Фильтр, поиск, пагинация, смена статусов.
[Скриншот 5: админ-панель]
"""),
]
