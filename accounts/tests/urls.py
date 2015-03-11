from django.conf.urls import patterns, include, url
from django.contrib import admin
from accounts.tests.views import (
    MinimumRoleRequiredView,
    InvalidMinimumRoleRequiredView,
    minimum_role_required_func_view,
)


urlpatterns = patterns(
    '',
    url(r'^minimum-role-required/$', MinimumRoleRequiredView.as_view(), name='minimum-role-required'),
    url(r'^minimum-role-required-func/$', minimum_role_required_func_view, name='minimum-role-required-func'),
    url(r'^invalid-minimum-role-required/$', InvalidMinimumRoleRequiredView.as_view(), name='invalid-minimum-role-required'),
)
