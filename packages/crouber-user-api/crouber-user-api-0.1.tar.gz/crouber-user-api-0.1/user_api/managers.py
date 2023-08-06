from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):

    def _create_user(self, firstname, lastname, email, password,
                     is_active, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a user with given password and
        other details.
        """
        if not email:
            raise ValueError('Users must have an e-mail address')
        if not firstname:
            raise ValueError('Users must have a first name')
        if not lastname:
            raise ValueError('Users must have a last name')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            firstname=firstname,
            lastname=lastname,
            email=email,
            is_active=is_active,  # noqa: E501 - False upon registration until e-mail verified by user
            is_staff=is_staff,
            is_superuser=is_superuser,
            last_login=now
            # created_date=now
        )

        user.set_password(password)
        user.save()
        return user

    def create_user(self, firstname, lastname, email, password,
                    **extra_fields):
        """
        exposed method that handles creating a user
        """
        return self._create_user(firstname, lastname, email,
                                 password, True, False, False, **extra_fields)

    def create_superuser(self, firstname, lastname, email, password,
                         **extra_fields):
        """
        exposed method that handles creating a super user
        """
        user = self._create_user(firstname, lastname, email,
                                 password, True, True, True, **extra_fields)
        return user
