# Generated by Django 4.0.3 on 2022-04-17 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather_admin', '0010_weather_field_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weather',
            name='field_name',
        ),
    ]