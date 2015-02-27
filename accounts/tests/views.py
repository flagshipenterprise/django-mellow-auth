from django.http import HttpResponse
from django.views.generic.base import View
from accounts.mixins import MinimumRoleRequiredMixin


class MinimumRoleRequiredView(MinimumRoleRequiredMixin, View):
    role = 'admin'

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')


class InvalidMinimumRoleRequiredView(MinimumRoleRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')
