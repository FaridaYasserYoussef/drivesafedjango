from  .models import Driver
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