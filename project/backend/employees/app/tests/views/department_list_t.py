from unittest import expectedFailure
from backend.employees.actions.objects.serializers import DepartmentSerializer, EmployeeSerializer
from ..support.main import BaseClassForTest, ViewBaseForTest
from django.test import Client
from ...models import Department, Employee


class DepartmentListViewTest(ViewBaseForTest):

    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)
        cls.client = Client()
        cls.create_user(cls, 'department_list', '123456')
        cls.header = cls.get_default_header(cls)
        cls.path = '/departments/'
        cls.request = cls.client.get(cls.path, **cls.header)
        cls.valid_data = {
            'name': 'test',
        }

    def test_jwt_authentication(self):
        super().view_test_jwt_authentication()

    def test_status(self):
        self.assertEqual(self.request.status_code, 200) # 200 - OK

    def test_data(self):
        serializer = DepartmentSerializer(Department.objects.all(), many=True)
        self.assertEqual(
            self.request.data,
            serializer.data
        )

    def test_post_method(self):
        request = self.client.post(self.path, data=self.valid_data, **self.header)
        self.assertEqual(request.status_code, 201) # 201 - CREATED

    def test_error_required_name_field(self):
        request = self.client.post(self.path, data={}, **self.header)
        self.assertEqual('This field is required.', str(request.data['name'][0]))