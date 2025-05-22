from django.db import models
from supplies.models import Item

class ArchiveItem(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='archive')
    archive_reason = models.TextField()
    archived_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item.name