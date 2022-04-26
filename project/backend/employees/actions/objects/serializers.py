from rest_framework import serializers
from backend.employees.app.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        representation = super(EmployeeSerializer, self).to_representation(instance)
        representation['department'] = instance.department.name
        return representation    
    
    class Meta:
        model = Employee
        fields = 'id', 'name', 'email', 'department', 'salary', 'birth-date'