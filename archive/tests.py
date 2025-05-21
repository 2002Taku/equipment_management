from django.test import TestCase
from .models import Archive

class ArchiveModelTest(TestCase):

    def setUp(self):
        self.archive_item = Archive.objects.create(
            reason='Outdated equipment',
            equipment_id=1
        )

    def test_archive_creation(self):
        self.assertEqual(self.archive_item.reason, 'Outdated equipment')
        self.assertEqual(self.archive_item.equipment_id, 1)

    def test_archive_str(self):
        self.assertEqual(str(self.archive_item), 'Outdated equipment')  # Assuming __str__ method is defined in the model

    def test_archive_retrieval(self):
        retrieved_item = Archive.objects.get(id=self.archive_item.id)
        self.assertEqual(retrieved_item, self.archive_item)