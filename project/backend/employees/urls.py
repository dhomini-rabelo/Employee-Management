from django.urls import path
from .views import (
    EmployeeCreateAndListView, DepartmentCreateAndListView, DepartmentDetailView,
    AgeReportView, EmployeeDetailView, SalaryReportView, home_page,
)


urlpatterns = [
    path('', home_page, name='home'),

    path('employees/', EmployeeCreateAndListView.as_view()),
    path('employees', EmployeeCreateAndListView.as_view()),
    
    path('departments/', DepartmentCreateAndListView.as_view()),
    path('departments', DepartmentCreateAndListView.as_view()),
    
    path('employees/<int:pk>/', EmployeeDetailView.as_view()),
    path('employees/<int:pk>', EmployeeDetailView.as_view()),
    
    path('departments/<int:pk>/', DepartmentDetailView.as_view()),
    path('departments/<int:pk>', DepartmentDetailView.as_view()),
    
    path('reports/employees/age/', AgeReportView.as_view()),
    path('reports/employees/age', AgeReportView.as_view()),

    path('reports/employees/salary/', SalaryReportView.as_view()),
    path('reports/employees/salary', SalaryReportView.as_view()),
]
