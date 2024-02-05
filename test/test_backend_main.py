import unittest
from fastapi.testclient import TestClient
from backend.main import app, reformateDate
from datetime import datetime


class TestExpenseUpload(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_reformate_date(self):
        reformatted_date = reformateDate("2022-01-01")
        self.assertEqual(reformatted_date, "01.01.2022")

    def test_upload_data_success(self):
        expenses_data = {
            "expenses": [
                {"description": "Test Expense 1", "date": "2022-01-01", "cost": 100.0},
                {"description": "Test Expense 2", "date": "2022-01-02", "cost": 150.0}
            ],
            "user_ids": "1,2",
            "user_shares": "50,50"
        }
        response = self.client.post("/upload-data/", json=expenses_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Data processed successfully", "output": "mock_output"})

    def test_upload_data_failure(self):
        expenses_data = {
            "expenses": [],
            "user_ids": "",
            "user_shares": ""
        }
        response = self.client.post("/upload-data/", json=expenses_data)
        self.assertEqual(response.status_code, 500)


if __name__ == '__main__':
    unittest.main()
