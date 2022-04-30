from unittest import expectedFailure
from backend.employees.actions.objects.serializers import DepartmentSerializer, EmployeeSerializer
from ..support.main import BaseClassForTest, ViewBaseForTest
from django.test import Client
from ...models import Department, Employee



class DepartmentDetailViewTest(ViewBaseForTest):

    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)
        cls.client = Client()
        cls.create_user(cls, 'department_detail', '123456')
        cls.header = cls.get_default_header(cls)
        cls.path = f'/departments/{cls.department_1.id}/'
        cls.request = cls.client.get(cls.path, **cls.header)
        cls.valid_data = {
            'name': 'test'
        }

    def test_jwt_authentication(self):
        super().view_test_jwt_authentication()

    def test_status(self):
        self.assertEqual(self.request.status_code, 200) # 200 - OK

    def test_data(self):
        serializer = DepartmentSerializer(Department.objects.get(id=self.department_1.id))
        self.assertEqual(
            self.request.data,
            serializer.data
        )

    def test_put_method(self):
        data = self.valid_data.copy()
        request = self.client.put(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['name'], data['name'])

    def test_patch_method(self):
        data = {'name': 'patch'}
        request = self.client.patch(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['name'], data['name'])

    def test_delete_method(self):
        request = self.client.delete(f'/departments/{self.department_2.id}/', **self.header)
        self.assertEqual(request.status_code, 204) # 204 - NO CONTENT
