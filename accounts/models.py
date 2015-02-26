from django.db import models
from accounts.roles import Role


class Account(models.Model):
    role = models.IntegerField(choices=Role.get_roles())
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    """
    is_superuser = models.BooleanField('superuser status', default=False,
        help_text='Designates that this user has all permissions without '
                  'explicitly assigning them.')
    groups = models.ManyToManyField(Group, verbose_name='groups',
        blank=True, help_text='The groups this user belongs to. A user will '
                                'get all permissions granted to each of '
                                'their groups.',
        related_name="user_set", related_query_name="user")

    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField(
        default=True,
        help_text='Designates whether this user should be treated as active. '
                  'Unselect this instead of deleting accounts.')

    date_joined = models.DateTimeField(default=timezone.now)

    activation_key = models.CharField(max_length=40, default=make_activation_key)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def is_employee(self):
        return (self.role == Account.EMPLOYEE or
                self.role == Account.ADMINISTRATOR)

    def is_administrator(self):
        return self.role == Account.ADMINISTRATOR

    def __unicode__(self):
        return self.get_full_name()

    def get_username(self):
        return self.email

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

    def send_activation_email(self, domain):
        if self.role == Account.CLIENT:
            applications = LoanApplication.objects.filter(client=self.client, status=LoanApplication.PENDING)
            total_documents = ApplicationDocument.objects.filter(application__client=self.client).count()

            send_templated_mail(
                template_name='new_client_password_link',
                from_email=ADMIN_EMAIL_SENDER,
                recipient_list=[self.email],
                context={
                    'domain': domain,
                    'account': self,
                    'applications': applications,
                    'total_documents': total_documents,
                }
            )
        else:
            send_templated_mail(
                template_name='new_user_password_link',
                from_email=ADMIN_EMAIL_SENDER,
                recipient_list=[self.email],
                context={
                    'domain': domain,
                    'account': self,
                }
            )
    """
