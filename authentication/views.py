from lib2to3.pgen2.driver import Driver
from django.contrib.auth.models import User  # Assuming you are using Django's built-in User model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib

from .models import Vehicle, VehicleType

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
            user = User.objects.get(email=email, password=hashed_password)
            return JsonResponse({'message': 'Login successful'}, status = 200)
        except User.DoesNotExist:
            return JsonResponse({'message': 'Invalid credentials'}, status=400)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)


def sign_up(request):
    if request.method == 'POST':
        # Extract data from the POST request
        username = request.POST.get('username')
        email = request.POST.get('email')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        safety_score = request.POST.get('safety_score')
        license_plate = request.POST.get('license_plate')
        vehicle_type_id = request.POST.get('vehicle_type_id')

        # Hash the provided password using SHA-256 (optional)
        password = request.POST.get('password')
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            # Create a new Driver instance
            driver = Driver.objects.create(
                username=username,
                email=email,
                age=age,
                gender=gender,
                safety_score=safety_score,
                password=hashed_password
            )

            # Create a new Vehicle instance associated with the driver
            vehicle_type = VehicleType.objects.get(id=vehicle_type_id)
            vehicle = Vehicle.objects.create(
                license_plate=license_plate,
                type=vehicle_type,
                driver=driver.id
            )

            return JsonResponse({'message': 'Sign up successful'})
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)