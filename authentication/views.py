from  .models import Driver
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib

from .models import Vehicle, VehicleType

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os


@csrf_exempt
def upload_video_data(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        file_name = default_storage.save(os.path.join('videos', file.name), ContentFile(file.read()))
        file_url = default_storage.url(file_name)
        return JsonResponse({'status': 'success', 'file_name': file_name, 'file_url': file_url})
    return JsonResponse({'status': 'failed'}, status=400)

@csrf_exempt
def upload_sensor_data(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        file_name = default_storage.save(os.path.join('uploads', file.name), ContentFile(file.read()))
        file_url = default_storage.url(file_name)
        return JsonResponse({'status': 'success', 'file_name': file_name, 'file_url': file_url})
    return JsonResponse({'status': 'failed'}, status=400)
@csrf_exempt
def edit_driver(request):
    if request.method == 'POST':
        # Get the new username and age from the POST request
        new_username = request.POST.get('username')
        new_age = request.POST.get('age')
        driver_id = request.POST.get("id")

        try:
            # Retrieve the driver by ID
            driver = Driver.objects.get(id=driver_id)
            
            # Update the driver's username and age
            if new_username:
                driver.username = new_username
            if new_age:
                driver.age = int(new_age)
            
            # Save the updated driver object
            driver.save()

            # Return the updated driver details in the response
            return JsonResponse({
                'message': 'Driver updated successfully',
                'success': True,
                'driverData': {
                    'id': str(driver.id),
                    'username': driver.username,
                    'email': driver.email,
                    'age': str(driver.age),
                    'gender': driver.gender,
                    'password': driver.password,
                    'safety_score': str(driver.safety_score),
                }
            }, status=200)

        except Driver.DoesNotExist:
            return JsonResponse({'message': 'Driver not found', 'success': False}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e), 'success': False}, status=400)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)


@csrf_exempt
def getVehicleByDriver(request):
    if request.method == 'POST':
        driver = request.POST.get('driver')

        try:
            # Query the database to find a user with the provided username and hashed password
            vehicle = Vehicle.objects.get(driver=driver)
            return JsonResponse({'message': 'Vehicle Found', 'success': True, "vehicleData": {
             "id": str(vehicle.id),
             "license_plate": vehicle.license_plate,
             "type": vehicle.type.type,
             "driver": vehicle.driver.id
            }}, status = 200)
        except Driver.DoesNotExist:
            return JsonResponse({'message': 'Invalid credentials', 'success': False}, status=400)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)
@csrf_exempt
def login(request):
    if request.method == 'POST':
        # Extract username and password from the POST request
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Hash the provided password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            # Query the database to find a user with the provided username and hashed password
            user = Driver.objects.get(email=email, password=hashed_password)
            return JsonResponse({'message': 'Login successful', 'success': True, "userData": {
             "id": str(user.id),
             "username": user.username,
             "email": user.email,
             "password": user.password,
             "age" : str(user.age),
             "gender": user.gender,
             "safety_score": str(user.safety_score)

            }}, status = 200)
        except Driver.DoesNotExist:
            return JsonResponse({'message': 'Invalid credentials', 'success': False}, status=400)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
def sign_up(request):
    if request.method == 'POST':
        # Extract data from the POST request
        username = request.POST.get('username')
        print(username)
        email = request.POST.get('email')
        print(email)
        age = request.POST.get('age')
        print(age)
        gender = request.POST.get('gender')
        print(gender)
        # safety_score = request.POST.get('safety_score')
        license_plate = request.POST.get('license_plate')
        print(license_plate)
        vehicle_type = request.POST.get('vehicle_type')
        print(vehicle_type)
        # Hash the provided password using SHA-256 (optional)
        password = request.POST.get('password')
        print(password)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        print(hashed_password)

        try:
            # Create a new Driver instance
            driver = Driver.objects.create(
                username=username,
                email=email,
                age=int(age),
                gender=gender,
                password=hashed_password
            )

            # Create a new Vehicle instance associated with the driver
            vehicle_type = VehicleType.objects.get(type=vehicle_type)
            print(vehicle_type.id)
            print(driver.id)
            vehicle = Vehicle.objects.create(
                license_plate=str(license_plate),
                type=vehicle_type,
                driver= driver
            )

            return JsonResponse({'message': 'Sign up successful', 'success': True})
        except Exception as e:
            print(str(e))
            return JsonResponse({'message': str(e), 'success': False}, status=400)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)

@csrf_exempt  
def validate_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        license_plate = request.POST.get('license_plate')
        
        try:
            # Check if any Driver or Vehicle object exists with the provided email or license plate
            driver_exists = Driver.objects.filter(email=email).exists()
            vehicle_exists = Vehicle.objects.filter(license_plate=license_plate).exists()
            
            if driver_exists or vehicle_exists:
                # If either a Driver or Vehicle object exists, return validation failure
                return JsonResponse({'message': 'Email or license plate is already in use', 'validated': False}, status=400)
            else:
                # If neither a Driver nor Vehicle object exists, return validation success
                return JsonResponse({'message': 'Validation successful', 'validated': True}, status=200)
        except Exception as e:
            return JsonResponse({'message': str(e), 'success': False}, status=400)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)