from decimal import Decimal
from unittest import expectedFailure
from Fast.utils.main import d2, get_age, if_none
from backend.employees.actions.objects.serializers import EmployeeSerializer
from ..support.main import BaseClassForTest
from django.test import Client
from ...models import Department, Employee
from django.db.models import F, Avg, Max, Min, Sum


class AgeReportViewTest(BaseClassForTest):

    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)
        cls.client = Client()
        cls.path = f'/reports/employees/age/'
        cls.request = cls.client.get(cls.path)

    def test_status(self):
        self.assertEqual(self.request.status_code, 200) # 200 - OK

    def test_data(self):
        ages = []
        employees = Employee.objects.all()

        for employee in employees:
            age = get_age(employee.birth_date, False)
            ages.append(age)

        average = d2(sum(ages) / len(ages)) if len(ages) > 0 else "0.00"
        max_age = max(ages) if len(ages) > 0 else None
        min_age = min(ages) if len(ages) > 0 else None

        y_dt, o_dt = self.request.data['younger'], self.request.data['older']
        younger_age = get_age(Employee.objects.get(id=y_dt['id']).birth_date, False) if y_dt else y_dt
        older_age = get_age(Employee.objects.get(id=o_dt['id']).birth_date, False) if o_dt else o_dt


        self.assertEqual(older_age, max_age)
        self.assertEqual(younger_age, min_age)
        self.assertEqual(self.request.data['average'], average)

    