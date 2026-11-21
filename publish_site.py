# -*- coding: utf-8 -*-
"""
Публикация сайта на GitHub Pages: главная с двумя версиями + веб-тренажёр.

Что делает:
  1. docs/index.html  — самодостаточный тренажёр + баннер «Скачать APK»;
  2. docs/DemoExam-09-02-07.apk — APK для скачивания с сайта;
  3. index.html       — главная страница с двумя кнопками: веб и APK;
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
REPO = "https://github.com/alessstft/Demoexam"
SITE = "https://alessstft.github.io/Demoexam/"

BANNER = """
<div style="background:#2E8B57;color:#fff;padding:10px 12px;text-align:center;
            font:600 13px -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
            position:relative;z-index:25">
  Веб-версия тренажёра ·
  <a href="DemoExam-09-02-07.apk" download
     style="color:#fff;text-decoration:underline">Скачать APK для Android</a>
  ·
  <a href="%s" target="_blank" rel="noopener"
     style="color:#fff;text-decoration:underline">исходники</a>
</div>
""" % REPO

LANDING = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#2E8B57">
<title>ДЭ 09.02.07-2-2027 «Программист» — тренажёр</title>
<style>
  :root { --bg:#f3f6f8; --card:#fff; --ink:#1d2733; --muted:#5c6b7a;
          --line:#dde5ea; --accent:#2E8B57; --accent-d:#1f6a41; --soft:#e8f3ec; }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--bg); color:var(--ink);
         font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; }
  main { max-width:900px; margin:0 auto; padding:36px 18px 60px; }
  h1 { font-size:28px; line-height:1.2; margin:0 0 8px; }
  h1 small { display:block; font-size:14px; font-weight:400; color:var(--muted); margin-top:6px; }
  .lead { color:var(--muted); margin:0 0 28px; }
  .cards { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
  @media (max-width:680px) { .cards { grid-template-columns:1fr; } }
  .card { display:flex; flex-direction:column; background:var(--card);
          border:1px solid var(--line); border-radius:18px; padding:22px;
          text-decoration:none; color:var(--ink);
          box-shadow:0 2px 8px rgba(20,40,60,.07); transition:transform .15s, box-shadow .15s; }
  .card:hover { transform:translateY(-2px); box-shadow:0 8px 22px rgba(20,40,60,.12); }
  .icon { font-size:34px; line-height:1; margin-bottom:10px; }
  .card h2 { margin:0 0 6px; font-size:20px; color:var(--accent-d); }
  .card p { margin:0 0 18px; color:var(--muted); font-size:14px; flex:1; }
  .btn { display:inline-block; text-align:center; background:var(--accent); color:#fff;
         font-weight:700; padding:12px 16px; border-radius:12px; }
  .card.secondary .btn { background:var(--soft); color:var(--accent-d); }
  .note { margin-top:22px; font-size:13px; color:var(--muted); }
  .links { margin-top:26px; font-size:14px; }
  a { color:var(--accent-d); }
  .tag { display:inline-block; background:var(--soft); color:var(--accent-d);
         font-size:12px; font-weight:700; padding:3px 10px; border-radius:999px;
         margin-right:6px; }
</style>
</head>
<body>
<main>
  <h1>ДЭ 09.02.07-2-2027 «Программист»
    <small>Профильный демонстрационный экзамен · 5 заданий · 100 баллов</small>
  </h1>
  <p class="lead">
    <span class="tag">Python + SQLite</span>
    <span class="tag">8 таблиц</span>
    <span class="tag">офлайн</span>
  </p>

  <div class="cards">
    <a class="card" href="docs/">
      <div class="icon">🌐</div>
      <h2>Веб-версия</h2>
      <p>План на 60 занятий, 15 уроков, 42 теста, 19 SQL-задач с автопроверкой
         и пробный экзамен на 100 баллов. Открывается в любом браузере.</p>
      <span class="btn">Открыть в браузере</span>
    </a>

    <a class="card secondary" href="DemoExam-09-02-07.apk" download>
      <div class="icon">🤖</div>
      <h2>Android APK</h2>
      <p>Тот же тренажёр в телефоне. SQLite встроен, интернет и разрешения
         не нужны. Устанавливается за минуту.</p>
      <span class="btn">Скачать APK · 0,45 МБ</span>
    </a>
  </div>

  <p class="note">
    Обе версии используют одни и те же материалы. Прогресс сохраняется локально
    (в браузере или в приложении) и переносится через «Прогресс → Скопировать JSON».
    APK подписан самоподписанным сертификатом — Android может предупредить
    «неизвестный разработчик», это нормально.
  </p>

  <p class="links">
    <a href="https://github.com/alessstft/Demoexam">Исходники, инструкции,
    шпаргалки и релизы на GitHub</a>
  </p>
</main>
</body>
</html>
"""


def main():
    DOCS.mkdir(exist_ok=True)
    html = HTML.read_text(encoding="utf-8")
    if "site-banner" not in html:
        html = html.replace("<body>", '<body>\n<!-- site-banner -->' + BANNER, 1)
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    (DOCS / "index.html").write_text(html, encoding="utf-8")
    shutil.copy2(APK, DOCS / APK.name)

    (ROOT / "index.html").write_text(LANDING, encoding="utf-8")
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")

    print("Готово:")
    print("  ", ROOT / "index.html", "(главная: две версии)")
    print("  ", DOCS / "index.html", f"{ (DOCS / 'index.html').stat().st_size / 1024 / 1024:.2f} МБ")
    print("  ", DOCS / APK.name, f"{APK.stat().st_size / 1024:.0f} КБ")
    print("Сайт:", SITE)


if __name__ == "__main__":
    main()
