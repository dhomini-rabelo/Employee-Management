from unittest import expectedFailure
from backend.employees.actions.objects.serializers import EmployeeSerializer
from .support.main import BaseClassForTest
from django.test import Client
from ..models import Department, Employee


class EmployeeListViewTest(BaseClassForTest):

    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)
        cls.client = Client()
        cls.path = '/employees'
        cls.request = cls.client.get(cls.path)
        cls.valid_data = {
            'name': 'test',
            'email': 'test@email.com',
            'department': cls.department_1.name,
            'salary': '1000.50',
            'birth_date': '17-03-2003',
        }

    def test_status(self):
        self.assertEqual(self.request.status_code, 200) # 200 - OK

    def test_data(self):
        serializer = EmployeeSerializer(Employee.objects.all(), many=True)
        self.assertEqual(
            self.request.data,
            serializer.data
        )

    def test_post_method(self):
        request = self.client.post(self.path, data=self.valid_data, content_type='application/json')
        self.assertEqual(request.status_code, 201) # 201 - CREATED

    def test_post_error_department_not_found(self):
        data = self.valid_data.copy()
        data['department'] = 'name not exists'
        request = self.client.post(self.path, data=data, content_type='application/json')
        self.assertEqual(request.status_code, 400) # 400 - BAD REQUEST
        self.assertEqual(['Department not found'], request.data['department'])

    def test_error_invalid_email_1(self):
        data = self.valid_data.copy()
        data['email'] = 'test'
        request = self.client.post(self.path, data=data, content_type='application/json')
        self.assertEqual(request.status_code, 400)
        self.assertEqual('Enter a valid email address.', str(request.data['email'][0]))

    def test_error_invalid_email_2(self):
        data = self.valid_data.copy()
        data['email'] = 'test@'
        request = self.client.post(self.path, data=data, content_type='application/json')
        self.assertEqual(request.status_code, 400)
        self.assertEqual('Enter a valid email address.', str(request.data['email'][0]))

    def test_error_invalid_email_3(self):
        data = self.valid_data.copy()
        data['email'] = 'test@email'
        request = self.client.post(self.path, data=data, content_type='application/json')
        self.assertEqual(request.status_code, 400)
        self.assertEqual('Enter a valid email address.', str(request.data['email'][0]))

    def test_error_invalid_department_id(self):
        data = self.valid_data.copy()
        data['department'] = 1000000
        request = self.client.post(self.path, data=data, content_type='application/json')
        self.assertEqual(request.status_code, 400)
        self.assertEqual('Invalid pk "1000000" - object does not exist.', str(request.data['department'][0]))

    def test_error_invalid_salary_max_digits(self):
        data = self.valid_data.copy()
        data['salary'] = '150000000000000000000000000.55'
        request = self.client.post(self.path, data=data, content_type='application/json')
        self.assertEqual(request.status_code, 400)
        self.assertEqual('Ensure that there are no more than 20 digits in total.', str(request.data['salary'][0]))

    def test_error_invalid_salary_decimal_places_quantity(self):
        data = self.valid_data.copy()
        data['salary'] = '150.555'
        request = self.client.post(self.path, data=data, content_type='application/json')
        self.assertEqual(request.status_code, 400)
        self.assertEqual('Ensure that there are no more than 2 decimal places.', str(request.data['salary'][0]))

    def test_error_invalid_birth_date_format(self):
        data = self.valid_data.copy()
        data['birth_date'] = '17/03/2003'
        request = self.client.post(self.path, data=data, content_type='application/json')
        self.assertEqual(request.status_code, 400)
        self.assertEqual('Date has wrong format. Use one of these formats instead: DD-MM-YYYY, YYYY-MM-DD.', str(request.data['birth_date'][0]))