from django.test import TestCase
from .models import CustomUser, Permission

class PermissionModelTests(TestCase):

    def setUp(self):
        # テスト用ユーザーと権限を作成
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass', employee_id='999999', department='テスト部')
        self.permission = Permission.objects.create(user=self.user, permission_level='admin')

    def test_permission_creation(self):
        # 権限作成テスト
        self.assertEqual(self.permission.user.username, 'testuser')
        self.assertEqual(self.permission.permission_level, 'admin')

    def test_permission_str(self):
        # __str__メソッドのテスト
        self.assertEqual(str(self.permission), 'testuser - admin')

    def test_user_permissions(self):
        # ユーザーから権限が参照できるかテスト
        self.assertIn(self.permission, self.user.permissions.all())