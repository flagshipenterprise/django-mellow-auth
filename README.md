==================
Django Mellow Auth
==================

## Overview

A role/organization based user account system for Django. Conceived originally by DVColgan, and written by StettJawa.

## The Role Hierarchy

Roles are related to each other in a heap-like structure, which can be used as is, or redefined by the client program. If role `B` has a parent role `A`, then `A` has at least as many permissions as `B`, and we say `A > B`. So actions which are permissible to users with role `B` are also permissible to those with role `A`, but not necessarily vice versa. This structure is illustrated below.

      A
     /
    B


Now consider the following role structure.

      A
     / \
    B   C
       /
      D

The following hold: `A > B`, `A > C`, and `C > D`. However, lateral comparisons are not valid - that is, an action permissible to `B` may or may not necessarily be permissible to `C`, so there's no meaning to `B > C`, and C will be denied access to an action marked as `B` permissible, unless it is also marked as `C` or `D` permissible. Make sense? Good. Sorry 'bout the abstract terms.


## Defining Roles

In `settings.py` you can define the role hierarchy like so.

    MELLOW_ROLES = [
    #   (<role slug>, <verbose role name>, <role parent slug>)
        ('superadmin', 'Super Administrator', ),
        ('admin', 'Administrator', 'superadmin'),
        ('user', 'User', 'admin'),
    ]

Keep in mind that roles should be defined in order from highest permissions to lowest. Also, no more than ONE role can be created which does not have a parent role. There's always gotta be a big-daddy-admin to rule over all the other admins or they'd get out of hand.


## Organizations

User accounts are also categorized optionally by organization, if `MELLOW_ORGANIZATIONS = True` is in `settings.py`. When organizations are on, each account must belong to an organization.

