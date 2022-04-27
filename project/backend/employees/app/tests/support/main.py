from django.test import TestCase, Client
from unittest import expectedFailure
from ...models import Department, Employee
from random import randint
from django.db.models import Model


class BaseClassForTest(TestCase):

    def create_models(self):
        # creating departments
        for counter in range(1, 4):
            new_department = Department.objects.create(name=f'test_department_{counter}')
            setattr(self, f'department_{counter}', new_department)

        # creating employees
        for counter in range(1, 11):
            employee_department = getattr(self, f'department_{randint(1, 3)}')
            new_employee = Employee.objects.create(
                name=f'test_employee_{counter}',
                email=f'test_employee_{counter}@ssys.com.br',
                department=employee_department,
                salary=f'{randint(1, 5000)}.00',
                birth_date=f'{randint(1975, 2005)}-{randint(1, 12)}-{randint(1, 28)}'
            )
            setattr(self, f'employee_{counter}', new_employee)