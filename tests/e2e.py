from fastapi.testclient import TestClient
from unittest import TestCase

from books import app

client = TestClient(app)

class TestBookApi(TestCase):
    def test_get_all_books(self):
        response = client.get('/books')
        self.assertEqual(response.status_code, 200)
