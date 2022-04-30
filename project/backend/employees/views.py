# this backend
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


class EmployeeCreateAndListView(CreateAndListViewWithAuthenticationAndEmployeeCache):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.order_by('id').select_related('department')


class DepartmentCreateAndListView(CreateAndListViewWithAuthenticationAndEmployeeCache):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.order_by('id')   


class EmployeeDetailView(DetailViewWithAuthenticationAndEmployeeCache):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.order_by('id').select_related('department')
    group_name = 'employee_detail' # not use space


class DepartmentDetailView(DetailViewWithAuthenticationAndEmployeeCache):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.order_by('id')
    group_name = 'department_detail' # not use space


class AgeReportView(SimpleApiWithAuthentication):

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


class SalaryReportView(SimpleApiWithAuthentication):

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