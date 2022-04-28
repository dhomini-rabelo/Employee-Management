from django.urls import path
from . import views


urlpatterns = [
    path('employees', views.EmployeeCreateAndListView.as_view()),
    path('employees/<int:pk>', views.EmployeeDetailView.as_view()),
    path('reports/employees/age', views.AgeReportView.as_view()),
]
