from django.test import TestCase, override_settings
from .factories import RoleFactory
from mellow.roles import Role
from mellow.settings import DEFAULT_MELLOW_ROLES


class SettingsTestCase(TestCase):
    @override_settings(MELLOW_ROLES=DEFAULT_MELLOW_ROLES)
    def test_default_settings(self):
        roles = Role.list_roles()
        self.assertEquals(len(roles), 3)
        self.assertTrue('superadmin' in roles)
        self.assertTrue('admin' in roles)
        self.assertTrue('user' in roles)
