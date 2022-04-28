from django.http import HttpRequest
from rest_framework import generics
from Fast.api.renderers import ApiWithSimpleDRFView
from Fast.django.decorators.cache.api import static_global_cache_page_renewable, dinamic_global_cache_page_renewable
from backend.employees.actions.objects.serializers import EmployeeSerializer
from backend.employees.app.models import Employee
from rest_framework.renderers import JSONRenderer
from django.utils.decorators import method_decorator


EMPLOYEE_CACHE_LIST = 'employee_cache' # data is renewed with signals post_save


class EmployeeCreateAndListView(generics.ListCreateAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.order_by('id')
    renderer_classes = [JSONRenderer, ApiWithSimpleDRFView]

    @method_decorator(static_global_cache_page_renewable(EMPLOYEE_CACHE_LIST))
    def get(self, request: HttpRequest):
        return super().get(request)    


class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.order_by('id')
    renderer_classes = [JSONRenderer, ApiWithSimpleDRFView]
    get_name_id = lambda request, pk : f'employee_{pk}'

    @method_decorator(dinamic_global_cache_page_renewable(EMPLOYEE_CACHE_LIST, 'employee_detail', get_name_id))
    def get(self, request: HttpRequest, pk: int):
        return super().get(request, pk)


