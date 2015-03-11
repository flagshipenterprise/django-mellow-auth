from django import forms
from accounts.models import Account
from accounts.roles import Role


class CreateUnactivatedAccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('email', 'first_name', 'last_name', 'role')

    def __init__(self, *args, **kwargs):
        super(CreateUnactivatedAccountForm, self).__init__(*args, **kwargs)
        self.fields['role'] = forms.ChoiceField(choices=Role.get_roles())

    def save(self, commit=True):
        instance = super(CreateUnactivatedAccountForm, self).save(commit=False)
        instance.set_unusable_password()
        instance.save(commit)

        instance.send_activation_email(self.domain)
        return instance


class AccountActivateForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        account = super(AccountActivateForm, self).save(commit=False)
        account.set_password(self.cleaned_data["password1"])
        if commit:
            account.save()
        return account


# Some duplication in this form
class AccountUpdateForm(forms.ModelForm):
    role = forms.ChoiceField(choices=Role.get_roles())

    class Meta:
        model = Account
        fields = ('email', 'first_name', 'last_name', 'role')

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account', None)
        super(AccountUpdateForm, self).__init__(*args, **kwargs)

        if self.account and hasattr(self.account, 'role'):
            # If you are not an admin you can't see roles
            if self.account.role < Account.ADMINISTRATOR:
                del self.fields['role']

            else:
                # If you are an administrator or up you can change roles for
                # appropriate level
                self.fields['role'].choices = [
                    choice for choice in self.fields['role'].choices
                    if choice[0] <= self.account.role
                ]
        else:
            raise Exception('You must provide an account to this form.')


class AccountChangePasswordForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('password1', 'password2')

    def clean_password2(self):

        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):

        # Save the provided password in hashed format
        account = super(AccountChangePasswordForm, self).save(commit=False)
        account.set_password(self.cleaned_data["password1"])
        if commit:
            account.save()
        return account
