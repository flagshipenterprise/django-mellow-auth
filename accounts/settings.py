from django.conf import settings
from accounts.roles import Role

# Role tree
DEFAULT_MELLOW_ROLES = [
    ('superadmin', 'Super Administrator', ),
    ('admin', 'Administrator', 'superadmin'),
    ('user', 'User', 'admin'),
]
MELLOW_ROLES = getattr(settings, 'MELLOW_ROLES', DEFAULT_MELLOW_ROLES)
Role.set_roles(MELLOW_ROLES)

# Account creation role permission
MELLOW_MINIMUM_ACCOUNT_CREATE_ROLE = getattr(
    settings, 'MELLOW_MINIMUM_ACCOUNT_CREATE_ROLE', 'admin')
