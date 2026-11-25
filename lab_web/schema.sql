-- Схема БД портала «Корочки.есть»
-- 6 таблиц, 3НФ, ограничения целостности.
-- Запуск: sqlite3 instance/korochki.db < schema.sql

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS roles (
    role_id   INTEGER PRIMARY KEY,
    role_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS users (
    user_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    login         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    full_name     TEXT NOT NULL,
    phone         TEXT NOT NULL,
    email         TEXT NOT NULL UNIQUE,
    role_id       INTEGER NOT NULL REFERENCES roles(role_id),
    created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS courses (
    course_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    title          TEXT NOT NULL UNIQUE,
    description    TEXT,
    duration_hours INTEGER NOT NULL CHECK (duration_hours > 0),
    price          REAL NOT NULL CHECK (price >= 0),
    image          TEXT
);

CREATE TABLE IF NOT EXISTS application_statuses (
    status_id   INTEGER PRIMARY KEY,
    status_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS applications (
    application_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id        INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    course_id      INTEGER NOT NULL REFERENCES courses(course_id) ON DELETE RESTRICT,
    start_date     TEXT NOT NULL,
    payment_method TEXT NOT NULL CHECK (payment_method IN ('cash', 'phone_transfer')),
    status_id      INTEGER NOT NULL REFERENCES application_statuses(status_id),
    cancel_reason  TEXT,
    created_at     TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS reviews (
    review_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER NOT NULL UNIQUE
                   REFERENCES applications(application_id) ON DELETE CASCADE,
    user_id        INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    rating         INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review_text    TEXT,
    created_at     TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_applications_user   ON applications(user_id);
CREATE INDEX IF NOT EXISTS idx_applications_course ON applications(course_id);
CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(status_id);
CREATE INDEX IF NOT EXISTS idx_reviews_rating      ON reviews(rating);
