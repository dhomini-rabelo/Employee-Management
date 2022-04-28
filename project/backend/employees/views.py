from datetime import datetime, timedelta, date
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from Fast.api.renderers import ApiWithSimpleDRFView
from Fast.django.decorators.cache.api import static_global_cache_page_renewable, dinamic_global_cache_page_renewable
from backend.employees.actions.objects.serializers import EmployeeSerializer
from backend.employees.app.models import Employee
from rest_framework.renderers import JSONRenderer
from django.utils.decorators import method_decorator
from django.db.models import Q, F, Avg
from django.db import models
from django.db.models import IntegerField, ExpressionWrapper, F, DateTimeField, FloatField, BigIntegerField



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


class AgeReportView(APIView):
    renderer_classes = [JSONRenderer, ApiWithSimpleDRFView]

    def get(self, request):
        now = datetime.now().date()
        employees_with_life_seconds = Employee.objects.annotate(life_seconds=(now - F('birth_date'))).order_by('life_seconds')
        younger, older =  employees_with_life_seconds.first(),  employees_with_life_seconds.last() # Employee or None
        average = employees_with_life_seconds.aggregate(average=Avg('life_seconds'))['average'] # timedelta or None

        response = {
            'younger': EmployeeSerializer(younger).data if younger else None, # None to json is null
            'older': EmployeeSerializer(older).data if older else None,
            'average': str(round(average.days / 365.25, 2)) if average else "0.00",
        }

        return Response(response)
