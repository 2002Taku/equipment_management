from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # 拡張ユーザーモデル。社員番号・部署を追加
    employee_id = models.CharField(max_length=6, unique=True, verbose_name="社員番号")
    department = models.CharField(max_length=100, verbose_name="所属部署")

    def is_admin(self):
        # 管理者判定（例：社員番号が1で始まる場合）
        return self.employee_id.startswith('1')

# class Permission(models.Model):
#     # 権限管理モデル
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='permissions')
#     permission_level = models.CharField(max_length=50)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.permission_level}"