from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    department = models.CharField(max_length=100, verbose_name="所属部署")

    def is_admin(self):
        # 管理者判定（例：社員番号が1で始まる場合）
        return self.username.startswith('1')

