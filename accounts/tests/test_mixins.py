from django.test import TestCase, Client
from django.views.generic.base import View
from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from accounts.mixins import MinimumRoleRequiredMixin
from accounts.roles import Role


class TestView(MinimumRoleRequiredMixin, View):
    role = 'admin'


class TestInvalidView(MinimumRoleRequiredMixin, View):
    pass


class MinimumRoleRequiredMixinTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_required_role(self):
        view = TestView()
        self.assertTrue(view.get_required_role(), Role.get_role(slug='admin'))

    def test_invalid_required_role_view(self):
        view = TestInvalidView()
        self.assertRaisesMessage(
            ImproperlyConfigured,
            "Views which inherit from MinimumRoleRequiredMixin must have a \"role\" member.",
            view.get_required_role)
