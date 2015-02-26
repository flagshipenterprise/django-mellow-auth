

# Role class
class Role(object):

    # Static role data
    __role_id = 0
    __roles_by_id = {}
    __roles_by_slug = {}

    def __init__(self, slug, name, parent=None):
        self.slug = slug
        self.name = name
        self.parent = parent
        self.id = Role.__role_id
        Role.__role_id = Role.__role_id + 1
        Role.__roles_by_id[self.id] = self
        Role.__roles_by_slug[self.slug] = self

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
        Role.__role_id = 0
        Role.__roles_by_id = {}
        Role.__roles_by_slug = {}

    @staticmethod
    def list_roles():
        return Role.__roles_by_slug.keys()

    @staticmethod
    def get_role(id=None, slug=None):
        role_id = id
        role_slug = slug
        if role_id:
            return Role.__roles_by_id[role_id]
        elif role_slug:
            return Role.__roles_by_slug[role_slug]
        return None

    @staticmethod
    def get_roles():
        return Role.__roles_by_id.items()

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
                parent = Role.get_role(slug=role_config[2])
            role = Role(role_config[0], role_config[1], parent)
