# Generated by Django 5.0.3 on 2024-06-06 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manageTrips', '0002_trip_endtime_trip_strattime_alter_trip_driver_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trip',
            old_name='stratTime',
            new_name='startTime',
        ),
    ]