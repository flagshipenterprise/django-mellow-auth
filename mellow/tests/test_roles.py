from django.test import TestCase, override_settings
from .factories import RoleFactory
from accounts.roles import Role
from accounts.settings import DEFAULT_MELLOW_ROLES


class RoleTestCase(TestCase):
    def setUp(self):
        Role.clear_roles()
        self.role_1 = RoleFactory.create()
        self.role_2 = RoleFactory.create(parent=self.role_1)
        self.role_3 = RoleFactory.create(parent=self.role_1)
        self.role_4 = RoleFactory.create(parent=self.role_3)

    @override_settings(MELLOW_ROLES=DEFAULT_MELLOW_ROLES)
    def test_get_roles(self):
        roles = Role.get_roles()
        self.assertEquals(len(roles), 4)
        self.assertTrue((self.role_1.slug, self.role_1) in roles)
        self.assertTrue((self.role_2.slug, self.role_2) in roles)
        self.assertTrue((self.role_3.slug, self.role_3) in roles)
        self.assertTrue((self.role_4.slug, self.role_4) in roles)

    @override_settings(MELLOW_ROLES=DEFAULT_MELLOW_ROLES)
    def test_list_roles(self):
        roles = Role.list_roles()
        self.assertEquals(len(roles), 4)
        self.assertTrue(self.role_1.slug in roles)
        self.assertTrue(self.role_2.slug in roles)
        self.assertTrue(self.role_3.slug in roles)
        self.assertTrue(self.role_4.slug in roles)

    @override_settings(MELLOW_ROLES=DEFAULT_MELLOW_ROLES)
    def test_set_roles(self):
        mellow_roles = [
            ('superadmin', 'Super Administrator'),
            ('admin', 'Administrator', 'superadmin'),
            ('user', 'User', 'admin'),
            ('client', 'Client', 'admin'),
        ]
        Role.set_roles(mellow_roles)
        roles = Role.list_roles()

        # Test role name list
        self.assertEquals(len(roles), 4)
        self.assertTrue('superadmin' in roles)
        self.assertTrue('admin' in roles)
        self.assertTrue('user' in roles)
        self.assertTrue('client' in roles)

        # Test role relationships
        self.assertEquals(Role.get_role(slug='superadmin').parent, None)
        self.assertEquals(Role.get_role(slug='admin').parent.slug, 'superadmin')
        self.assertEquals(Role.get_role(slug='user').parent.slug, 'admin')
        self.assertEquals(Role.get_role(slug='client').parent.slug, 'admin')

    @override_settings(MELLOW_ROLES=DEFAULT_MELLOW_ROLES)
    def test_role_comparisons(self):

        # Self comparisons
        self.assertTrue(self.role_1.supersedes(self.role_1))
        self.assertTrue(self.role_2.supersedes(self.role_2))
        self.assertTrue(self.role_3.supersedes(self.role_3))
        self.assertTrue(self.role_4.supersedes(self.role_4))

        # Top-down comparisons
        self.assertTrue(self.role_1.supersedes(self.role_2))
        self.assertTrue(self.role_1.supersedes(self.role_3))
        self.assertTrue(self.role_1.supersedes(self.role_4))
        self.assertTrue(self.role_3.supersedes(self.role_4))
        self.assertTrue(self.role_3.supersedes(self.role_4))

        # Horizontal and bottom-up comparisons
        self.assertFalse(self.role_2.supersedes(self.role_1))
        self.assertFalse(self.role_2.supersedes(self.role_3))
        self.assertFalse(self.role_2.supersedes(self.role_4))
        self.assertFalse(self.role_3.supersedes(self.role_1))
        self.assertFalse(self.role_3.supersedes(self.role_2))
        self.assertFalse(self.role_4.supersedes(self.role_1))
        self.assertFalse(self.role_4.supersedes(self.role_2))
        self.assertFalse(self.role_4.supersedes(self.role_3))
