from Fast.django.decorators.cache.controler import renew_global_cache
from .models import Employee
from django.db.models.signals import post_save


def renew_employee_apis_cache(sender, instance, created, **kwargs):
    renew_global_cache([
        '/employees',
    ])


post_save.connect(renew_employee_apis_cache, sender=Employee)