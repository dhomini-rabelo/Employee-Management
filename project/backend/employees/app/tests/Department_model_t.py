from django.test import TestCase
from unittest import expectedFailure
from .support.main import BaseClassForTest
from ..models import Department, Employee


class DepartmentModelTest(BaseClassForTest):

    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)

    @expectedFailure
    def test_name_error_for_max_size(self):
        self.department_1 = 'x' * 257
        self.department_1.save()

    @expectedFailure
    def test_name_error_for_null_string(self):
        self.department_1 = ''
        self.department_1.save()

    def test_str_method(self):
        self.assertEqual(str(self.department_1), self.department_1.name)

    def test_many_to_one_relationship_with_Employee_model(self):
        self.assertEqual(list(self.department_1.employees.all()), list(Employee.objects.filter(department__id=self.department_1.id)))
        self.assertEqual(list(self.department_2.employees.all()), list(Employee.objects.filter(department__id=self.department_2.id)))
        self.assertEqual(list(self.department_3.employees.all()), list(Employee.objects.filter(department__id=self.department_3.id)))
