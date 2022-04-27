from django.apps import AppConfig


class EmployeesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.employees.app'
    verbose_name = 'employees'
    label = 'employees'

    def ready(self):
        """
        Active signals in employees.app.signals
        """
        import backend.employees.app.signals
