from django.db import models
from authentication.models import *
# Create your models here.

class Trip(models.Model):
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    initial_lat = models.FloatField()
    initial_long = models.FloatField()
    last_lat = models.FloatField()
    last_long = models.FloatField()
    duration = models.CharField(max_length=500)
    distance = models.FloatField()
    csvPath = models.CharField(max_length=500)
    videoPath = models.CharField(max_length=500)
    sensorProcessed = models.BooleanField(default= False)
    videoProcessed = models.BooleanField(default= False)
    startTime = models.CharField(max_length=500)
    endTime = models.CharField(max_length=500)


class TripScores(models.Model):
    trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE)
    tripScore = models.FloatField()

  

    