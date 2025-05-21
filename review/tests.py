from django.test import TestCase
from .models import Review

class ReviewModelTest(TestCase):

    def setUp(self):
        self.review = Review.objects.create(
            comment="Great equipment!",
            rating=5,
            equipment_id=1  # Assuming an equipment with ID 1 exists
        )

    def test_review_creation(self):
        self.assertEqual(self.review.comment, "Great equipment!")
        self.assertEqual(self.review.rating, 5)

    def test_review_str(self):
        self.assertEqual(str(self.review), "Great equipment!")  # Assuming __str__ method is defined in the model

    def test_review_rating_range(self):
        with self.assertRaises(ValueError):
            Review.objects.create(comment="Bad equipment", rating=6, equipment_id=1)  # Rating should be between 1 and 5

    def test_review_related_equipment(self):
        self.assertEqual(self.review.equipment_id, 1)  # Check if the related equipment ID is correct