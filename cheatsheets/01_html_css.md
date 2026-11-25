# HTML и CSS — шпаргалка

## Каркас страницы

```html
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
  <main class="container">...</main>
  <footer>...</footer>
  <script src="/static/js/app.js" defer></script>
</body>
</html>
```

## Семантика

| Тег | Когда |
|---|---|
| `header` | шапка страницы/блока |
| `nav` | навигация |
| `main` | основное содержимое, один на страницу |
| `section` | смысловой раздел с заголовком |
| `article` | самостоятельная карточка/запись |
| `aside` | боковая заметка |
| `footer` | подвал |

## Формы

```html
<form method="post" novalidate>
  <input type="hidden" name="csrf_token" value="{{ csrf_token }}">

  <label for="login">Логин</label>
  <input id="login" name="login" required minlength="6"
         pattern="[A-Za-z0-9]{6,}" autocomplete="username">

  <label for="phone">Телефон</label>
  <input id="phone" name="phone" type="tel" placeholder="8(921)111-11-11">

  <label for="email">E-mail</label>
  <input id="email" name="email" type="email" required>

  <button type="submit">Отправить</button>
</form>
```

- `label for` = `input id`;
- `type="email"`, `type="tel"`, `type="date"`;
- `required`, `minlength`, `pattern`;
- ошибки — текстом под полем, не одним `alert`.

## CSS: переменные и сброс

```css
:root {
  --brand: #2563eb;
  --bg: #f8fafc;
  --ink: #0f172a;
  --muted: #64748b;
  --radius: 14px;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: system-ui, "Segoe UI", sans-serif;
  line-height: 1.5;
  color: var(--ink);
  background: var(--bg);
}
img { max-width: 100%; height: auto; display: block; }
```

## Flexbox

```css
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}
```

- `justify-content` — главная ось;
- `align-items` — поперечная;
- `flex-wrap: wrap` — перенос;
- `flex: 1` — занять свободное место.

## Grid

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px;
}
```

## Адаптив

```css
/* mobile-first: база — мобильный */
.grid { grid-template-columns: 1fr; }

@media (min-width: 640px) {
  .grid { grid-template-columns: repeat(2, 1fr); }
}
@media (min-width: 960px) {
  .grid { grid-template-columns: repeat(3, 1fr); }
}
```

Экзаменационный размер — **390×844**. Проверяй в DevTools.

## Состояния и доступность

```css
.btn:hover { background: var(--brand-dark); }
.btn:focus-visible { outline: 3px solid #93c5fd; outline-offset: 2px; }
.field input[aria-invalid="true"] { border-color: #dc2626; }
```

- контраст текста ≥ 4.5:1;
- зона нажатия ≥ 44×44 px;
- `alt` у изображений;
- `aria-label` у кнопок-иконок;
- не отключай `outline` без замены.
