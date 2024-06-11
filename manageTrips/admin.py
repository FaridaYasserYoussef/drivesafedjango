from django.contrib import admin
from .models import Trip
# Register your models here.


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    pass