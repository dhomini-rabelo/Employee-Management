from Fast.django.decorators.cache.controler import renew_global_cache
from backend.employees.views import EMPLOYEE_CACHE_LIST
from django.core.cache import cache
from .models import Department, Employee
from django.db.models.signals import post_save, post_delete


def renew_employee_apis_cache(*args, **kwargs):
    employee_cache_list = cache.get(EMPLOYEE_CACHE_LIST) or []
    renew_global_cache(employee_cache_list)


post_save.connect(renew_employee_apis_cache, sender=Department)
post_delete.connect(renew_employee_apis_cache, sender=Department)
post_save.connect(renew_employee_apis_cache, sender=Employee)
post_delete.connect(renew_employee_apis_cache, sender=Employee)