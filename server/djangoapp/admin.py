from django.contrib import admin
from .models import CarMake, CarModel
# from .models import related models


# Register your models here.

# CarModelInline class

class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1

# CarModelAdmin class
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

# CarMakeAdmin class with CarModelInline

admin.site.register(CarMake, CarMakeAdmin)

# Register models here


# Register your models here.

