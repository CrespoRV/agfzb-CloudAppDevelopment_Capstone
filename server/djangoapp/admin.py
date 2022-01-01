from django.contrib import admin
from .models import CarMake,CarModel


# Register your models here.

admin.site.register(CarModel)
admin.site.register(CarMake)

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 3

class CarMakeModel(admin.ModelAdmin):
    fields = ('name','description','country_origin')
    inlines = [CarModelInline]


# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here
