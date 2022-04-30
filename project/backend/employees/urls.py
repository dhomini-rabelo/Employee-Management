from django.urls import path
from . import views


urlpatterns = [
    path('employees/', views.EmployeeCreateAndListView.as_view()),
    path('departments/', views.DepartmentCreateAndListView.as_view()),
    path('employees/<int:pk>/', views.EmployeeDetailView.as_view()),
    path('departments/<int:pk>/', views.DepartmentDetailView.as_view()),
    path('reports/employees/age/', views.AgeReportView.as_view()),
    path('reports/employees/salary/', views.SalaryReportView.as_view()),
]
