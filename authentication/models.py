from django.db import models
import hashlib
class AccountType(models.Model):
    type = models.CharField(max_length=100)

class VehicleType(models.Model):
    type = models.CharField(max_length=100)

class Driver(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    safety_score = models.FloatField(default=100)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE, default=1)
    password = models.CharField(max_length=64, default='')  # SHA-256 hashed password

    def set_password(self, password):
        # Hash the password using SHA-256 algorithm
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.password = hashed_password

    def check_password(self, password):
        # Check if the provided password matches the stored hashed password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return self.password == hashed_password

class Vehicle(models.Model):
    license_plate = models.CharField(max_length=20)
    type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)