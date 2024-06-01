from django.db import models

# Create your models here.

class Trip(models.Model):
    driver_id = models.IntegerField()
    vehicle_id = models.IntegerField()
    initial_lat = models.FloatField()
    initial_long = models.FloatField()
    last_lat = models.FloatField()
    last_long = models.FloatField()
    duration = models.IntegerField()
    distance = models.FloatField()
    csvPath = models.CharField(max_length=500)
    videoPath = models.CharField(max_length=500)
    sensorProcessed = models.BooleanField(default= False)
    videoProcessed = models.BooleanField(default= False)
    