from django.test import TestCase
from django.contrib.auth.models import User
from .models import Permission

class PermissionModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.permission = Permission.objects.create(user=self.user, level='admin')

    def test_permission_creation(self):
        self.assertEqual(self.permission.user.username, 'testuser')
        self.assertEqual(self.permission.level, 'admin')

    def test_permission_str(self):
        self.assertEqual(str(self.permission), 'testuser - admin')

    def test_user_permissions(self):
        self.assertIn(self.permission, self.user.permission_set.all())