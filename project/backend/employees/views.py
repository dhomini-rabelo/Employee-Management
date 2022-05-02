# this backend
from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from backend.employees.actions.objects.serializers import DepartmentSerializer, EmployeeSerializer
from backend.employees.actions.objects.views import (
        DetailViewWithAuthenticationAndEmployeeCache, SimpleApiWithAuthentication, 
        CreateAndListViewWithAuthenticationAndEmployeeCache, EMPLOYEE_CACHE_LIST
)
from backend.employees.app.models import Department, Employee
# django rest framework
from rest_framework.response import Response
# django
from django.utils.decorators import method_decorator
from django.db.models import F, Avg
# support
from Fast.django.decorators.cache.api import static_global_cache_page_renewable
from Fast.utils.main import d2
from datetime import datetime


@require_http_methods(['GET'])
def home_page(request):
    return render(request, 'pages/index.html')


class EmployeeCreateAndListView(CreateAndListViewWithAuthenticationAndEmployeeCache):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.order_by('id').select_related('department')


class DepartmentCreateAndListView(CreateAndListViewWithAuthenticationAndEmployeeCache):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.order_by('id')   


class EmployeeDetailView(DetailViewWithAuthenticationAndEmployeeCache):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.order_by('id').select_related('department')
    group_name = 'employee_detail' # not use space because is invalid character for cache key


class DepartmentDetailView(DetailViewWithAuthenticationAndEmployeeCache):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.order_by('id')
    group_name = 'department_detail' # not use space because is invalid character for cache key


class AgeReportView(SimpleApiWithAuthentication):

    @method_decorator(static_global_cache_page_renewable(EMPLOYEE_CACHE_LIST))
    def get(self, request: HttpRequest):
        now = datetime.now().date() # returns datetime.date obj
        f_expression = now - F('birth_date') # date_obj minus date_obj returns timedelta represented by DurationField
        employees_with_life_seconds = Employee.objects.annotate(life_seconds=f_expression).order_by('life_seconds')
        younger, older =  employees_with_life_seconds.first(),  employees_with_life_seconds.last() # Employee or None
        average = employees_with_life_seconds.aggregate(average=Avg('life_seconds'))['average'] # timedelta or None

        report = {
            'younger': EmployeeSerializer(younger).data if younger else None, # None to json is null
            'older': EmployeeSerializer(older).data if older else None,
            'average': d2(average.days / 365.25) if average else "0.00", # convert life seconds ( timedelta ) for years or return "0.00"
        }

        return Response(report)


class SalaryReportView(SimpleApiWithAuthentication):

    @method_decorator(static_global_cache_page_renewable(EMPLOYEE_CACHE_LIST))
    def get(self, request: HttpRequest):
        employees = Employee.objects.order_by('-salary')
        lowest, highest = employees.last(), employees.first() # Employee or None
        average = employees.aggregate(average=Avg('salary'))['average'] # Decimal or None

        report = {
            'lowest': EmployeeSerializer(lowest).data if lowest else None,
            'highest': EmployeeSerializer(highest).data if highest else None,
            'average': d2(average) if average else "0.00",
        }

        return Response(report)