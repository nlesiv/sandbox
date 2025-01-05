from django.contrib import admin

from empApp.models import Employee

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    #List the display columns to be dislayed in the ADmin CRUD section for the Employee model
    list_display = ['firstName', 'lastName', 'salary']

admin.site.register(Employee, EmployeeAdmin)
