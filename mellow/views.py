from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, CreateView, UpdateView, RedirectView, TemplateView, View
from loantrac import settings
from loantrac.settings import ADMIN_EMAIL_SENDER
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import password_reset
from templated_email import send_templated_mail
from common.functions import get_object_or_None
from common.mixins import GETToFormInitialMixin
from mellow.models import Account
from mellow.settings import MELLOW_ADMIN_ROLE
from mellow.forms import (
    CreateUnactivatedAccountForm,
    AccountActivateForm,
    AccountUpdateForm,
    AccountChangePasswordForm,
)

from mellow.mixins import (
    MinimumRoleRequiredMixin,
)

from braces.views import LoginRequiredMixin


class AccountListView(
        LoginRequiredMixin,
        MinimumRoleRequiredMixin,
        ListView):
    model = Account
    role = MELLOW_ADMIN_ROLE
    context_object_name = 'accounts'


class AccountCreateView(
        LoginRequiredMixin,
        MinimumRoleRequiredMixin,
        GETToFormInitialMixin,
        CreateView):
    model = Account
    template_name = 'accounts/account_create.html'
    role = MELLOW_ADMIN_ROLE
    form_class = CreateUnactivatedAccountForm

    def get_success_url(self):
        return reverse('account_list')
        #if self.object.role == Account.CLIENT:
        #    return reverse('loanapplication_list_pending')
        #else:
        #    return reverse('account_list')

    def get_form_kwargs(self):
        kwargs = super(AccountCreateView, self).get_form_kwargs()
        kwargs['account'] = self.request.user
        kwargs['domain'] = settings.SITE_DOMAIN
        return kwargs


class AccountActivateView(UpdateView):
    model = Account
    template_name = 'accounts/account_activate.html'
    success_url = reverse_lazy('home')
    form_class = AccountActivateForm

    def get_object(self):
        return get_object_or_None(Account, activation_key=self.kwargs['activation_key'])

    def get_context_data(self, **kwargs):
        context = super(AccountActivateView, self).get_context_data(**kwargs)
        if self.object is None or self.object.has_usable_password():
            context['invalid_key'] = True
        return context

    def form_valid(self, form):
        self.object = form.save()
        account = authenticate(username=self.object.email,
                               password=self.request.POST['password1'])
        login(self.request, account)
        return super(AccountActivateView, self).form_valid(form)


class AccountResendActivationEmailView(
        LoginRequiredMixin,
        MinimumRoleRequiredMixin,
        RedirectView):
    model = Account
    permanent = False
    url = reverse_lazy('account_list')
    role = MELLOW_ADMIN_ROLE

    def post(self, request, *args, **kwargs):
        account = get_object_or_404(Account, pk=self.kwargs['pk'])
        account.send_activation_email(settings.SITE_DOMAIN)
        return super(AccountResendActivationEmailView, self).post(request, *args, **kwargs)


class AccountUpdateView(
        LoginRequiredMixin,
        MinimumRoleRequiredMixin,
        UpdateView):
    model = Account
    form_class = AccountUpdateForm
    role = MELLOW_ADMIN_ROLE

    def get_form_kwargs(self):
        kwargs = super(AccountUpdateView, self).get_form_kwargs()
        kwargs['account'] = self.request.user
        return kwargs


"""
class AccountChangePasswordView(
        LoginRequiredMixin,
        UpdateView):
    model = Account
    template_name = 'accounts/account_change_password.html'
    success_url = reverse_lazy('home')
    form_class = AccountChangePasswordForm

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return super(AccountChangePasswordView, self).form_valid(form)

class FeatureRequestView(
        LoginRequiredMixin,
        MinimumRoleRequiredMixin,
        TemplateView):
    template_name = 'feature_request.html'
    role = Account.EMPLOYEE
"""
