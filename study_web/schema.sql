PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    user_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    login         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS progress (
    user_id    INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    course     TEXT NOT NULL,
    module     INTEGER NOT NULL,
    step       INTEGER NOT NULL,
    status     TEXT NOT NULL DEFAULT 'done',
    score      INTEGER,
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (user_id, course, module, step)
);
