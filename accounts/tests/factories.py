import factory
from accounts.roles import Role
from accounts.models import Account


class RoleFactory(factory.Factory):
    class Meta:
        # Ha! It's this factory produces nothing but role-models.
        # We should all look up to it.
        model = Role

    slug = factory.Sequence(lambda n: 'role%d' % n)
    name = factory.Sequence(lambda n: 'Role #%d' % n)
    parent = None


class AccountFactory(factory.DjangoModelFactory):
    class Meta:
        model = Account

    role = factory.SubFactory(RoleFactory)
    email = factory.Sequence(lambda n: 'user%d@gmail.com' % n)
    first_name = factory.Sequence(lambda n: 'First-%d' % n)
    last_name = factory.Sequence(lambda n: 'Last-%d' % n)
    password = factory.PostGenerationMethodCall('set_password', 'password')

    #@classmethod
    #def _create(cls, model_class, *args, **kwargs):
    #    manager = cls._get_manager(model_class)
    #    account = manager.create(*args, **kwargs)
    #    account.set_password('password')
    #    return account
