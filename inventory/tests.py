from django.test import TestCase
from .models import Equipment

class EquipmentModelTest(TestCase):

    def setUp(self):
        Equipment.objects.create(name="Test Equipment", description="Test Description", category="Test Category", stock=10)

    def test_equipment_creation(self):
        equipment = Equipment.objects.get(name="Test Equipment")
        self.assertEqual(equipment.description, "Test Description")
        self.assertEqual(equipment.category, "Test Category")
        self.assertEqual(equipment.stock, 10)

    def test_equipment_stock_update(self):
        equipment = Equipment.objects.get(name="Test Equipment")
        equipment.stock = 5
        equipment.save()
        self.assertEqual(equipment.stock, 5)

    def test_equipment_str(self):
        equipment = Equipment.objects.get(name="Test Equipment")
        self.assertEqual(str(equipment), "Test Equipment")