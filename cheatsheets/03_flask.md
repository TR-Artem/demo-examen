# Flask: маршруты, Jinja2, формы, сессии

## Запуск

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install flask
pip freeze > requirements.txt
python app.py
```

## Минимум

```python
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-me'

@app.get('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
```

## Маршруты и методы

```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login', '').strip()
        password = request.form.get('password', '')
        # валидация и запись
        flash('Готово', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')
```

## Jinja2

```html
{% extends 'base.html' %}
{% block content %}
  <h1>{{ title }}</h1>
  {% for course in courses %}
    <article class="card">
      <h2>{{ course.title }}</h2>
      <p>{{ course.description }}</p>
    </article>
  {% endfor %}
{% endblock %}
```

- `{{ }}` — вывод, HTML экранируется;
- `{% %}` — логика;
- `{% extends %}` / `{% block %}` — наследование;
- `url_for('static', filename='css/style.css')` — статика;
- `|date_ru`, `|money` — свои фильтры.

## Сессия и роли

```python
from functools import wraps
from flask import session, redirect, url_for, flash, abort

def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Сначала войдите', 'error')
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

session['user_id'] = user['user_id']
session.clear()      # выход
```

## Flash и PRG

```python
flash('Заявка создана', 'success')
return redirect(url_for('dashboard'))   # Post/Redirect/Get
```

```html
{% with messages = get_flashed_messages(with_categories=true) %}
  {% for category, message in messages %}
    <div class="alert alert--{{ category }}">{{ message }}</div>
  {% endfor %}
{% endwith %}
```

## Ошибки

```python
@app.errorhandler(404)
def not_found(_):
    return render_template('error.html', code=404, message='Не найдено'), 404
```

## Структура

```
app.py
db.py
models.py
security.py
schema.sql
seed.py
templates/
static/
tests/
```
