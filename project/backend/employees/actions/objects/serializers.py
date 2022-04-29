from django.http import QueryDict
from rest_framework import serializers
from backend.employees.app.models import Department, Employee
from rest_framework.fields import empty
from rest_framework.exceptions import ErrorDetail
from django.conf import settings


class EmployeeSerializer(serializers.ModelSerializer):
    # default format -> %Y-%m-%d
    birth_date = serializers.DateField(format=settings.DATE_FIELD_FORMAT_IN_API, input_formats=[settings.DATE_FIELD_FORMAT_IN_API, 'iso-8601'])

    def __init__(self, instance=None, data=empty, **kwargs):
        if (data is not empty) and (not isinstance(data, QueryDict)) and (isinstance(data.get('department'), str)):
            """
            This condition is used for create a new serializer with department field as string, also works with int type
            """
            department = Department.objects.filter(name__iexact=data['department']).first()
            data['department'] = department.id if department is not None else 0 # 0 is not possible id value
        return super().__init__(instance, data, **kwargs)

    @property
    def errors(self):
        if not hasattr(self, '_errors'):
            msg = 'You must call `.is_valid()` before accessing `.errors`.'
            raise AssertionError(msg)
        
        if self._errors.get('department') == [ErrorDetail(string='Invalid pk "0" - object does not exist.', code='does_not_exist')]:
            self._errors = {**self._errors, 'department': ['Department not found']}
        
        return self._errors

    def to_representation(self, instance: Employee):
        representation = super(EmployeeSerializer, self).to_representation(instance)
        representation['department'] = instance.department.name # default value for foreign key is id
        return representation    
    
    class Meta:
        model = Employee
        fields = 'id', 'name', 'email', 'department', 'salary', 'birth_date'