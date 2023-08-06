from django.db import models

# Create your models here.


class CreationModificationDateBase(models.Model):
    '''abstract class for creation and modification
    timestamps'''

    created_date = models.DateTimeField(
        "Created date",
        auto_now_add=True)
    modified_date = models.DateTimeField(
        "Last modified date",
        auto_now=True)

    class Meta:
        abstract = True
