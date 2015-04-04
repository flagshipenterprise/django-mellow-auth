from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.core.urlresolvers import reverse
from django_webtest import WebTest
from django.test import override_settings
from webtest import AppError
from accounts.mixins import MinimumRoleRequiredMixin
from accounts.roles import Role
from accounts.tests.factories import AccountFactory
from accounts.tests.views import (
    MinimumRoleRequiredView,
    InvalidMinimumRoleRequiredView,
)
from accounts.settings import DEFAULT_MELLOW_ROLES


class MinimumRoleRequiredMixinTestCase(WebTest):
    urls = 'accounts.tests.urls'

    @override_settings(MELLOW_ROLES=DEFAULT_MELLOW_ROLES)
    def setUp(self):
        self.user = AccountFactory.create(role='user')
        self.admin = AccountFactory.create(role='admin')
        self.superadmin = AccountFactory.create(role='superadmin')

    @override_settings(MELLOW_ROLES=DEFAULT_MELLOW_ROLES)
    def test_get_required_role(self):
        view = MinimumRoleRequiredView()
        self.assertTrue(view.get_required_role(), Role.get_role(slug='admin'))

    @override_settings(MELLOW_ROLES=DEFAULT_MELLOW_ROLES)
    def test_invalid_required_role_view(self):
        view = InvalidMinimumRoleRequiredView()
        self.assertRaisesMessage(
            ImproperlyConfigured,
            "Views which inherit from MinimumRoleRequiredMixin must have a \"role\" member.",
            view.get_required_role)

    @override_settings(MELLOW_ROLES=DEFAULT_MELLOW_ROLES)
    def test_bad_permissions(self):
        response = self.app.get(reverse('minimum-role-required'), user=self.user, status=403)

    @override_settings(MELLOW_ROLES=DEFAULT_MELLOW_ROLES)
    def test_equal_permissions(self):
        response = self.app.get(reverse('minimum-role-required'), user=self.admin, status=200)

    @override_settings(MELLOW_ROLES=DEFAULT_MELLOW_ROLES)
    def test_better_permissions(self):
        response = self.app.get(reverse('minimum-role-required'), user=self.superadmin, status=200)

    @override_settings(MELLOW_ROLES=DEFAULT_MELLOW_ROLES)
    def test_min_role_req_func_view(self):
        response = self.app.get(reverse('minimum-role-required-func'), user=self.superadmin, status=200)
        response = self.app.get(reverse('minimum-role-required-func'), user=self.admin, status=200)
        response = self.app.get(reverse('minimum-role-required-func'), user=self.user, status=403)
