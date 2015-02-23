import factory
from accounts.models import Role


class RoleFactory(factory.Factory):
    class Meta:
        # Ha! It's this factory produces nothing but role-models.
        # We should all look up to it.
        model = Role

    name = factory.Sequence(lambda n: 'Role #%d' % n)
    parent = None
