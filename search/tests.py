from django.test import TestCase
from .models import Equipment

class EquipmentSearchTests(TestCase):

    def setUp(self):
        Equipment.objects.create(name="Laptop", description="A personal computer for mobile use.")
        Equipment.objects.create(name="Projector", description="A device that projects visual images.")

    def test_search_by_name(self):
        response = self.client.get('/search/', {'q': 'Laptop'})
        self.assertContains(response, "Laptop")
        self.assertNotContains(response, "Projector")

    def test_search_by_description(self):
        response = self.client.get('/search/', {'q': 'device'})
        self.assertContains(response, "Projector")
        self.assertContains(response, "Laptop")

    def test_empty_search(self):
        response = self.client.get('/search/', {'q': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No results found.")