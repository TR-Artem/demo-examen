# -*- coding: utf-8 -*-
"""Тесты учебного портала."""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import create_app  # noqa: E402
import study_content  # noqa: E402


class StudyAppTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.app = create_app({
            "TESTING": True,
            "SECRET_KEY": "test",
            "DATABASE": os.path.join(self.tmp.name, "test.db"),
            "CSRF_ENABLED": False,
        })
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def login(self, login="student", password="password123"):
        return self.client.post(
            "/login", data={"login": login, "password": password},
            follow_redirects=False)

    def test_root_redirects_to_login(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])

    def test_registration(self):
        response = self.client.post("/register", data={
            "login": "student2",
            "password": "password123",
            "password2": "password123",
        }, follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])

    def test_registration_errors(self):
        response = self.client.post("/register", data={
            "login": "ab",
            "password": "123",
            "password2": "456",
        })
        text = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Никнейм", text)
        self.assertIn("Пароль", text)

    def test_login_and_courses(self):
        response = self.login()
        self.assertEqual(response.status_code, 302)
        self.assertIn("/courses", response.headers["Location"])

        page = self.client.get("/courses")
        self.assertEqual(page.status_code, 200)
        text = page.get_data(as_text=True)
        self.assertIn("Веб и мультимедиа", text)
        self.assertIn("Программист", text)
        self.assertNotIn("Заявк", text)
        self.assertNotIn("₽", text)

    def test_course_modules_and_content(self):
        self.login()
        shell = self.client.get("/course/web", follow_redirects=True)
        self.assertEqual(shell.status_code, 200)
        text = shell.get_data(as_text=True)
        self.assertIn("Введение. HTML и CSS", text)
        self.assertIn("Экзамен: структура и модули", text)

        content = self.client.get("/course/web/content")
        self.assertEqual(content.status_code, 200)
        text = content.get_data(as_text=True)
        self.assertIn("ДЭ 09.02.07-3-2027", text)
        self.assertIn("--topbar-h:0px", text)

    def test_theory_step_and_progress(self):
        self.login()
        page = self.client.get("/course/web/module/1/step/1")
        self.assertEqual(page.status_code, 200)
        self.assertIn("Экзамен: структура и модули", page.get_data(as_text=True))

        response = self.client.post("/course/web/module/1/step/1",
                                    follow_redirects=False)
        self.assertEqual(response.status_code, 302)

        total = sum(len(m["steps"]) for m in study_content.modules("web"))
        course = self.client.get("/course/web", follow_redirects=True)
        self.assertIn(f"1 из {total} шагов", course.get_data(as_text=True))

    def test_quiz_step(self):
        self.login()
        step = study_content.modules("web")[0]["steps"][1]
        data = {f"q{i}": str(q["ans"]) for i, q in enumerate(step["questions"])}
        response = self.client.post("/course/web/module/1/step/2", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Шаг зачтён", response.get_data(as_text=True))

    def test_sql_step(self):
        self.login()
        step = study_content.modules("web")[3]["steps"][1]  # SQL-практика
        task = step["tasks"][0]
        response = self.client.post(
            "/course/web/module/4/step/2",
            data={"task_id": task["id"], "user_sql": task["expected"]})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Верно", response.get_data(as_text=True))

    def test_programmer_content(self):
        self.login()
        content = self.client.get("/course/programmer/content")
        self.assertEqual(content.status_code, 200)
        self.assertIn("Программист", content.get_data(as_text=True))

    def test_content_requires_login(self):
        response = self.client.get("/course/web/content")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])

    def test_unknown_course(self):
        self.login()
        self.assertEqual(self.client.get("/course/nope").status_code, 404)
        self.assertEqual(self.client.get("/course/nope/content").status_code, 404)

    def test_logout(self):
        self.login()
        self.client.post("/logout")
        response = self.client.get("/courses", follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])


if __name__ == "__main__":
    unittest.main()
