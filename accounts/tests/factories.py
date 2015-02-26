import factory
from accounts.roles import Role


class RoleFactory(factory.Factory):
    class Meta:
        # Ha! It's this factory produces nothing but role-models.
        # We should all look up to it.
        model = Role

    slug = factory.Sequence(lambda n: 'role%d' % n)
    name = factory.Sequence(lambda n: 'Role #%d' % n)
    parent = None
