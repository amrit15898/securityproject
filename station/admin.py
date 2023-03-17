from django.contrib import admin
from .models import Equation
# Register your models here.


class equation(admin.ModelAdmin):
    list_display = ['equation', 'created_on']

admin.site.register(Equation, equation)
