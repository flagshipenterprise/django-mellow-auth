from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from accounts.roles import Role


class MinimumRoleRequiredMixin(object):
    role = None

    def get_required_role(self):
        if self.role:
            return Role.get_role(slug=self.role)
        else:
            raise ImproperlyConfigured("Views which inherit from MinimumRoleRequiredMixin must have a \"role\" member.")

    def get_user_role(self, request):
        return Role.get_role(id=request.user.role)

    def dispatch(self, request, **kwargs):

        # Ensure that the user is authenticated
        if not user.is_authenticated():
            raise PermissionDenied

        # Get the required role and the user's role
        required_role = self.get_required_role()
        user_role = self.get_user_role()

        # Ensure that the user has correct permissions
        if not user_role.supersedes(requred_role):
            raise PermissionDenied

        # Execute the normal dispatch method
        return super(MinimumRoleRequiredMixin, self).dispatch(request, **kwargs)