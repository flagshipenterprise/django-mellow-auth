from mellow.models import Account
from mellow.roles import Role
from mellow.settings import MELLOW_ADMIN_ROLE


class ImpersonateMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated():
            return

        user_role = Role.get_role(request.user.role)
        admin_role = Role.get_role(MELLOW_ADMIN_ROLE)
        if user_role.supersedes(admin_role):
            if '__impersonate' in request.GET:
                request.session['impersonate_id'] = int(request.GET['__impersonate'])
            elif '__unimpersonate' in request.GET:
                if 'impersonate_id' in request.session:
                    del request.session['impersonate_id']

            if 'impersonate_id' in request.session:
                request.impersonator = request.user
                request.user = Account.objects.get(pk=request.session['impersonate_id'])
