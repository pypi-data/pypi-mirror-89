from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from core_app.models import CreationModificationDateBase as basedate
from .managers import CustomUserManager
# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin, basedate):
    """Custom user model with email as the primary key"""

    email = models.EmailField(
        max_length=250, unique=True, null=False, blank=False)
    firstname = models.CharField(max_length=200, null=False, blank=False)
    lastname = models.CharField(max_length=200, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    objects = CustomUserManager()

    # see documentation to change;
    # https://docs.djangoproject.com/en/3.1/ref/models/instances/#model-instance-methods
    # https://www.django-rest-framework.org/api-guide/routers/#routing-for-extra-actions
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('customuser-me', )

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Return the first name plus the last name, with a space
        in between
        """
        full_name = '%s %s' % (self.firstname, self.lastname)
        return full_name.strip()

    def get_short_name(self):
        """
        Return the short name for the user.
        """
        return self.firstname

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this user.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)
