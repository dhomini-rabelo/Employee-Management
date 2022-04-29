from unittest import expectedFailure
from backend.employees.actions.objects.serializers import EmployeeSerializer
from ..support.main import BaseClassForTest, ViewBaseForTest
from django.test import Client
from ...models import Department, Employee



class EmployeeDetailViewTest(ViewBaseForTest):

    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)
        cls.client = Client()
        cls.create_user(cls, 'employee_detail', '123456')
        cls.header = cls.get_default_header(cls)
        cls.path = f'/employees/{cls.employee_1.id}/'
        cls.request = cls.client.get(cls.path, **cls.header)
        cls.valid_data = {
            'id': cls.employee_1.id,
            'name': cls.employee_1.name,
            'email': cls.employee_1.email,
            'department': cls.department_1.name,
            'salary': cls.employee_1.salary,
            'birth_date': cls.employee_1.birth_date,
        }

    def test_jwt_authentication(self):
        super().view_test_jwt_authentication()

    def test_status(self):
        self.assertEqual(self.request.status_code, 200) # 200 - OK

    def test_data(self):
        serializer = EmployeeSerializer(Employee.objects.get(id=self.employee_1.id))
        self.assertEqual(
            self.request.data,
            serializer.data
        )

    def test_put_method(self):
        data = self.valid_data.copy()
        data['name'] = 'new name'
        data['email'] = 'newname@email.test'
        request = self.client.put(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['name'], data['name'])
        self.assertEqual(request.data['email'], data['email'])

    def test_patch_method(self):
        data = {'salary': '1850.75', 'birth_date': '17-03-2003'}
        request = self.client.patch(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['salary'], data['salary'])
        self.assertEqual(request.data['birth_date'], data['birth_date'])

    def test_delete_method(self):
        request = self.client.delete(f'/employees/{self.employee_2.id}/', **self.header)
        self.assertEqual(request.status_code, 204) # 204 - NO CONTENT

    def test_error_is_required_in_put_method(self):
        data = self.valid_data.copy()
        del data['salary']
        del data['email']
        request = self.client.put(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual('This field is required.', str(request.data['salary'][0]))
        self.assertEqual('This field is required.', str(request.data['email'][0]))

    def test_put_error_department_not_found(self):
        data = self.valid_data.copy()
        data['department'] = 'name not exists'
        request = self.client.put(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400) # 400 - BAD REQUEST
        self.assertEqual(['Department not found'], request.data['department'])

    def test_put_error_invalid_email_1(self):
        data = self.valid_data.copy()
        data['email'] = 'test'
        request = self.client.put(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual('Enter a valid email address.', str(request.data['email'][0]))

    def test_put_error_invalid_email_2(self):
        data = self.valid_data.copy()
        data['email'] = 'test@'
        request = self.client.put(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual('Enter a valid email address.', str(request.data['email'][0]))

    def test_put_error_invalid_email_3(self):
        data = self.valid_data.copy()
        data['email'] = 'test@email'
        request = self.client.put(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual('Enter a valid email address.', str(request.data['email'][0]))

    def test_put_error_invalid_department_id(self):
        data = self.valid_data.copy()
        data['department'] = 1000000
        request = self.client.put(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual('Invalid pk "1000000" - object does not exist.', str(request.data['department'][0]))

    def test_put_error_invalid_salary_max_digits(self):
        data = self.valid_data.copy()
        data['salary'] = '150000000000000000000000000.55'
        request = self.client.put(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual('Ensure that there are no more than 20 digits in total.', str(request.data['salary'][0]))

    def test_put_error_invalid_salary_decimal_places_quantity(self):
        data = self.valid_data.copy()
        data['salary'] = '150.555'
        request = self.client.put(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual('Ensure that there are no more than 2 decimal places.', str(request.data['salary'][0]))

    def test_put_error_invalid_birth_date_format(self):
        data = self.valid_data.copy()
        data['birth_date'] = '17/03/2003'
        request = self.client.put(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual('Date has wrong format. Use one of these formats instead: DD-MM-YYYY, YYYY-MM-DD.', str(request.data['birth_date'][0]))

    def test_patch_error_department_not_found(self):
        data = {}
        data['department'] = 'name not exists'
        request = self.client.patch(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400) # 400 - BAD REQUEST
        self.assertEqual(['Department not found'], request.data['department'])

    def test_patch_error_invalid_email_1(self):
        data = {}
        data['email'] = 'test'
        request = self.client.patch(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual('Enter a valid email address.', str(request.data['email'][0]))

    def test_patch_error_invalid_email_2(self):
        data = {}
        data['email'] = 'test@'
        request = self.client.patch(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual('Enter a valid email address.', str(request.data['email'][0]))

    def test_patch_error_invalid_email_3(self):
        data = {}
        data['email'] = 'test@email'
        request = self.client.patch(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual('Enter a valid email address.', str(request.data['email'][0]))

    def test_patch_error_invalid_department_id(self):
        data = {}
        data['department'] = 1000000
        request = self.client.patch(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual('Invalid pk "1000000" - object does not exist.', str(request.data['department'][0]))

    def test_patch_error_invalid_salary_max_digits(self):
        data = {}
        data['salary'] = '150000000000000000000000000.55'
        request = self.client.patch(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual('Ensure that there are no more than 20 digits in total.', str(request.data['salary'][0]))

    def test_patch_error_invalid_salary_decimal_places_quantity(self):
        data = {}
        data['salary'] = '150.555'
        request = self.client.patch(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual('Ensure that there are no more than 2 decimal places.', str(request.data['salary'][0]))

    def test_patch_error_invalid_birth_date_format(self):
        data = {}
        data['birth_date'] = '17/03/2003'
        request = self.client.patch(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual('Date has wrong format. Use one of these formats instead: DD-MM-YYYY, YYYY-MM-DD.', str(request.data['birth_date'][0]))