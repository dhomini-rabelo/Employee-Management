from django.http import HttpRequest
from rest_framework import generics
from Fast.api.renderers import ApiWithSimpleDRFView
from Fast.django.decorators.cache.api import static_global_cache_page_renewable
from backend.employees.actions.objects.serializers import EmployeeSerializer
from backend.employees.app.models import Employee
from rest_framework.renderers import JSONRenderer
from django.utils.decorators import method_decorator


EMPLOYEE_CACHE_LIST = 'employee_cache'


class EmployeeCreateAndListView(generics.ListCreateAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.order_by('id')
    renderer_classes = [JSONRenderer, ApiWithSimpleDRFView]

    @method_decorator(static_global_cache_page_renewable(EMPLOYEE_CACHE_LIST)) # data is renewed with signals post_save
    def get(self, request: HttpRequest):
        return super().get(request)    
