from django.urls import path
from . import views


urlpatterns = [
    path('employees', views.EmployeeCreateAndListView.as_view()),
]
