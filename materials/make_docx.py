# -*- coding: utf-8 -*-
"""Создаёт минимальный .docx с шаблоном руководства пользователя."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.sax.saxutils import escape

BASE = Path(__file__).resolve().parent
OUT = BASE / "Руководство_пользователя.docx"

DOC = [
    ("title", "РУКОВОДСТВО ПОЛЬЗОВАТЕЛЯ"),
    ("subtitle", "Система оформления заказов обуви «Чудо Обувь»"),
    ("subtitle", "Версия 1.0"),
    ("h1", "1. Назначение программы"),
    ("p", "Система предназначена для просмотра каталога обуви, выбора модели "
           "и размера, оформления заказов, а также для работы сотрудников "
           "с заказами и статистикой."),
    ("h1", "2. Вход в систему"),
    ("p", "Выберите свой логин из списка и нажмите «Войти». Пароль не требуется. "
           "Для просмотра каталога без авторизации нажмите «Без входа»."),
    ("p", "После входа ФИО пользователя отображается в правом верхнем углу."),
    ("shot", "[Скриншот 1. Окно входа в систему]"),
    ("h1", "3. Каталог товаров"),
    ("p", "В каталоге отображаются изображение товара (или заглушка picture.png), "
           "категория, наименование, производство, состав, цена со скидкой "
           "и остаток («много» или «мало»). Строки с остатком не более трёх пар "
           "подсвечены светло-красным цветом."),
    ("p", "Авторизованному пользователю доступны поиск по наименованию и описанию, "
           "фильтр по категории (первый пункт — «Все категории») и сортировка "
           "по цене по возрастанию и убыванию."),
    ("shot", "[Скриншот 2. Каталог товаров]"),
    ("h1", "4. Оформление заказа"),
    ("p", "Нажмите на товар, чтобы открыть карточку. Выберите размер и количество, "
           "нажмите «Добавить в корзину». В корзине проверьте позиции и нажмите "
           "«Оформить заказ». Заказ сохраняется с текущей датой, остаток уменьшается."),
    ("shot", "[Скриншот 3. Карточка товара / корзина]"),
    ("h1", "5. Работа с заказами (Менеджер, Администратор)"),
    ("p", "В разделе «Заказы» отображается список заказов с датой и ФИО клиента. "
           "Состав заказа: товар, производство, размер, количество, цена за единицу "
           "и итоговая сумма. Администратор может изменить дату заказа и удалить позицию."),
    ("shot", "[Скриншот 4. Список заказов и состав]"),
    ("h1", "6. Статистика"),
    ("p", "Кнопка «Статистика» доступна Менеджеру и Администратору. В окне — "
           "таблица всех заказов и три показателя: количество заказов, выручка, "
           "средний чек."),
    ("shot", "[Скриншот 5. Статистика заказов]"),
    ("h1", "7. Завершение работы"),
    ("p", "Для выхода нажмите «Выход» — программа вернётся на экран входа."),
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
