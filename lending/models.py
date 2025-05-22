from django.db import models
from django.conf import settings
from supplies.models import Item
from datetime import timedelta, date

class Lending(models.Model):
    # 貸出対象の備品
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='lendings')
    # 貸出したユーザー
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # ユーザー名（履歴用に保存）
    user_name = models.CharField(max_length=100)
    # ユーザーの所属部署（履歴用に保存）
    user_department = models.CharField(max_length=100)
    # 貸出日
    borrowed_at = models.DateField(auto_now_add=True)
    # 返却予定日
    return_due_date = models.DateField()

    def save(self, *args, **kwargs):
        # 返却予定日が未設定の場合は貸出日+6日で自動設定
        if not self.return_due_date:
            self.return_due_date = self.borrowed_at + timedelta(days=6)
        super().save(*args, **kwargs)

    def is_due_soon(self):
        # 返却予定日まで3日以内ならTrue
        return (self.return_due_date - date.today()).days <= 3

    def __str__(self):
        # 管理画面などでの表示用
        return f"{self.item.name} - {self.user_name}"