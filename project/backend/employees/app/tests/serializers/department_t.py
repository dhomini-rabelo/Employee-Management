from unittest import expectedFailure
from backend.employees.actions.objects.serializers import DepartmentSerializer, EmployeeSerializer
from ..support.main import BaseClassForTest
from ...models import Department, Employee
from decimal import Decimal


class DepartmentSerializerTest(BaseClassForTest):
    
    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)
        cls.serializer = DepartmentSerializer(instance=cls.department_1)
        cls.serializer_many = DepartmentSerializer(instance=Department.objects.all(), many=True)
        cls.valid_data_for_creation = {
            'name': 'test',
        }

    def test_default_creation(self):
        test_serializer = DepartmentSerializer(data=self.valid_data_for_creation)
        self.assertTrue(test_serializer.is_valid())

    def test_data_for_serializer(self):
        department_1 = {
            'id': self.department_1.id,
            'name': self.department_1.name           
        }
        self.assertEqual(self.serializer.data, department_1)

    def test_error_required_name_field(self):
        serializer = DepartmentSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual('This field is required.', str(serializer.errors['name'][0]))