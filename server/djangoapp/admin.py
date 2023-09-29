from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    fields = ['name', 'description']
    search_fields = ['name']
    list_filter = ['name']
    list_display = ['name', 'description']
    inlines = [CarModelInline]

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ['name', 'dealer_id', 'type', 'year']
    search_fields = ['name', 'dealer_id', 'type']
    list_filter = ['name', 'dealer_id', 'type']
    list_display = ['name', 'dealer_id', 'type', 'year']

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)

# Register models here

