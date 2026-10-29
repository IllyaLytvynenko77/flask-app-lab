import unittest
from app import app


class ProductsBlueprintTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_product_list(self):
        """Список товарів містить усі три товари."""
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"Phone", response.data)
        self.assertIn(b"PC", response.data)

    def test_product_detail(self):
        """Детальна сторінка товару з id=2."""
        response = self.client.get("/products/2")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Phone", response.data)
        self.assertIn(b"800", response.data)

    def test_product_not_found(self):
        """Неіснуючий id повертає 404."""
        response = self.client.get("/products/999")
        self.assertEqual(response.status_code, 404)

    def test_invalid_id_type(self):
        """Нечисловий id не відповідає маршруту (404)."""
        response = self.client.get("/products/abc")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
