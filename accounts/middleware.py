from accounts.models import Account
from accounts.roles import Role
from accounts.settings import MELLOW_ADMIN_ROLE


class ImpersonateMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated() and Role.get_role(request.user.role).supercedes(MELLOW_ADMIN_ROLE):
            if '__impersonate' in request.GET:
                request.session['impersonate_id'] = int(request.GET['__impersonate'])
            elif '__unimpersonate' in request.GET:
                if 'impersonate_id' in request.session:
                    del request.session['impersonate_id']

            if 'impersonate_id' in request.session:
                request.impersonator = request.user
                request.user = Account.objects.get(pk=request.session['impersonate_id'])
