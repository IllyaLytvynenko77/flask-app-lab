import unittest
from app import create_app
from config import TestingConfig


class Lab4BlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()

    def test_index_redirects_to_login(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 302)
        self.assertIn("/login", res.headers["Location"])

    def test_login_and_profile_flow(self):
        res = self.client.post(
            "/login",
            data={"username": "admin", "password": "12345"},
            follow_redirects=True,
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn("Ласкаво просимо, admin!".encode("utf-8"), res.data)

    def test_cookie_and_theme_management(self):
        self.client.post("/login", data={"username": "admin", "password": "12345"})
        res = self.client.post(
            "/cookie/add",
            data={"key": "lang", "value": "uk", "days": "5"},
            follow_redirects=True,
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"lang", res.data)

        res_theme = self.client.post("/theme/dark", follow_redirects=True)
        self.assertEqual(res_theme.status_code, 200)
        self.assertIn(b"theme-dark", res_theme.data)


if __name__ == "__main__":
    unittest.main()
