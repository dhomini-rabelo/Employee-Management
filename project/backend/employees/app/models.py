from django.db.models import (Model, CharField, DateTimeField, TextField, EmailField, ForeignKey, PositiveIntegerField, ImageField, RESTRICT, DecimalField, DateField, BooleanField, SET_NULL)


class Department(Model):
    name = CharField(max_length=256, verbose_name='Nome')

    def __str__(self):
        return self.name


class Employee(Model):
    name = CharField(max_length=256, verbose_name='Nome')
    email = EmailField(max_length=256)
    department = ForeignKey(to=Department, on_delete=SET_NULL, null=True, related_name='employees', verbose_name='Departamento')
    salary = DecimalField(max_digits=20, decimal_places=2, verbose_name='Salário')
    birth_date = DateField(verbose_name='Data de nascimento')

    def __str__(self):
        return self.name
