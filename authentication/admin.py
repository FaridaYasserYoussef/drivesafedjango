from django.contrib import admin

from .models import Driver, Vehicle, AccountType, VehicleType

@admin.register(AccountType)
class AccountTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    pass

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    pass
