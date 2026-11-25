# Регистрация, вход, роли, безопасность

## Хеширование пароля

```python
from werkzeug.security import generate_password_hash, check_password_hash

password_hash = generate_password_hash(password)
ok = check_password_hash(user['password_hash'], password)
```

Пароль в открытом виде не хранить никогда.

## Валидация на сервере

```python
LOGIN_RE = r'^[A-Za-z0-9]{6,}$'
FIO_RE = r'^[А-Яа-яЁё\s-]+$'
PHONE_RE = r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$'
EMAIL_RE = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
```

Проверяй:

- логин — формат + уникальность;
- пароль — 8+;
- ФИО — кириллица, пробелы, дефис;
- телефон — точный формат;
- email — формат + уникальность;
- все поля обязательны.

## Сессия

```python
session.clear()
session['user_id'] = user['user_id']
session['role_id'] = user['role_id']
```

```python
app.config.update(
    SECRET_KEY='...',
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)
```

## Роли

```python
def admin_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if session.get('role_id') != 1:
            abort(403)
        return view(*args, **kwargs)
    return wrapper
```

Админ: `Admin / KorokNET`. Прямой заход на `/admin` без прав — 403.

## SQL-инъекции

```python
# плохо
cur.execute(f"SELECT * FROM users WHERE login = '{login}'")

# хорошо
cur.execute('SELECT * FROM users WHERE login = ?', (login,))
```

## XSS

Jinja2 экранирует `{{ }}` автоматически. Не используй `|safe`
для пользовательских данных.

## CSRF

```python
import secrets

def csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    return session['csrf_token']

@app.before_request
def csrf_protect():
    if request.method == 'POST':
        sent = request.form.get('csrf_token', '')
        if not secrets.compare_digest(session.get('csrf_token', ''), sent):
            abort(400)
```

```html
<input type="hidden" name="csrf_token" value="{{ csrf_token }}">
```

## Ошибки

- «Неверный логин или пароль» — не раскрывай, что именно неверно;
- `debug=False` на защите/деплое;
- не показывай traceback и пути к файлам;
- 404/403/500 — красивые страницы.

## Чек-лист безопасности

- [ ] пароли — хеш;
- [ ] логин и email уникальны;
- [ ] все POST защищены CSRF-токеном;
- [ ] SQL — только параметры;
- [ ] `/admin` проверяет роль;
- [ ] cookie HttpOnly + SameSite;
- [ ] нет секретов в git (`.env` в `.gitignore`).
