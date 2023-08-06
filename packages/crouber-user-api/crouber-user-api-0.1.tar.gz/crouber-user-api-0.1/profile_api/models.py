from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="profile",
        related_query_name="profile"
    )
    middle_initial = models.CharField(max_length=1, blank=True, null=True)
    profile_name = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    phonenumber = PhoneNumberField(blank=True, null=True, unique=True)
    profile_image = models.ImageField(upload_to='', blank=True, null=True)
    profile_active = models.BooleanField(default=True)
    address1 = models.CharField(
        "Address line 1",
        max_length=1024,
        null=True,
        blank=True)
    address2 = models.CharField(
        "Address line 2",
        max_length=1024,
        null=True,
        blank=True)
    zip_code = models.CharField(
        "ZIP / Postal code",
        max_length=12,
        null=True,
        blank=True)
    city = models.CharField(
        "City",
        max_length=1024,
        null=True,
        blank=True)
    state = models.CharField(
        "State",
        max_length=100,
        null=True,
        blank=True)
    country = models.CharField(
        "Country",
        default="USA",
        max_length=100,
        null=True,
        blank=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

    def __str__(self):
        """Return the profile name for each instance
        which is the e-mail
        """
        return self.user.email

    def address(self):
        """Return the address name for each instance
        which is the full address
        """
        return "{0}, {1}, {2}, {3}, {4}, {5}".format(self.address1,
            self.address2, self.city, self.state,                  # noqa
            self.zip_code, self.country,)                          # noqa
