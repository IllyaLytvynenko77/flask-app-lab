import unittest
from app import app


class MainPagesTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_resume(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_homepage(self):
        response = self.client.get("/homepage")
        self.assertEqual(response.status_code, 200)

    def test_contacts(self):
        response = self.client.get("/contacts")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
