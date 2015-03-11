from django.http import HttpResponse
from django.views.generic.base import View
from accounts.mixins import MinimumRoleRequiredMixin, minimum_role_required


class MinimumRoleRequiredView(MinimumRoleRequiredMixin, View):
    role = 'admin'

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')


class InvalidMinimumRoleRequiredView(MinimumRoleRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')


@minimum_role_required('admin')
def minimum_role_required_func_view(request, *args, **kwargs):
    return HttpResponse('Hello, World!')
