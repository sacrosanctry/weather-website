from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Weather(models.Model):
    id          = models.AutoField(primary_key=True, unique=True)
    city        = models.ForeignKey('City', on_delete=models.CASCADE, blank=True, null=True)
    date        = models.ForeignKey('Date', on_delete=models.CASCADE, blank=True, null=True)
    temperature = models.IntegerField(blank=True, null=True)
    weather     = models.ForeignKey('WeatherElement', on_delete=models.CASCADE, blank=True, null=True)
    humidity    = models.IntegerField(blank=True, null=True)

    @staticmethod
    def hottest_day(city_name):
        temp_max = Weather.objects.all().order_by('temperature').filter(city__name=city_name).last() # among all cities and weathers
        return temp_max

    @staticmethod
    def coolest_day(city_name):
        temp_min = Weather.objects.all().order_by('temperature').filter(city__name=city_name).first()
        return temp_min

    @staticmethod
    def temperature_gap(city_name):
        if Weather.hottest_day(city_name) != None and Weather.coolest_day(city_name) != None:
            gap = Weather.hottest_day(city_name).temperature - Weather.coolest_day(city_name).temperature
            return gap
        else:
            return None

    def __str__(self):
        return f"{self.city} {self.date}"


class City(models.Model):
    id   = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=30) # max_length = required
    def __str__(self):
        return self.name


class Date(models.Model):
    id   = models.AutoField(primary_key=True, unique=True)
    date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    def __str__(self):
        return f"{self.date}"


class WeatherElement(models.Model):
    id              = models.AutoField(primary_key=True, unique=True)
    weather_element = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.weather_element


class Role(models.Model):
    id        = models.AutoField(primary_key=True, unique=True)
    role_name = models.CharField(max_length=40, blank=True)
    def __str__(self):
        return self.role_name


class MyUser(User):
    name  = models.CharField(max_length=40, blank=True)
    roles = models.ManyToManyField('Role', blank=True, null=True)
    def __str__(self):
        return f"{self.username} {self.name} {self.is_staff}"