# JavaScript: DOM, события, валидация, слайдер

## Поиск и изменение элементов

```js
const form = document.querySelector('#register-form');
const login = document.querySelector('#login');
const error = document.querySelector('#login-error');

login.value = 'demo01';
error.textContent = 'Логин занят';
document.body.classList.toggle('menu-open');
```

## События

```js
form.addEventListener('submit', (event) => {
  if (!form.checkValidity()) {
    event.preventDefault();
    return;
  }
});

button.addEventListener('click', () => { /* ... */ });
input.addEventListener('input', () => { /* ... */ });
input.addEventListener('blur', () => { /* ... */ });
```

## Валидация

```js
const RULES = {
  login: [/^[A-Za-z0-9]{6,}$/, 'Логин: латиница и цифры, 6+'],
  password: [/^.{8,}$/, 'Пароль: 8+ символов'],
  full_name: [/^[А-Яа-яЁё\s-]+$/, 'ФИО: кириллица, пробелы, дефис'],
  phone: [/^8\(\d{3}\)\d{3}-\d{2}-\d{2}$/, 'Телефон: 8(XXX)XXX-XX-XX'],
  email: [/^[^\s@]+@[^\s@]+\.[^\s@]+$/, 'Некорректный email'],
};

form.addEventListener('submit', (event) => {
  let ok = true;
  for (const [name, [re, message]] of Object.entries(RULES)) {
    const field = form.elements[name];
    const box = document.querySelector(`#${name}-error`);
    const valid = re.test(field.value.trim());
    box.textContent = valid ? '' : message;
    field.classList.toggle('is-error', !valid);
    field.setAttribute('aria-invalid', String(!valid));
    if (!valid) ok = false;
  }
  if (!ok) event.preventDefault();
});
```

Серверная валидация обязательна: клиентскую легко обойти.

## Слайдер 4 / 3 секунды

```js
const root = document.querySelector('[data-slider]');
const img = root.querySelector('.slider__img');
const slides = [1, 2, 3, 4].map(n => `/static/img/slide-${n}.svg`);
let index = 0;
let timer = null;

function show(i) {
  index = (i + slides.length) % slides.length;
  img.src = slides[index];
  img.alt = `Слайд ${index + 1}`;
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
start();
```

## Анимации

```css
.reveal { animation: fade-up .5s ease both; }
@keyframes fade-up {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: .001ms !important; transition-duration: .001ms !important; }
}
```

## Полезно

```js
setTimeout(fn, 300);           // один раз
setInterval(fn, 3000);         // каждые 3 секунды
clearInterval(timer);
localStorage.setItem('key', 'value');
const data = await (await fetch('/api/applications')).json();
```
