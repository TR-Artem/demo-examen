# Git, README, документы

## Первый репозиторий

```bash
git init
git add .
git commit -m "feat: каркас проекта и схема БД"
git branch -M main
git remote add origin <url>
git push -u origin main
```

## После каждого модуля

```bash
git status
git add .
git commit -m "feat: заявки, статусы и админ-панель"
git push
```

## .gitignore

```gitignore
venv/
__pycache__/
*.pyc
*.db
.env
.DS_Store
```

## Что должно быть в репозитории

- исходники **папкой**, не архивом;
- `schema.sql` с DDL и демо-данными;
- `README.md`;
- ER-диаграмма (PDF/PNG);
- руководство пользователя;
- скриншоты;
- осмысленные коммиты в каждом модуле.

## README.md — шаблон

```markdown
# «Корочки.есть»

Портал онлайн-курсов. ДЭ 09.02.07, веб-квалификация.

## Стек
Python 3.10+, Flask, SQLite, Jinja2, HTML/CSS/JS.

## Запуск
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

## Демо-доступ
- пользователь: demo01 / password123
- администратор: Admin / KorokNET

## Структура
app.py, db.py, models.py, security.py, schema.sql, templates/, static/

## База данных
6 таблиц: roles, users, courses, application_statuses, applications, reviews.

## Функционал
Регистрация, вход, заявки, статусы, отзывы, админка, фильтры, пагинация.

## Скриншоты
(вставить 4–6 изображений)
```

## Руководство пользователя

1–2 страницы, 4+ скриншота:

1. Назначение системы.
2. Регистрация.
3. Вход.
4. Новая заявка.
5. Мои заявки и отзыв.
6. Админ-панель.

Формат: `Руководство_пользователя.docx` или `.pdf`.

## Проверка перед сдачей

```bash
git status                 # нет мусора
git log --oneline          # коммиты по модулям
python -m unittest discover -s tests -v
```

- нет `venv/`, `*.db`, `.env`;
- README открывается и инструкция работает;
- все ссылки и скриншоты на месте.
