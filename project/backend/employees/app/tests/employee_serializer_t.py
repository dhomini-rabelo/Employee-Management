from unittest import expectedFailure
from backend.employees.actions.objects.serializers import EmployeeSerializer
from .support.main import BaseClassForTest
from ..models import Department, Employee
from decimal import Decimal


class EmployeeSerializerTest(BaseClassForTest):
    
    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)
        cls.serializer = EmployeeSerializer(instance=cls.employee_1)
        cls.serializer_many = EmployeeSerializer(instance=Employee.objects.all(), many=True)
        cls.valid_data_for_creation = {
            'name': 'test',
            'email': 'test@test.com',
            'department': cls.department_1.id, # or cls.department_1.name
            'salary': '1000.50',
            'birth_date': '17-03-2003'
        }

    def test_default_creation(self):
        test_serializer = EmployeeSerializer(data=self.valid_data_for_creation)
        self.assertTrue(test_serializer.is_valid())

    def test_creation_with_department_using_department_name(self):
        data = self.valid_data_for_creation.copy()
        data['department'] = self.department_1.name
        test_serializer = EmployeeSerializer(data=data)
        self.assertTrue(test_serializer.is_valid())

    def test_representation(self):
        self.assertEqual(self.serializer.data['department'], self.employee_1.department.name)

    def test_data_for_serializer(self):
        employee_1 = {
            'id': self.employee_1.id,
            'name': self.employee_1.name,
            'email': self.employee_1.email,
            'department': self.employee_1.department.name,
            'salary': str(self.employee_1.salary),
            'birth_date': f'{self.adapt_date_number(self.employee_1.birth_date.day)}-{self.adapt_date_number(self.employee_1.birth_date.month)}-{self.employee_1.birth_date.year}',
        }
        self.assertEqual(self.serializer.data, employee_1)

    def test_error_department_not_found(self):
        data = self.valid_data_for_creation.copy()
        data['department'] = 'name not exists'
        test_serializer = EmployeeSerializer(data=data)
        self.assertFalse(test_serializer.is_valid())
        self.assertEqual(['Department not found'], test_serializer.errors['department'])

    def test_error_invalid_email_1(self):
        data = self.valid_data_for_creation.copy()
        data['email'] = 'test'
        test_serializer = EmployeeSerializer(data=data)
        self.assertFalse(test_serializer.is_valid())
        self.assertEqual('Enter a valid email address.', str(test_serializer.errors['email'][0]))

    def test_error_invalid_email_2(self):
        data = self.valid_data_for_creation.copy()
        data['email'] = 'test@'
        test_serializer = EmployeeSerializer(data=data)
        self.assertFalse(test_serializer.is_valid())
        self.assertEqual('Enter a valid email address.', str(test_serializer.errors['email'][0]))

    def test_error_invalid_email_3(self):
        data = self.valid_data_for_creation.copy()
        data['email'] = 'test@email'
        test_serializer = EmployeeSerializer(data=data)
        self.assertFalse(test_serializer.is_valid())
        self.assertEqual('Enter a valid email address.', str(test_serializer.errors['email'][0]))

    def test_error_invalid_department_id(self):
        data = self.valid_data_for_creation.copy()
        data['department'] = 1000000
        test_serializer = EmployeeSerializer(data=data)
        self.assertFalse(test_serializer.is_valid())
        self.assertEqual('Invalid pk "1000000" - object does not exist.', str(test_serializer.errors['department'][0]))

    def test_error_invalid_salary_max_digits(self):
        data = self.valid_data_for_creation.copy()
        data['salary'] = '150000000000000000000000000.55'
        test_serializer = EmployeeSerializer(data=data)
        self.assertFalse(test_serializer.is_valid())
        self.assertEqual('Ensure that there are no more than 20 digits in total.', str(test_serializer.errors['salary'][0]))

    def test_error_invalid_salary_decimal_places_quantity(self):
        data = self.valid_data_for_creation.copy()
        data['salary'] = '150.555'
        test_serializer = EmployeeSerializer(data=data)
        self.assertFalse(test_serializer.is_valid())
        self.assertEqual('Ensure that there are no more than 2 decimal places.', str(test_serializer.errors['salary'][0]))

    def test_error_invalid_birth_date_format(self):
        data = self.valid_data_for_creation.copy()
        data['birth_date'] = '17/03/2003'
        test_serializer = EmployeeSerializer(data=data)
        self.assertFalse(test_serializer.is_valid())
        self.assertEqual('Date has wrong format. Use one of these formats instead: DD-MM-YYYY, YYYY-MM-DD.', str(test_serializer.errors['birth_date'][0]))
