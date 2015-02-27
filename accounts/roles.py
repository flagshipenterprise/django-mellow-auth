

# Role class
class Role(object):

    # Static role data
    __roles = {}

    def __init__(self, slug, name, parent=None):
        self.slug = slug
        self.name = name
        self.parent = parent
        Role.__roles[self.slug] = self

    def __str__(self):
        return self.name

    def supersedes(self, other):
        """
        Returns true if this role has at least as many permissions as "other".
        This is dependent on the truth of two conditions: 1) self is at the
        same or higher level than other, and 2) that self can be crossed on a
        rootward traversal of the role heap.
        """
        parent = other
        while parent:
            if self is parent:
                return True
            parent = parent.parent
        return False

    @staticmethod
    def clear_roles():
        Role.__roles = {}

    @staticmethod
    def list_roles():
        return Role.__roles.keys()

    @staticmethod
    def get_role(slug):
        return Role.__roles[slug]

    @staticmethod
    def get_roles():
        return Role.__roles.items()

    @staticmethod
    def set_roles(config):
        """
        Takes a config list (like MELLOW_ROLES set in the settings.py file as
        according to the README), and builds up the list of Roles.
        """

        # Remove old roles
        Role.clear_roles()

        # Add new roles in
        for role_config in config:
            parent = None
            if len(role_config) > 2:
                parent = Role.get_role(role_config[2])
            role = Role(role_config[0], role_config[1], parent)
