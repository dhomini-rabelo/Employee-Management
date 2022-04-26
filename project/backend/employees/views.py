from rest_framework import generics
from backend.employees.actions.objects.serializers import EmployeeSerializer
from backend.employees.app.models import Employee


class ProductCreateAndListView(generics.ListCreateAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.order_by('name')