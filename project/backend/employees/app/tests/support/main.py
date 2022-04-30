from django.test import TestCase, Client
from unittest import expectedFailure
from backend.employees.app.signals import renew_employee_apis_cache
from ...models import Department, Employee
from random import randint
from django.db.models import Model
from decimal import Decimal
from datetime import date
from backend.accounts.app.models import User

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
                salary=Decimal(f'{randint(1, 5000)}.00'),
                birth_date=date(randint(1975, 2005), randint(1, 12), randint(1, 28))
            )
            setattr(self, f'employee_{counter}', new_employee)

    def adapt_date_number(self, number: int):
        return str(number) if number >= 10 else f'0{number}'



class ViewBaseForTest(BaseClassForTest):

    def view_test_jwt_authentication(self):
        request = self.client.get(self.path)
        self.assertEqual(request.status_code, 401) # 401 - UNAUTHORIZED

    def create_user(self, username, password):
        self.username, self.password = username, password
        user = User(username=self.username)
        user.set_password(self.password)
        user.save()

    def get_default_header(self):
        request = self.client.post('/token/', data={'username': self.username, 'password': self.password}, content_type='application/json')
        return {'content_type': 'application/json', 'HTTP_AUTHORIZATION': f'Bearer {request.data["access"]}'}

    @classmethod
    def tearDownClass(cls):
        # clear cache
        renew_employee_apis_cache(None, None, None)