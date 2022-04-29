from unittest import expectedFailure
from Fast.utils.main import d2, if_none
from backend.employees.actions.objects.serializers import EmployeeSerializer
from ..support.main import BaseClassForTest, ViewBaseForTest
from django.test import Client
from ...models import Department, Employee
from django.db.models import F, Avg, Max, Min, Sum


class SalaryReportViewTest(ViewBaseForTest):

    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)
        cls.client = Client()
        cls.create_user(cls, 'salary_report', '123456')
        cls.header = cls.get_default_header(cls)
        cls.path = f'/reports/employees/salary/'
        cls.request = cls.client.get(cls.path, **cls.header)

    def test_jwt_authentication(self):
        super().view_test_jwt_authentication()

    def test_status(self):
        self.assertEqual(self.request.status_code, 200) # 200 - OK

    def test_data(self):
        employees = Employee.objects.all()
        report = employees.aggregate(max_salary=Max('salary'), min_salary=Min('salary'), average_salary=Avg('salary'))
        report['average_salary'] = if_none(report['average_salary'], "0.00")
        employee_highest = employees.filter(id=self.request.data['highest']['id']).first()
        employee_lowest = employees.filter(id=self.request.data['lowest']['id']).first()

        self.assertEqual(self.request.data['average'], d2(report['average_salary']))
        self.assertEqual(employee_highest.salary if employee_highest else None, report['max_salary'])
        self.assertEqual(employee_lowest.salary if employee_lowest else None, report['min_salary'])

