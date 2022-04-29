from datetime import datetime
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework import generics
from Fast.api.views.renderers import SimpleJsonApi
from Fast.django.decorators.cache.api import static_global_cache_page_renewable, dinamic_global_cache_page_renewable
from Fast.utils.main import d2
from backend.employees.actions.objects.serializers import EmployeeSerializer
from backend.employees.app.models import Employee
from rest_framework.renderers import JSONRenderer
from django.utils.decorators import method_decorator
from django.db.models import F, Avg


EMPLOYEE_CACHE_LIST = 'employee_cache' # data is renewed with signals post_save


class EmployeeCreateAndListView(generics.ListCreateAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.order_by('id')
    renderer_classes = [JSONRenderer]

    @method_decorator(static_global_cache_page_renewable(EMPLOYEE_CACHE_LIST))
    def get(self, request: HttpRequest):
        return super().get(request)    


class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.order_by('id')
    renderer_classes = [JSONRenderer]
    get_name_id = lambda request, pk : f'employee_{pk}'

    @method_decorator(dinamic_global_cache_page_renewable(EMPLOYEE_CACHE_LIST, 'employee_detail', get_name_id))
    def get(self, request: HttpRequest, pk: int):
        return super().get(request, pk)


class AgeReportView(SimpleJsonApi):

    @method_decorator(static_global_cache_page_renewable(EMPLOYEE_CACHE_LIST))
    def get(self, request):
        now = datetime.now().date()
        employees_with_life_seconds = Employee.objects.annotate(life_seconds=(now - F('birth_date'))).order_by('life_seconds')
        younger, older =  employees_with_life_seconds.first(),  employees_with_life_seconds.last() # Employee or None
        average = employees_with_life_seconds.aggregate(average=Avg('life_seconds'))['average'] # timedelta or None

        response = {
            'younger': EmployeeSerializer(younger).data if younger else None, # None to json is null
            'older': EmployeeSerializer(older).data if older else None,
            'average': d2(average.days / 365.25) if average else "0.00", # convert life seconds ( timedelta ) for years or return "0.00"
        }

        return Response(response)


class SalaryReportView(SimpleJsonApi):

    @method_decorator(static_global_cache_page_renewable(EMPLOYEE_CACHE_LIST))
    def get(self, request):
        employees = Employee.objects.order_by('-salary')
        lowest, highest = employees.last(), employees.first()
        average = employees.aggregate(average=Avg('salary'))['average'] # Decimal or None

        response = {
            'lowest': EmployeeSerializer(lowest).data if lowest else None,
            'highest': EmployeeSerializer(highest).data if highest else None,
            'average': d2(average) if average else "0.00",
        }

        return Response(response)