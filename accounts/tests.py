from django.test import TestCase
from .models import CustomUser, Permission

class PermissionModelTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass', employee_id='999999', department='テスト部')
        self.permission = Permission.objects.create(user=self.user, permission_level='admin')

    def test_permission_creation(self):
        self.assertEqual(self.permission.user.username, 'testuser')
        self.assertEqual(self.permission.permission_level, 'admin')

    def test_permission_str(self):
        self.assertEqual(str(self.permission), 'testuser - admin')

    def test_user_permissions(self):
        self.assertIn(self.permission, self.user.permissions.all())