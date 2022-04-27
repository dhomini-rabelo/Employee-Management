from rest_framework import generics
from Fast.api.views.renderers import SimpleJsonApi
from backend.employees.actions.objects.serializers import EmployeeSerializer
from backend.employees.app.models import Employee


class EmployeeCreateAndListView(generics.ListCreateAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.order_by('id')
