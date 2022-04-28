from datetime import date
from unittest import expectedFailure
from .support.main import BaseClassForTest
from ..models import Department, Employee
from decimal import Decimal


class EmployeeModelTest(BaseClassForTest):

    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)

    @expectedFailure
    def test_name_error_for_max_size(self):
        self.employee_1.name = 'x' * 257
        self.employee_1.save()

    @expectedFailure
    def test_name_error_for_null_value(self):
        self.employee_1.name = None
        self.employee_1.save()

    @expectedFailure
    def test_email_error_for_max_size(self):
        self.employee_1.email = 'x' * 257
        self.employee_1.save()

    @expectedFailure
    def test_email_error_for_null_value(self):
        self.employee_1.email = None
        self.employee_1.save()

    @expectedFailure
    def test_salary_error_for_max_digits(self):
        self.employee_1.salary = Decimal('11111111111111111111111111110111111111110.99')
        self.employee_1.save()

    def test_str_method(self):
        self.assertEqual(str(self.employee_1), self.employee_1.name)

    def test_Department_with_null_value(self):
        self.employee_3.department = None
        self.employee_3.save()
        self.assertIs(self.employee_3.department, None)

    def test_change_value(self):
        new_value = 'new_value'
        self.employee_10.name = new_value
        self.employee_10.save()
        self.assertEqual(new_value, self.employee_10.name)

        new_value = 'new_value@email.com'
        self.employee_10.email = new_value
        self.employee_10.save()
        self.assertEqual(new_value, self.employee_10.email)

        self.employee_10.department = self.department_3
        self.employee_10.save()
        self.assertEqual(self.department_3, self.employee_10.department)

        new_value = Decimal('100.50')
        self.employee_10.salary = new_value
        self.employee_10.save()
        self.assertEqual(new_value, self.employee_10.salary)

        new_value = date(1999, 12, 31)
        self.employee_10.birth_date = new_value
        self.employee_10.save()
        self.assertEqual(new_value, self.employee_10.birth_date)

    def test_many_to_one_relationship_with_Department_model(self):
        self.assertTrue(isinstance(self.employee_1.department, Department))
