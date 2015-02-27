from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from accounts.roles import Role


class MinimumRoleRequiredMixin(object):
    role = None

    def get_required_role(self):
        if self.role:
            return Role.get_role(self.role)
        else:
            raise ImproperlyConfigured("Views which inherit from MinimumRoleRequiredMixin must have a \"role\" member.")

    def get_user_role(self, request):
        return Role.get_role(request.user.role)

    def dispatch(self, request, **kwargs):

        # Ensure that the user is authenticated
        if not request.user.is_authenticated():
            raise PermissionDenied

        # Get the required role and the user's role
        required_role = self.get_required_role()
        user_role = self.get_user_role(request)

        if not user_role.supersedes(required_role):
            raise PermissionDenied

        # Execute the normal dispatch method
        return super(MinimumRoleRequiredMixin, self).dispatch(request, **kwargs)