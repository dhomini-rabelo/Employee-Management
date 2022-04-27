from django.contrib.auth.models import AbstractUser
from django.utils.safestring import mark_safe
from django.db.models import (Model, CharField, DateTimeField, TextField, EmailField, ForeignKey, PositiveIntegerField, ImageField, RESTRICT, DecimalField, DateField, BooleanField)


class User(AbstractUser):
    name = CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.username

