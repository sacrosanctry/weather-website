from django.contrib import admin

from weather_admin.models import Weather, City, Date, WeatherElement, MyUser, Role

# Register your models here.

class WeatherDisplay(admin.ModelAdmin):
    # fieldsets = [('date',{'fields':['date']}), ('name',{'fields':['city_id']})]
    list_display = ('city', 'date')

class MyUserDisplay(admin.ModelAdmin):
    list_display = ('username', 'name', 'is_staff')

admin.site.register(Weather, WeatherDisplay)
admin.site.register(City)
admin.site.register(Date)
admin.site.register(WeatherElement)
admin.site.register(MyUser, MyUserDisplay)
admin.site.register(Role)