# -*- coding: utf-8 -*-
"""Создаёт минимальный .docx с шаблоном руководства пользователя."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.sax.saxutils import escape

BASE = Path(__file__).resolve().parent
OUT = BASE / "Руководство_пользователя.docx"

DOC = [
    ("title", "РУКОВОДСТВО ПОЛЬЗОВАТЕЛЯ"),
    ("subtitle", "Портал онлайн-курсов «Корочки.есть»"),
    ("subtitle", "Версия 1.0"),
    ("h1", "1. Назначение программы"),
    ("p", "Портал предназначен для записи на онлайн-курсы дополнительного "
           "профессионального образования. Пользователь регистрируется, создаёт "
           "заявку на выбранный курс, следит за статусом обучения и оставляет "
           "отзыв после завершения. Администратор видит все заявки и управляет "
           "статусами."),
    ("h1", "2. Регистрация"),
    ("p", "Откройте страницу «Регистрация». Заполните логин (латиница и цифры, "
           "минимум 6 символов), пароль (минимум 8 символов), ФИО (кириллица, "
           "пробелы и дефис), телефон в формате 8(XXX)XXX-XX-XX и email. "
           "Ошибки показываются под полями. Логин и email должны быть уникальными."),
    ("shot", "[Скриншот 1. Форма регистрации с ошибками]"),
    ("h1", "3. Вход в систему"),
    ("p", "Введите логин и пароль. При ошибке выводится сообщение «Неверный логин "
           "или пароль». Для перехода к регистрации используйте ссылку "
           "«Ещё не зарегистрированы? Регистрация». Администратор входит под "
           "логином Admin и паролем KorokNET."),
    ("shot", "[Скриншот 2. Страница входа]"),
    ("h1", "4. Новая заявка"),
    ("p", "В личном кабинете нажмите «Новая заявка». Выберите курс из выпадающего "
           "списка, укажите дату начала в формате ДД.ММ.ГГГГ и способ оплаты "
           "(наличными или переводом по номеру телефона). Нажмите «Отправить заявку»."),
    ("shot", "[Скриншот 3. Форма новой заявки]"),
    ("h1", "5. Мои заявки"),
    ("p", "В разделе «Мои заявки» отображаются курс, дата начала, оплата, стоимость "
           "и статус: «Новая», «Идет обучение», «Обучение завершено» или «Отменена» "
           "с причиной. После статуса «Обучение завершено» появляется форма отзыва: "
           "оценка 1–5 и комментарий. Отзыв можно оставить один раз."),
    ("shot", "[Скриншот 4. Личный кабинет со статусами и формой отзыва]"),
    ("h1", "6. Админ-панель"),
    ("p", "Войдите как Admin / KorokNET. В панели доступны сводка по статусам "
           "и выручке, фильтр по статусу, поиск по ФИО, телефону или курсу, "
           "таблица всех заявок, смена статуса, отмена с обязательной причиной "
           "и пагинация."),
    ("shot", "[Скриншот 5. Админ-панель с фильтром]"),
    ("shot", "[Скриншот 6. Мобильная версия 390×844]"),
    ("h1", "7. Завершение работы"),
    ("p", "Нажмите «Выйти» в правом верхнем углу. Сессия завершится, и вы вернётесь "
           "на главную страницу."),
]


def run(text, size=None, bold=False, align=None, italic=False):
    props = []
    if bold:
        props.append("<w:b/>")
    if italic:
        props.append("<w:i/>")
    if size:
        props.append(f'<w:sz w:val="{size}"/>')
    rpr = f"<w:rPr>{''.join(props)}</w:rPr>" if props else ""
    jc = f'<w:jc w:val="{align}"/>' if align else ""
    ppr = f"<w:pPr>{jc}</w:pPr>" if jc else ""
    return (f'<w:p>{ppr}<w:r>{rpr}'
            f'<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>')


body = []
for kind, text in DOC:
    if kind == "title":
        body.append(run(text, size=36, bold=True, align="center"))
    elif kind == "subtitle":
        body.append(run(text, size=26, align="center"))
    elif kind == "h1":
        body.append(run(text, size=28, bold=True))
    elif kind == "shot":
        body.append(run(text, size=22, italic=True, align="center"))
        body.append(run(""))
    else:
        body.append(run(text, size=24))

document = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    "<w:body>" + "".join(body) +
    '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
    '<w:pgMar w:top="1134" w:right="850" w:bottom="1134" w:left="1701" '
    'w:header="708" w:footer="708" w:gutter="0"/></w:sectPr>'
    "</w:body></w:document>"
)

styles = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:docDefaults><w:rPrDefault><w:rPr>'
    '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>'
    '<w:sz w:val="24"/><w:lang w:val="ru-RU"/>'
    "</w:rPr></w:rPrDefault></w:docDefaults>"
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
    '<w:name w:val="Normal"/></w:style></w:styles>'
)

content_types = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
    "</Types>"
)

rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
    "</Relationships>"
)

doc_rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    "</Relationships>"
)

with ZipFile(OUT, "w", ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", rels)
    z.writestr("word/document.xml", document)
    z.writestr("word/styles.xml", styles)
    z.writestr("word/_rels/document.xml.rels", doc_rels)

print("Готово:", OUT, OUT.stat().st_size, "байт")
