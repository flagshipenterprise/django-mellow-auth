from django.test import TestCase
from .factories import RoleFactory
from accounts.roles import Role
from accounts.settings import DEFAULT_MELLOW_ROLES


class SettingsTestCase(TestCase):
    def test_default_settings(self):
        roles = Role.list_roles()
        self.assertEquals(len(roles), 3)
        self.assertTrue('superadmin' in roles)
        self.assertTrue('admin' in roles)
        self.assertTrue('user' in roles)
