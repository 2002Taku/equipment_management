from django.db import models
from django.conf import settings
from inventory.models import Item
from datetime import timedelta, date

class Lending(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='lendings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    user_department = models.CharField(max_length=100)
    borrowed_at = models.DateField(auto_now_add=True)
    return_due_date = models.DateField()

    def save(self, *args, **kwargs):
        if not self.return_due_date:
            self.return_due_date = self.borrowed_at + timedelta(days=6)
        super().save(*args, **kwargs)

    def is_due_soon(self):
        return (self.return_due_date - date.today()).days <= 3

    def __str__(self):
        return f"{self.item.name} - {self.user_name}"