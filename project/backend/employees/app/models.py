from django.db.models import (Model, CharField, DateTimeField, TextField, EmailField, ForeignKey, PositiveIntegerField, ImageField, RESTRICT, DecimalField, DateField, BooleanField, SET_NULL)


class Department(Model):
    name = CharField(max_length=256)

    def __str__(self):
        return self.name


class Employee(Model):
    name = CharField(max_length=256)
    email = EmailField(max_length=256)
    department = ForeignKey(to=Department, on_delete=SET_NULL, null=True, related_name='employees')
    salary = DecimalField(max_digits=20, decimal_places=2)
    birth_date = DateField()

    def __str__(self):
        return self.name
