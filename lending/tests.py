from django.test import TestCase
from .models import Lending

class LendingModelTest(TestCase):

    def setUp(self):
        self.lending = Lending.objects.create(
            item_name="Test Item",
            borrower="Test Borrower",
            due_date="2023-12-31",
            status="borrowed"
        )

    def test_lending_creation(self):
        self.assertEqual(self.lending.item_name, "Test Item")
        self.assertEqual(self.lending.borrower, "Test Borrower")
        self.assertEqual(self.lending.due_date, "2023-12-31")
        self.assertEqual(self.lending.status, "borrowed")

    def test_lending_str(self):
        self.assertEqual(str(self.lending), "Test Item borrowed by Test Borrower")