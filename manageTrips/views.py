from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from .models import Trip
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def save_trip(request):
    if request.method == 'POST':
        driver_id = request.POST.get('driver_id')
        vehicle_id = request.POST.get('vehicle_id')
        initial_lat = request.POST.get('initial_lat')
        initial_long = request.POST.get('initial_long')
        last_lat = request.POST.get('last_lat')
        last_long = request.POST.get('last_long')
        duration = request.POST.get('duration')
        distance = request.POST.get('distance')
        csvPath = request.POST.get('csvPath')
        videoPath = request.POST.get('videoPath')

        try:
            # Create a new Driver instance
            trip = Trip.objects.create(
                driver_id=int(driver_id),
                vehicle_id=int(vehicle_id),
                initial_lat= float(initial_lat),
                initial_long= float(initial_long),
                last_lat = float(last_lat),
                last_long = float(last_long),
                duration = int(duration),
                distance = float(distance),
                csvPath = csvPath,
                videoPath = videoPath
    
            )

            # Create a new Vehicle instance associated with the driver


            return JsonResponse({'message': 'Sign up successful', 'success': True})
        except Exception as e:
            print(str(e))
            return JsonResponse({'message': str(e), 'success': False}, status=400)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)
