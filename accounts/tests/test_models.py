from django.test import TestCase
from .factories import RoleFactory


class RoleTestCase(TestCase):

    def setUp(self):
        self.role_1 = RoleFactory.create()
        self.role_2 = RoleFactory.create(parent=self.role_1)
        self.role_3 = RoleFactory.create(parent=self.role_1)
        self.role_4 = RoleFactory.create(parent=self.role_3)

    def test_role_comparisons(self):

        # Self comparisons
        self.assertTrue(self.role_1.supersedes(self.role_1))
        self.assertTrue(self.role_2.supersedes(self.role_2))
        self.assertTrue(self.role_3.supersedes(self.role_3))
        self.assertTrue(self.role_4.supersedes(self.role_4))

        # Top down comparisons
        self.assertTrue(self.role_1.supersedes(self.role_2))
        self.assertTrue(self.role_1.supersedes(self.role_3))
        self.assertTrue(self.role_1.supersedes(self.role_4))
        self.assertTrue(self.role_3.supersedes(self.role_4))
        self.assertTrue(self.role_3.supersedes(self.role_4))

        # Horizontal comparisons
        self.assertFalse(self.role_2.supersedes(self.role_1))
        self.assertFalse(self.role_2.supersedes(self.role_3))
        self.assertFalse(self.role_2.supersedes(self.role_4))
        self.assertFalse(self.role_3.supersedes(self.role_1))
        self.assertFalse(self.role_3.supersedes(self.role_2))
        self.assertFalse(self.role_4.supersedes(self.role_1))
        self.assertFalse(self.role_4.supersedes(self.role_2))
        self.assertFalse(self.role_4.supersedes(self.role_3))
