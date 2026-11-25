# -*- coding: utf-8 -*-
"""Smoke-тесты эталонного проекта. Запуск: python -m unittest discover -s tests"""
from __future__ import annotations

import os
import sqlite3
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import create_app  # noqa: E402


class AppTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tmp.name, "test.db")
        self.app = create_app({
            "TESTING": True,
            "SECRET_KEY": "test-secret",
            "DATABASE": self.db_path,
            "CSRF_ENABLED": False,
        })
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    # -- helpers -------------------------------------------------------
    def db(self):
        con = sqlite3.connect(self.db_path)
        con.row_factory = sqlite3.Row
        return closing(con)

    def login(self, login="demo01", password="password123"):
        return self.client.post(
            "/login", data={"login": login, "password": password},
            follow_redirects=False,
        )

    # -- tests ---------------------------------------------------------
    def test_index_redirects_to_login(self):
        response = self.client.get("/", follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])

    def test_index_redirects_authenticated_user(self):
        self.login()
        response = self.client.get("/", follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboard", response.headers["Location"])

    def test_registration_valid(self):
        response = self.client.post("/register", data={
            "login": "newuser1",
            "password": "password123",
            "password2": "password123",
        }, follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        with self.db() as con:
            row = con.execute(
                "SELECT login, full_name, password_hash FROM users WHERE login = ?",
                ("newuser1",)).fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row["full_name"], "newuser1")
        self.assertNotEqual(row["password_hash"], "password123")

    def test_registration_invalid(self):
        response = self.client.post("/register", data={
            "login": "ab",
            "password": "123",
            "password2": "456",
        })
        text = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Никнейм", text)
        self.assertIn("Пароль", text)

    def test_registration_cyrillic_nickname(self):
        response = self.client.post("/register", data={
            "login": "Тест02",
            "password": "password123",
            "password2": "password123",
        }, follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        with self.db() as con:
            row = con.execute("SELECT login FROM users WHERE login = ?", ("Тест02",)).fetchone()
        self.assertIsNotNone(row)

    def test_registration_password_mismatch(self):
        response = self.client.post("/register", data={
            "login": "newuser2",
            "password": "password123",
            "password2": "different123",
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("не совпадают", response.get_data(as_text=True))

    def test_login_and_logout(self):
        response = self.login()
        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboard", response.headers["Location"])

        dashboard = self.client.get("/dashboard")
        self.assertEqual(dashboard.status_code, 200)
        self.assertIn("Мои заявки", dashboard.get_data(as_text=True))

        self.client.post("/logout")
        protected = self.client.get("/dashboard", follow_redirects=False)
        self.assertEqual(protected.status_code, 302)
        self.assertIn("/login", protected.headers["Location"])

    def test_wrong_password(self):
        response = self.client.post(
            "/login", data={"login": "demo01", "password": "wrong"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Неверный логин или пароль", response.get_data(as_text=True))

    def test_create_application(self):
        self.login()
        response = self.client.post("/applications/new", data={
            "course_id": "1",
            "start_date": "15.09.2026",
            "payment_method": "cash",
        }, follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        with self.db() as con:
            row = con.execute(
                "SELECT start_date, payment_method, status_id FROM applications "
                "ORDER BY application_id DESC LIMIT 1").fetchone()
        self.assertEqual(row["start_date"], "2026-09-15")
        self.assertEqual(row["payment_method"], "cash")
        self.assertEqual(row["status_id"], 1)

    def test_invalid_application_date(self):
        self.login()
        response = self.client.post("/applications/new", data={
            "course_id": "1",
            "start_date": "2026-09-15",
            "payment_method": "cash",
        })
        # ISO-дата тоже допустима, поэтому проверяем именно мусор
        self.assertEqual(response.status_code, 302)

        bad = self.client.post("/applications/new", data={
            "course_id": "1",
            "start_date": "вчера",
            "payment_method": "cash",
        })
        self.assertEqual(bad.status_code, 200)
        self.assertIn("ДД.ММ.ГГГГ", bad.get_data(as_text=True))

    def test_admin_forbidden_for_user(self):
        self.login()
        response = self.client.get("/admin")
        self.assertEqual(response.status_code, 403)

    def test_admin_access(self):
        response = self.login("Admin", "KorokNET")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin", response.headers["Location"])
        page = self.client.get("/admin")
        self.assertEqual(page.status_code, 200)
        self.assertIn("Все заявки", page.get_data(as_text=True))

    def test_cancel_requires_reason(self):
        self.login("Admin", "KorokNET")
        with self.db() as con:
            app_id = con.execute(
                "SELECT application_id FROM applications WHERE status_id = 1 LIMIT 1"
            ).fetchone()["application_id"]

        self.client.post(f"/admin/applications/{app_id}/status",
                         data={"status_id": "4", "cancel_reason": ""})
        with self.db() as con:
            status = con.execute(
                "SELECT status_id FROM applications WHERE application_id = ?",
                (app_id,)).fetchone()["status_id"]
        self.assertEqual(status, 1)

        self.client.post(f"/admin/applications/{app_id}/status",
                         data={"status_id": "4", "cancel_reason": "Тестовая отмена"})
        with self.db() as con:
            row = con.execute(
                "SELECT status_id, cancel_reason FROM applications WHERE application_id = ?",
                (app_id,)).fetchone()
        self.assertEqual(row["status_id"], 4)
        self.assertEqual(row["cancel_reason"], "Тестовая отмена")

    def test_review_only_after_completion(self):
        self.login()
        with self.db() as con:
            app_id = con.execute(
                "SELECT application_id FROM applications "
                "WHERE user_id = (SELECT user_id FROM users WHERE login = 'demo01') "
                "AND status_id = 1 LIMIT 1").fetchone()["application_id"]

        response = self.client.post(
            f"/applications/{app_id}/review",
            data={"rating": "5", "review_text": "Отличный курс"},
            follow_redirects=True,
        )
        self.assertIn("только после завершения",
                      response.get_data(as_text=True))

    def test_api_requires_login(self):
        response = self.client.get("/api/applications")
        self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()
