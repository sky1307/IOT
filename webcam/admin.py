from re import search
from django.contrib import admin
from .models import Student
# Register your models here.
class StudenInfo(admin.ModelAdmin):
    list_display = ['id', 'name', 'mssv', 'status', 'Class']
    list_filter = ['name']
    search_fields = ['mssv']
admin.site.register(Student, StudenInfo)