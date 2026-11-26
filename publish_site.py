# -*- coding: utf-8 -*-
"""
Публикация сайта на GitHub Pages: главная-лендинг + веб-тренажёр.

Что делает:
  1. docs/index.html  — самодостаточный тренажёр (из DemoExam-mobile.html);
  2. docs/DemoExam-09-02-07.apk — APK для скачивания с сайта;
  3. index.html       — главная страница в стиле страницы курса Stepik;
  4. .nojekyll        — чтобы GitHub Pages не обрабатывал файлы через Jekyll.

После запуска:
  git add index.html .nojekyll docs publish_site.py
  git commit -m "Update website"
  git push
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
APK = ROOT / "DemoExam-09-02-07.apk"
HTML = ROOT / "DemoExam-mobile.html"
HTML_PROG = ROOT / "DemoExam-mobile-programmer.html"
HTML_IS = ROOT / "DemoExam-mobile-is.html"

COURSE_CHOOSER = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#222222">
<title>ДЭ 09.02.07-2027 — выбор курса</title>
<style>
  :root{
    --brand:#4485ed; --brand-d:#2f6fd0; --green:#54ad54; --green-d:#469a46;
    --topbar:#222; --page:#f3f4f6; --card:#fff; --ink:#222; --muted:#6b7280;
    --line:#e5e7eb; --soft:#eef4ff; --header-h:56px;
  }
  *{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
  html,body{margin:0;padding:0}
  body{background:var(--page);color:var(--ink);
       font:15px/1.6 Roboto,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}
  a{color:var(--brand)}
  .wrap{max-width:1080px;margin:0 auto;padding:0 clamp(14px,4vw,20px)}
  .topbar{background:var(--topbar);color:#fff;min-height:var(--header-h);
          display:flex;align-items:center;position:sticky;top:0;z-index:60}
  .topbar .wrap{display:flex;align-items:center;gap:18px;width:100%}
  .brand{display:flex;align-items:center;gap:8px;text-decoration:none;color:#fff}
  .brand-mark{width:30px;height:30px;border-radius:7px;background:var(--brand);
              display:grid;place-items:center;font-size:11px;font-weight:800}
  .brand-text{font-size:20px;font-weight:700;letter-spacing:-.5px}
  .brand-text span{color:#8ab4f8;font-weight:400}
  .topbar nav{margin-left:auto;display:flex;gap:18px;flex-wrap:wrap}
  .topbar nav a{color:#cfd8e3;text-decoration:none;font-size:14px}
  .topbar nav a:hover{color:#fff}
  main{padding:34px 0 60px}
  .eyebrow{font-size:11.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
           color:var(--brand);margin:0 0 8px}
  h1{font-size:clamp(1.7rem,4vw,2.3rem);line-height:1.15;margin:0 0 10px;letter-spacing:-.5px}
  .lead{font-size:16px;color:#555;max-width:760px;margin:0 0 26px}
  .grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
  .course-card{background:var(--card);border:1px solid var(--line);border-radius:14px;
               padding:22px 20px;display:flex;flex-direction:column;
               box-shadow:0 4px 16px rgba(15,23,42,.05)}
  .course-card--is{border-top:4px solid #0ea5e9}
  .course-card--web{border-top:4px solid var(--green)}
  .course-card--prog{border-top:4px solid #f59e0b}
  .code{font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;
        color:var(--muted);margin-bottom:8px}
  .course-card h2{margin:0 0 8px;font-size:1.2rem;line-height:1.25}
  .course-card p{margin:0 0 14px;color:#555;font-size:.92rem}
  .stats{list-style:none;margin:0 0 18px;padding:0;display:grid;gap:6px}
  .stats li{font-size:.86rem;color:#374151;display:flex;gap:8px;align-items:flex-start}
  .stats li:before{content:"✓";color:var(--green);font-weight:800}
  .actions{margin-top:auto;display:grid;gap:8px}
  .btn{display:inline-flex;align-items:center;justify-content:center;text-align:center;
       text-decoration:none;min-height:44px;padding:10px 16px;border-radius:8px;
       font-size:14px;font-weight:600;border:1px solid transparent}
  .btn.primary{background:var(--green);color:#fff}
  .btn.primary:hover{background:var(--green-d)}
  .btn.ghost{background:#fff;border-color:var(--line);color:var(--ink)}
  .btn.ghost:hover{background:#f7f8fa}
  .note{margin-top:24px;padding:16px 18px;border-radius:12px;background:#fff;
        border:1px solid var(--line);font-size:.9rem;color:#555}
  .note b{color:var(--ink)}
  footer{padding:24px 0;color:var(--muted);font-size:13px;text-align:center}
  @media (max-width:900px){.grid{grid-template-columns:1fr 1fr}}
  @media (max-width:680px){
    .grid{grid-template-columns:1fr}
    main{padding:22px 0 40px}
    .topbar nav{gap:12px}
    .course-card{padding:18px 16px}
  }
</style>
</head>
<body>
<header class="topbar">
  <div class="wrap">
    <a class="brand" href="../index.html" aria-label="ДЭ.Курс">
      <span class="brand-mark">ДЭ</span><span class="brand-text">.Курс</span>
    </a>
    <nav>
      <a href="../index.html">О курсе</a>
      <a href="https://github.com/TR-Artem/demo-examen" target="_blank" rel="noopener">Материалы</a>
    </nav>
  </div>
</header>
<main class="wrap">
  <p class="eyebrow">Демонстрационный экзамен · 09.02.07 · 2027</p>
  <h1>Выберите курс подготовки</h1>
  <p class="lead">Три квалификации в одном тренажёре. Все курсы открываются прямо на сайте:
    теория, тесты с практическими заданиями, SQL-практика и пробный экзамен.</p>

  <div class="grid">
    <article class="course-card course-card--web">
      <div class="code">09.02.07-3</div>
      <h2>Веб и мультимедиа</h2>
      <p>Flask, SQLite, HTML/CSS/JS. Три модуля экзамена и полный стек веб-разработки.</p>
      <ul class="stats">
        <li>53 вопроса и 14 практик с кодом</li>
        <li>19 SQL-задач с автопроверкой</li>
        <li>Пробник на 100 баллов · 4 часа</li>
      </ul>
      <div class="actions">
        <a class="btn primary" href="DemoExam-mobile.html">Открыть онлайн</a>
        <a class="btn ghost" href="DemoExam-mobile.html" download>Скачать офлайн-HTML</a>
      </div>
    </article>

    <article class="course-card course-card--prog">
      <div class="code">09.02.07-2</div>
      <h2>Программист</h2>
      <p>Python, SQLite и tkinter на примере магазина обуви. Четыре модуля КОД 2026.</p>
      <ul class="stats">
        <li>41 вопрос и 11 практик с кодом</li>
        <li>19 SQL-задач и CRUD-сценарии</li>
        <li>Пробник и чек-лист на 100 баллов</li>
      </ul>
      <div class="actions">
        <a class="btn primary" href="DemoExam-mobile-programmer.html">Открыть онлайн</a>
        <a class="btn ghost" href="DemoExam-mobile-programmer.html" download>Скачать офлайн-HTML</a>
      </div>
    </article>

    <article class="course-card course-card--is">
      <div class="code">09.02.07-5</div>
      <h2>Информационные системы</h2>
      <p>ER, SQL, авторизация, API, Postman и документация. Шесть заданий КИМ 2027.</p>
      <ul class="stats">
        <li>39 вопросов и 15 практик с кодом</li>
        <li>19 SQL-задач: себестоимость и заказы</li>
        <li>Импорт JSON, API и тест-кейсы</li>
      </ul>
      <div class="actions">
        <a class="btn primary" href="DemoExam-mobile-is.html">Открыть онлайн</a>
        <a class="btn ghost" href="DemoExam-mobile-is.html" download>Скачать офлайн-HTML</a>
      </div>
    </article>
  </div>

  <div class="note"><b>Как это работает.</b> Онлайн-версия открывается в браузере и сохраняет
    прогресс в localStorage. Офлайн-HTML можно скачать и заниматься без интернета.
    Для курса «Информационные системы» доступны все шесть экзаменационных заданий:
    ER-диаграмма, импорт JSON, SQL-стоимость заказа, вход с капчей и блокировкой,
    API с маскированием данных, Postman и проектная документация.</div>
</main>
<footer>ДЭ.Курс · подготовка к демонстрационному экзамену 09.02.07</footer>
</body>
</html>
"""

SWITCHER = """
<div class="course-switch" role="navigation" aria-label="Выбор курса">
  <a href="./">← Все курсы</a>
  <a href="DemoExam-mobile.html">Веб</a>
  <a href="DemoExam-mobile-programmer.html">Программист</a>
  <a href="DemoExam-mobile-is.html">ИС</a>
</div>
<style>
  .course-switch{
    position:fixed;right:12px;bottom:12px;z-index:100;
    display:flex;flex-wrap:wrap;gap:2px;align-items:center;
    padding:4px;border-radius:10px;background:rgba(34,34,34,.92);
    box-shadow:0 6px 20px rgba(0,0,0,.25);
    font:600 12px -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  }
  .course-switch a{color:#dbeafe;text-decoration:none;padding:5px 8px;border-radius:7px}
  .course-switch a:hover{background:rgba(255,255,255,.1);color:#fff}
  .course-switch a:first-child{color:#93c5fd}
  @media (max-width:560px){
    .course-switch{right:8px;bottom:8px;font-size:11px;max-width:calc(100vw - 16px)}
    .course-switch a{padding:4px 6px}
  }
</style>
"""


REPO = "https://github.com/TR-Artem/demo-examen"
SITE = "https://tr-artem.github.io/demo-examen/"

LANDING = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#222222">
<title>ДЭ 09.02.07-3-2027 «Разработчик веб и мультимедийных приложений» — курс</title>
<style>
  :root{
    --brand:#4485ed; --brand-d:#2f6fd0; --green:#54ad54; --green-d:#469a46;
    --topbar:#222; --page:#f3f4f6; --card:#fff; --ink:#222; --muted:#777;
    --line:#e6e8eb; --soft:#eef4ff; --code:#1e1e1e; --header-h:56px;
  }
  *{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
  html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
  html,body{margin:0;padding:0}
  body{background:var(--page);color:var(--ink);
       font:15px/1.6 Roboto,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;
       overflow-x:hidden}
  a{color:var(--brand)}
  .wrap{max-width:1080px;margin:0 auto;padding:0 clamp(14px,4vw,20px)}
  code{background:#eceff3;padding:1px 5px;border-radius:4px;font-size:.9em;overflow-wrap:anywhere}

  /* шапка */
  .topbar{background:var(--topbar);color:#fff;min-height:var(--header-h);
          display:flex;align-items:center;position:sticky;top:0;z-index:60;
          box-shadow:0 1px 0 rgba(255,255,255,.06)}
  .topbar .wrap{display:flex;align-items:center;gap:18px;width:100%}
  .brand{display:flex;align-items:center;gap:8px;text-decoration:none;color:#fff;flex:0 0 auto;min-height:44px}
  .brand-mark{width:30px;height:30px;border-radius:7px;background:var(--brand);
              display:grid;place-items:center;font-size:11px;font-weight:800}
  .brand-text{font-size:20px;font-weight:700;letter-spacing:-.5px}
  .brand-text span{color:#8ab4f8;font-weight:400}
  .topnav{display:flex;gap:20px;flex:1}
  .topnav a{display:inline-flex;align-items:center;min-height:44px;color:#bdbdbd;text-decoration:none;font-size:14px}
  .topnav a:hover{color:#fff}
  .topnav a.nav-cta{display:none}
  .login{border:1px solid rgba(255,255,255,.28);color:#fff;text-decoration:none;
         display:inline-flex;align-items:center;min-height:38px;
         padding:7px 16px;border-radius:6px;font-size:14px;white-space:nowrap}
  .login:hover{background:rgba(255,255,255,.08)}
  .menu-btn{display:none;width:42px;height:42px;padding:0;border-radius:8px;
            border:1px solid #3a3a3a;background:#2c2c2c;color:#fff;font-size:18px;
            line-height:1;cursor:pointer;place-items:center}
  .menu-btn:active{background:#3a3a3a}
  .menu-btn[aria-expanded="true"]{background:#3a3a3a}
  @media (max-width:760px){
    .brand-text{font-size:18px}
    .login{display:none}
    .menu-btn{display:grid;margin-left:auto;flex:0 0 auto}
    body.nav-open{overflow:hidden}
    .topnav{
      position:absolute;top:100%;left:0;right:0;display:grid;gap:2px;
      padding:8px 14px calc(12px + env(safe-area-inset-bottom));
      background:var(--topbar);border-top:1px solid #333;
      box-shadow:0 14px 28px rgba(0,0,0,.28);
      opacity:0;visibility:hidden;transform:translateY(-6px);pointer-events:none;
      transition:opacity .16s ease,transform .16s ease,visibility .16s;
    }
    .topnav a{min-height:48px;padding:0 12px;border-radius:8px;font-size:15px;color:#e3e3e3}
    .topnav a:hover{background:rgba(255,255,255,.07);color:#fff}
    .topnav a.nav-cta{display:inline-flex;justify-content:center;margin-top:6px;padding:0 14px;
                      background:var(--green);color:#fff;font-weight:600}
    .topnav a.nav-cta:hover{background:var(--green-d)}
    body.nav-open .topnav{opacity:1;visibility:visible;transform:none;pointer-events:auto}
  }

  main{padding:22px 0 60px}
  .crumbs{font-size:12.5px;color:var(--muted);margin-bottom:18px}
  .crumbs a{color:var(--muted);text-decoration:none}
  .crumbs a:hover{color:var(--brand)}
  .crumbs span{margin:0 7px;color:#bbb}

  /* обложка курса */
  .hero{display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:28px;align-items:start;margin-bottom:34px}
  .eyebrow{font-size:11.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--brand);margin-bottom:10px}
  h1{font-size:clamp(1.45rem,5.8vw,2.125rem);line-height:1.18;margin:0 0 14px;letter-spacing:-.4px;overflow-wrap:break-word}
  .lead{font-size:clamp(14.5px,3.7vw,16px);color:#555;margin:0 0 16px;max-width:620px}
  .tags{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:22px}
  .tag{font-size:12px;font-weight:600;padding:4px 10px;border-radius:999px;background:var(--soft);color:var(--brand-d)}
  .actions{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:24px}
  .btn{display:inline-flex;align-items:center;justify-content:center;text-align:center;text-decoration:none;
       min-height:44px;padding:11px 22px;border-radius:6px;font-size:14.5px;font-weight:500;
       border:1px solid transparent;transition:background .12s,border-color .12s}
  .btn.primary{background:var(--green);color:#fff}
  .btn.primary:hover{background:var(--green-d)}
  .btn.ghost{background:#fff;border-color:var(--line);color:var(--ink)}
  .btn.ghost:hover{background:#f7f8fa}
  .stats{display:flex;flex-wrap:wrap;gap:26px;padding-top:18px;border-top:1px solid var(--line)}
  .stat b{display:block;font-size:22px;line-height:1.1;font-weight:700}
  .stat span{font-size:12px;color:var(--muted)}

  .hero-card{background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden;
             box-shadow:0 2px 8px rgba(20,30,40,.06);position:sticky;top:calc(var(--header-h) + 16px)}
  .cover{height:156px;background:linear-gradient(135deg,#1f2b3a 0%,#22405e 55%,#2f6f4f 100%);
         color:#fff;display:flex;flex-direction:column;justify-content:flex-end;padding:20px}
  .cover b{font-size:32px;line-height:1;letter-spacing:-1px}
  .cover small{color:#b8d6ef;font-size:12px;margin-top:6px}
  .hero-card .body{padding:18px}
  .progress{height:6px;border-radius:99px;background:var(--line);overflow:hidden;margin-bottom:10px}
  .progress i{display:block;height:100%;width:0;background:var(--green)}
  .hero-card p{margin:0 0 12px;font-size:12.5px;color:var(--muted)}
  .checklist{list-style:none;margin:14px 0 0;padding:0}
  .checklist li{display:flex;gap:9px;padding:8px 0;border-top:1px solid var(--line);font-size:13px}
  .checklist li:before{content:"✓";color:var(--green);font-weight:700}
  .hero-card .btn{width:100%;margin-top:16px}

  /* основной блок */
  .layout{display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:28px;align-items:start}
  .card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:22px 24px;margin-bottom:18px}
  h2{font-size:21px;line-height:1.3;margin:0 0 12px;letter-spacing:-.2px}
  h3{font-size:15px;margin:0 0 6px}
  .card p{margin:8px 0;color:#444}
  .program{margin:14px 0 0}
  .program-item{display:flex;gap:12px;padding:11px 0;border-top:1px solid var(--line)}
  .num{width:26px;height:26px;flex:0 0 auto;border-radius:50%;background:var(--soft);color:var(--brand-d);
       display:grid;place-items:center;font-size:12px;font-weight:700;margin-top:1px}
  .program-item b{display:block;font-size:14.5px;font-weight:600}
  .program-item small{display:block;color:var(--muted);font-size:12.5px;line-height:1.45;margin-top:2px}
  .module{font-size:11.5px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:var(--muted);
          margin:18px 0 6px;display:flex;align-items:center;gap:8px}
  .module:before{content:"";width:3px;height:13px;border-radius:2px;background:var(--green)}
  .features{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-top:14px}
  .feature{border:1px solid var(--line);border-radius:8px;padding:13px 14px}
  .feature b{display:block;font-size:13.5px;margin-bottom:3px}
  .feature span{font-size:12.5px;color:var(--muted);line-height:1.45}
  .note{font-size:12.5px;color:var(--muted);margin-top:14px;line-height:1.55}
  .side .card{position:sticky;top:calc(var(--header-h) + 16px)}
  .side .kpi{display:flex;justify-content:space-between;gap:10px;padding:9px 0;border-bottom:1px solid var(--line);font-size:13.5px}
  .side .kpi:last-child{border-bottom:0}
  .side .kpi b{font-weight:600}
  .side .btn{width:100%;margin-top:6px}
  .side .btn + .btn{margin-top:8px}

  footer{background:var(--topbar);color:#9d9d9d;padding:28px 0;font-size:12.5px}
  footer .wrap{display:flex;flex-wrap:wrap;gap:18px;justify-content:space-between;align-items:center}
  footer a{color:#c9d9ef;text-decoration:none}
  footer a:hover{text-decoration:underline}

  @media (max-width:900px){
    .hero,.layout{grid-template-columns:1fr}
    .hero-card,.side .card{position:static}
  }
  @media (max-width:760px){
    .stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px 10px}
    .stat b{font-size:20px}
    .hero-card{margin-top:2px}
    .cover{height:104px;padding:16px}
    .cover b{font-size:26px}
    .hero-card .body{padding:16px}
    .checklist li{font-size:12.5px}
  }
  @media (max-width:560px){
    main{padding:16px 0 44px}
    .crumbs{display:flex;align-items:center;white-space:nowrap;overflow-x:auto;
            scrollbar-width:none;font-size:12px;margin-bottom:14px;padding-bottom:2px}
    .crumbs::-webkit-scrollbar{display:none}
    .crumbs span{margin:0 5px}
    h1{margin-bottom:10px}
    .lead{margin-bottom:14px}
    .tags{gap:6px;margin-bottom:18px}
    .tag{font-size:11.5px;padding:4px 9px}
    .actions{display:grid;grid-template-columns:1fr;gap:8px;margin-bottom:20px}
    .actions .btn{width:100%;min-height:48px;font-size:15px}
    .card{padding:16px 14px;margin-bottom:14px}
    h2{font-size:18px}
    .features{grid-template-columns:1fr;gap:8px}
    .feature{padding:12px 13px}
    .program-item{gap:10px}
    .note{font-size:12px}
    .side .btn{min-height:48px}
    footer{padding:24px 0 calc(24px + env(safe-area-inset-bottom))}
    footer .wrap{flex-direction:column;align-items:flex-start;gap:10px}
    footer .wrap>span{width:100%}
    footer .wrap>span:last-child{display:flex;flex-wrap:wrap;gap:4px 14px}
    footer a{display:inline-flex;align-items:center;min-height:32px}
  }
</style>
</head>
<body>
<header class="topbar">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="ДЭ.Курс">
      <span class="brand-mark">ДЭ</span>
      <span class="brand-text">.Курс</span>
    </a>
    <nav class="topnav" id="topnav">
      <a href="docs/">Каталог</a>
      <a href="docs/">Моё обучение</a>
      <a href="https://github.com/TR-Artem/demo-examen" target="_blank" rel="noopener">Материалы</a>
      <a class="nav-cta" href="docs/">Начать курс</a>
    </nav>
    <a class="login" href="docs/">Начать курс</a>
    <button class="menu-btn" id="menuBtn" type="button" aria-label="Открыть меню"
            aria-controls="topnav" aria-expanded="false">☰</button>
  </div>
</header>

<main>
  <div class="wrap">
    <div class="crumbs">
      <a href="index.html">Главная</a><span>/</span>
      <a href="docs/">Каталог</a><span>/</span>
      Демонстрационный экзамен
    </div>

    <section class="hero">
      <div>
        <div class="eyebrow">Профильный демонстрационный экзамен · 09.02.07</div>
        <h1>ДЭ 09.02.07-3-2027 «Разработчик веб и мультимедийных приложений»</h1>
        <p class="lead">
          Полный курс подготовки к демонстрационному экзамену: план на 12 недель,
          15 уроков теории, 53 теста с практическими заданиями, 19 SQL-задач
          с автопроверкой и пробный экзамен на 100 баллов. Всё работает офлайн
          прямо в браузере.
        </p>
        <div class="tags">
          <span class="tag">Flask + SQLite</span>
          <span class="tag">HTML / CSS / JS</span>
          <span class="tag">3 модуля · 100 баллов</span>
          <span class="tag">офлайн</span>
        </div>
        <div class="actions">
          <a class="btn primary" href="docs/">Выбрать курс</a>
          <a class="btn ghost" href="DemoExam-mobile.html" download>Скачать офлайн HTML</a>
          <a class="btn ghost" href="docs/DemoExam-mobile-is.html">Курс «Информационные системы»</a>
        </div>
        <div class="stats">
          <div class="stat"><b>60</b><span>занятий</span></div>
          <div class="stat"><b>15</b><span>уроков теории</span></div>
          <div class="stat"><b>53</b><span>теста</span></div>
          <div class="stat"><b>14</b><span>практик с кодом</span></div>
          <div class="stat"><b>19</b><span>SQL-задач</span></div>
          <div class="stat"><b>100</b><span>баллов</span></div>
        </div>
      </div>

      <aside class="hero-card">
        <div class="cover"><b>ДЭ 2027</b><small>Веб и мультимедийные приложения</small></div>
        <div class="body">
          <div class="progress"><i></i></div>
          <p>Прогресс сохраняется локально и переносится через JSON.</p>
          <ul class="checklist">
            <li>План на 12 недель и 60 занятий</li>
            <li>Теория, тесты и SQL с проверкой</li>
            <li>Тесты с редактором кода и автопроверкой</li>
            <li>Пробник с таймером 4:00:00</li>
            <li>Шпаргалки и разбор критериев</li>
          </ul>
          <a class="btn primary" href="docs/">Открыть тренажёр</a>
        </div>
      </aside>
    </section>

    <div class="layout">
      <div>
        <section class="card">
          <h2>О курсе</h2>
          <p>
            Курс собран по структуре КОД 09.02.07-3-2026: три модуля, 75 баллов
            инварианта и 25 баллов вариативной части. Внутри — весь стек
            экзамена: Python, Flask, SQLite, HTML, CSS и JavaScript.
          </p>
          <p>
            Начни с плана, пройди теорию, закрепи тесты и SQL, затем проверь
            себя на пробном экзамене. Прогресс сохраняется в браузере, поэтому
            можно возвращаться к курсу в любое время.
          </p>
          <div class="features">
            <div class="feature"><b>План на 12 недель</b><span>60 занятий с темами, задачами и отметками о выполнении.</span></div>
            <div class="feature"><b>Тесты + практика</b><span>53 вопроса и 14 заданий с редактором кода и автопроверкой.</span></div>
            <div class="feature"><b>Пробный экзамен</b><span>Чек-лист критериев на 100 баллов, таймер и оценка 3/4/5.</span></div>
            <div class="feature"><b>Офлайн</b><span>Веб-версия и один HTML-файл для телефона без интернета.</span></div>
          </div>
        </section>

        <section class="card">
          <h2>Второй курс: «Программист» (09.02.07-2)</h2>
          <p>
            Для квалификации «Программист» добавлен отдельный трек:
            <b>Python + SQLite + tkinter</b>, 4 модуля и предметная область
            «Магазин обуви» (КОД 2026). В нём свой план, теория, 41 тест
            с 11 практическими заданиями, SQL-практика и чек-лист на 100 баллов.
          </p>
          <div class="actions">
            <a class="btn primary" href="docs/DemoExam-mobile-programmer.html">Открыть онлайн</a>
            <a class="btn ghost" href="DemoExam-mobile-programmer.html" download>Скачать офлайн-версию</a>
          </div>
          <p class="note">
            На компьютере: <code>./run.sh programmer</code> или
            <code>run_programmer.bat</code>. В тренажёре есть переключатель «Курс».
          </p>
        </section>

        <section class="card">
          <h2>Третий курс: «Информационные системы» (09.02.07-5)</h2>
          <p>
            Для квалификации «Специалист по информационным системам»:
            <b>ER, SQL, авторизация, API, Postman и документация</b>,
            шесть заданий КИМ 2027. В курсе 15 уроков, 39 вопросов,
            15 практических заданий, 19 SQL-задач и чек-лист на 100 баллов.
          </p>
          <div class="actions">
            <a class="btn primary" href="docs/DemoExam-mobile-is.html">Открыть онлайн</a>
            <a class="btn ghost" href="DemoExam-mobile-is.html" download>Скачать офлайн-версию</a>
          </div>
          <p class="note">
            На компьютере: <code>./run.sh is</code> или <code>run_is.bat</code>.
          </p>
        </section>

        <section class="card">
          <h2>Программа курса</h2>
          <div class="program">
            <div class="module">Модуль 1 · Подготовка</div>
            <div class="program-item"><span class="num">1</span><div><b>План на 12 недель</b><small>60 занятий: HTML/CSS/JS → Flask → БД → модули экзамена → пробники</small></div></div>
            <div class="program-item"><span class="num">2</span><div><b>Теория</b><small>15 уроков: экзамен, вёрстка, адаптив, JavaScript, Flask, SQL, безопасность</small></div></div>
            <div class="program-item"><span class="num">3</span><div><b>Тесты с практикой</b><small>53 вопроса и 14 заданий: пиши код, получай автопроверку</small></div></div>

            <div class="module">Модуль 2 · Практика</div>
            <div class="program-item"><span class="num">4</span><div><b>SQL-практика</b><small>19 задач с автопроверкой: выборки, JOIN, агрегаты, даты</small></div></div>
            <div class="program-item"><span class="num">5</span><div><b>Пробный экзамен</b><small>Чек-лист на 100 баллов, таймер 4 часа, история попыток</small></div></div>

            <div class="module">Модуль 3 · Материалы</div>
            <div class="program-item"><span class="num">6</span><div><b>Шпаргалки</b><small>13 готовых фрагментов кода для экзамена</small></div></div>
            <div class="program-item"><span class="num">7</span><div><b>Мой прогресс</b><small>Готовность, слабые темы, экспорт и импорт JSON</small></div></div>
          </div>
          <p class="note">
            Дополнительно в репозитории: эталонный проект «Корочки.есть» на Flask,
            шпаргалки в Markdown, ER-диаграмма и руководство пользователя.
          </p>
        </section>
      </div>

      <aside class="side">
        <div class="card">
          <h3>Что внутри</h3>
          <div class="kpi"><span>Формат</span><b>веб + офлайн</b></div>
          <div class="kpi"><span>Стек</span><b>Flask + SQLite</b></div>
          <div class="kpi"><span>Доступ</span><b>без регистрации</b></div>
          <div class="kpi"><span>Прогресс</span><b>локально</b></div>
          <div class="kpi"><span>Язык</span><b>русский</b></div>
          <a class="btn primary" href="docs/">Перейти к курсу</a>
          <a class="btn ghost" href="DemoExam-mobile.html" download>Скачать HTML · ~1 МБ</a>
          <a class="btn ghost" href="https://github.com/TR-Artem/demo-examen" target="_blank" rel="noopener">Исходники на GitHub</a>
        </div>
      </aside>
    </div>
  </div>
</main>

<footer>
  <div class="wrap">
    <span>ДЭ.Курс · подготовка к демонстрационному экзамену 09.02.07</span>
    <span><a href="docs/">Тренажёр</a> · <a href="https://github.com/TR-Artem/demo-examen" target="_blank" rel="noopener">GitHub</a> · <a href="https://bom.firpo.ru/Public" target="_blank" rel="noopener">Банк оценочных материалов</a></span>
  </div>
</footer>
<script>
(function(){
  var btn = document.getElementById("menuBtn");
  var nav = document.getElementById("topnav");
  if(!btn || !nav) return;
  function setOpen(open){
    document.body.classList.toggle("nav-open", open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");
    btn.setAttribute("aria-label", open ? "Закрыть меню" : "Открыть меню");
    btn.textContent = open ? "✕" : "☰";
  }
  btn.addEventListener("click", function(){
    setOpen(!document.body.classList.contains("nav-open"));
  });
  nav.addEventListener("click", function(e){
    if(e.target.closest("a")) setOpen(false);
  });
  document.addEventListener("keydown", function(e){
    if(e.key === "Escape") setOpen(false);
  });
  document.addEventListener("click", function(e){
    if(document.body.classList.contains("nav-open") && !e.target.closest(".topbar")) setOpen(false);
  });
  window.addEventListener("resize", function(){
    if(window.innerWidth > 760) setOpen(false);
  });
})();
</script>
</body>
</html>
"""


def main():
    DOCS.mkdir(exist_ok=True)
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    (DOCS / "index.html").write_text(COURSE_CHOOSER, encoding="utf-8")
    shutil.copy2(APK, DOCS / APK.name)
    for source in (HTML, HTML_PROG, HTML_IS):
        if not source.exists():
            continue
        target = DOCS / source.name
        shutil.copy2(source, target)
        text = target.read_text(encoding="utf-8")
        if "course-switch" not in text:
            text = text.replace("</body>", SWITCHER + "\n</body>", 1)
            target.write_text(text, encoding="utf-8")

    (ROOT / "index.html").write_text(LANDING, encoding="utf-8")
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")

    print("Готово:")
    print("  ", ROOT / "index.html", "(главная: страница курса)")
    print("  ", DOCS / "index.html", "(выбор из трёх курсов)")
    print("  ", DOCS / APK.name, f"{APK.stat().st_size / 1024:.0f} КБ (архив)")
    for source in (HTML, HTML_PROG, HTML_IS):
        if source.exists():
            target = DOCS / source.name
            print("  ", target, f"{target.stat().st_size / 1024 / 1024:.2f} МБ")
    print("Сайт:", SITE)


if __name__ == "__main__":
    main()
