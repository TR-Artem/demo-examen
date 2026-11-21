# -*- coding: utf-8 -*-
"""
Публикация веб-версии на GitHub Pages.

Берёт самодостаточный DemoExam-mobile.html, добавляет сверху полосу
«Это веб-версия · Скачать APK» и кладёт результат в docs/index.html.
APK копируется рядом, чтобы скачиваться прямо с сайта.

После запуска:
  git add docs publish_site.py
  git commit -m "Add GitHub Pages web version"
  git push
Затем на GitHub: Settings → Pages → Deploy from a branch →
Branch: main, folder: /docs → Save.
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
SITE = DOCS / "index.html"
APK = ROOT / "DemoExam-09-02-07.apk"
HTML = ROOT / "DemoExam-mobile.html"

REPO = "https://github.com/alessstft/Demoexam"

BANNER = f"""
<div style="background:#2E8B57;color:#fff;padding:10px 12px;text-align:center;
            font:600 13px -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
            position:relative;z-index:25">
  Веб-версия тренажёра ·
  <a href="DemoExam-09-02-07.apk" download
     style="color:#fff;text-decoration:underline">Скачать APK для Android</a>
  ·
  <a href="{REPO}" target="_blank" rel="noopener"
     style="color:#fff;text-decoration:underline">исходники</a>
</div>
"""


def main():
    DOCS.mkdir(exist_ok=True)
    html = HTML.read_text(encoding="utf-8")
    if "site-banner" not in html:
        html = html.replace(
            "<body>",
            '<body>\n<!-- site-banner -->' + BANNER,
            1,
        )
    # Чтобы GitHub Pages не пытался обрабатывать файл через Jekyll
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    SITE.write_text(html, encoding="utf-8")
    shutil.copy2(APK, DOCS / APK.name)
    print("Готово:")
    print("  ", SITE, f"{SITE.stat().st_size / 1024 / 1024:.2f} МБ")
    print("  ", DOCS / APK.name, f"{APK.stat().st_size / 1024:.0f} КБ")
    print("Сайт после включения Pages:")
    print("   https://alessstft.github.io/Demoexam/")


if __name__ == "__main__":
    main()
