from django.contrib import admin
from .models import Employee, Department


admin.site.empty_value_display = 'NULL'


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = 'name', 'email', 'salary'
    list_display_links = 'name',
    list_per_page = 50
    list_select_related = False # use tuple, default is False
    ordering = 'name',
    search_fields = '^name', # ^ -> startswith, = -> iexact, @ ->	search, None -> icontains


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = 'id', 'name',
    list_display_links = 'name',
    list_per_page = 50
    list_select_related = False # use tuple, default is False
    ordering = 'name',
    search_fields = '^name', # ^ -> startswith, = -> iexact, @ ->	search, None -> icontains
