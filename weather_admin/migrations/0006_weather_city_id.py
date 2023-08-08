# Generated by Django 4.0.3 on 2022-04-03 00:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weather_admin', '0005_alter_weather_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='weather',
            name='city_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='weather_admin.city'),
        ),
    ]
