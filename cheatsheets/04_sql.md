# SQL для экзамена

## SELECT

```sql
SELECT application_id, start_date, payment_method
FROM applications
WHERE status_id = 1
ORDER BY start_date
LIMIT 10;
```

## Поиск

```sql
SELECT user_id, full_name, phone
FROM users
WHERE full_name LIKE '%Иван%'
   OR phone LIKE '8(921)%';
```

`LIKE` в SQLite регистрозависим для кириллицы — проверяй на реальных данных.

## JOIN

```sql
SELECT a.application_id, u.full_name, c.title, s.status_name
FROM applications a
JOIN users u ON u.user_id = a.user_id
JOIN courses c ON c.course_id = a.course_id
JOIN application_statuses s ON s.status_id = a.status_id
ORDER BY a.application_id;
```

- `INNER JOIN` — только совпадения;
- `LEFT JOIN` — все строки левой таблицы + совпадения.

## Агрегаты

```sql
SELECT c.title, COUNT(*) AS cnt
FROM applications a
JOIN courses c ON c.course_id = a.course_id
GROUP BY c.course_id, c.title
HAVING COUNT(*) > 1
ORDER BY cnt DESC;
```

`WHERE` — до группировки, `HAVING` — после.

## Подзапрос

```sql
SELECT u.user_id, u.full_name, a.application_id
FROM users u
JOIN applications a ON a.user_id = u.user_id
WHERE a.application_id = (
  SELECT a2.application_id
  FROM applications a2
  WHERE a2.user_id = u.user_id
  ORDER BY a2.created_at DESC
  LIMIT 1
);
```

## Даты

```sql
SELECT date('now');
SELECT date('now', '-30 days');
SELECT strftime('%Y-%m', created_at) AS month, COUNT(*)
FROM applications
GROUP BY month
ORDER BY month;
```

## CASE

```sql
SELECT application_id,
       CASE WHEN status_id = 3 THEN 'завершено' ELSE 'в работе' END AS state
FROM applications;
```

## Параметры

```python
cur.execute('SELECT * FROM users WHERE login = ?', (login,))
```

Никогда не склеивай SQL f-строкой: это SQL-инъекция.

## Полезно

```sql
SELECT COUNT(*) FROM applications;
SELECT COALESCE(SUM(price), 0) FROM courses;
SELECT DISTINCT payment_method FROM applications;
PRAGMA foreign_keys = ON;
```
