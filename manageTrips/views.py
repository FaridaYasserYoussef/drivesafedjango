from django.shortcuts import render
from django.http import JsonResponse
from authentication.models import Driver
from authentication.models import Vehicle
# Create your views here.
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import sync_to_async
import json
import asyncio
import joblib
from .models import Driver, Trip, TripScores
from django.core.serializers import serialize
from django.db.models import Avg
from .models import Trip
from django.views.decorators.csrf import csrf_exempt
import traceback
from datetime import datetime
from django.shortcuts import render
from django.db.models import Avg
from .models import TripScores
from authentication.models import Driver
# trips/views.py
import json
from django.http import StreamingHttpResponse
from django.core.serializers import serialize
from .models import Trip, TripScores
import asyncio
from segmentor.models import Segment, SegmentType
from classifier.models import SegmentClass
import numpy as np
from segmentor.SegmentorStrategy import *
from preprocessor.PreprocessorStrategy import *
from classifier.ClassifierStrategy import *


@csrf_exempt
def trigger_trip_processing(request):
    if request.method == "POST":
        trip_id = request.POST.get("trip_id")
        driver_id = request.POST.get("driver_id")

        trip = Trip.objects.get(id = trip_id)

        frame_segmentor_strategy = FrameDataSegmentorStrategy()
        sensor_segmentor_strategy = SensorDataSegmentorStrategy()

        segmentor_frame = Segmentor(strategy=frame_segmentor_strategy)
        segmentor_sensor = Segmentor(strategy=sensor_segmentor_strategy)
        segmentor_frame.segment(trip.videoPath, trip_id, driver_id)
        segmentor_sensor.segment(trip.csvPath, trip_id, driver_id)

        frame_type = SegmentType.objects.get(id = 1)
        sensor_type = SegmentType.objects.get(id = 2)

        trip = Trip.objects.get(id = trip_id)
        frame_segments = Segment.objects.filter(trip_id = trip, Segment_type = frame_type)
        sensor_segments = Segment.objects.filter(trip_id = trip, Segment_type = sensor_type)

        frame_preprocessor_strategy = FramePreprocessorStrategy()
        sensor_preprocessor_strategy = SensorPreprocessorStrategy()

        frame_preprocessor =  Preprocessor(strategy = frame_preprocessor_strategy)
        sensor_preprocessor = Preprocessor(strategy =  sensor_preprocessor_strategy)


        frame_classifier_strategy = FrameClassifierStrategy()
        sensor_classifier_strategy = SensorClassifierStrategy()

        frame_classifier =  Classifier(strategy = frame_classifier_strategy)
        sensor_classifier = Classifier(strategy =  sensor_classifier_strategy)




        







@csrf_exempt
def get_trip_events(request):
    if request.method == 'POST':
        try:
            trip_id = request.POST.get('trip_id')
            trip = Trip.objects.get(id = trip_id)
            segments = Segment.objects.filter(trip_id = trip)
            
            trip_events = []

            for segment in segments:
                class_event = SegmentClass.objects.get(segment_id = segment)
                trip_events.append(class_event.segment_class)
            return JsonResponse({'message': 'Events Fetched', 'success': True, 'eventData': trip_events}, status = 200)
        except Exception as e:
            error_message = traceback.format_exc()
            print(error_message)
            return JsonResponse({'message': 'An Error Occurred', 'success': False}, status=400)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)

# @csrf_exempt
# def get_trip_scored_events(request):
#     if request.method == 'POST':
#         try:
#             trip_id = request.POST.get('trip_id')
#             trip = Trip.objects.get(id = trip_id)
#             seg_type =  SegmentType.objects.get(id = 1)
#             segments = Segment.objects.filter(trip_id = trip, Segment_type = seg_type)
            
#             trip_events = []

#             for segment in segments:
#                 class_event = SegmentClass.objects.get(segment_id = segment)
#                 trip_events.append(class_event.segment_class)
            

#             counts = {
#             'TwoHands': 0,
#             'OneHand': 0,
#             'Drinking': 0,
#             'Smoking': 0,
#             'Eating': 0,
#             'PhoneCall': 0,
#             'PhoneUse': 0,
#             'NoHanded': 0
#             }

#             for item in trip_events:
#                 if item in counts:
#                     counts[item] += 1

# # Step 3: Extract the counts in the specified order

#             ordered_keys = ['TwoHands', 'OneHand', 'Drinking', 'Smoking', 'Eating', 'PhoneCall', 'PhoneUse', 'NoHanded']
#             ordered_counts = [counts[key] for key in ordered_keys]

#             model = joblib.load(r"D:\FlutterProjects\graduationproject\drivesafedjango\drivesafedjango\media\ai_models\linear_regression_model.joblib")
#             assert len(ordered_counts) == 8

# # Reshape ordered_counts into a 2D numpy array with shape (1, 8)
#             input_data = np.array(ordered_counts).reshape(8, 1)

# # Make predictions using the loaded model
#             prediction = model.predict(input_data)[0]
#             trip = Trip.objects.get(id = trip_id)
#             TripScores.objects.create(
#                 trip_id = trip,
#                 tripScore = prediction
#             )
            
#             trip.sensorProcessed = True
#             trip.videoProcessed = True

#     # Save the changes to the database
#             trip.save()




#             # return JsonResponse({'message': 'Events Fetched', 'success': True, 'eventData': trip_events}, status = 200)
#         except Exception as e:
#             pass
#     #         error_message = traceback.format_exc()
#     #         print(error_message)
#     #         return JsonResponse({'message': 'An Error Occurred', 'success': False}, status=400)
#     # else:
#     #     return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
async def sse_stream(request, driver_id):
    async def event_stream(driver_id):
        while True:
            driver = await sync_to_async(Driver.objects.get)(id=driver_id)
            trips = await sync_to_async(list)(Trip.objects.filter(driver_id=driver))

            trip_list = []
            for trip in trips:
                trip_score = await sync_to_async(TripScores.objects.filter)(trip_id=trip)
                current_trip_score = ''
                if await sync_to_async(trip_score.exists)():
                    current_trip_score = str((await sync_to_async(trip_score.first)()).tripScore)

                # Fetch related fields asynchronously
                driver_id = await sync_to_async(lambda: trip.driver_id.id)()
                vehicle_id = await sync_to_async(lambda: trip.vehicle_id.id)()

                trip_list.append({
                    'id': str(trip.id),
                    'driver_id': str(driver_id),
                    'vehicle_id': str(vehicle_id),
                    'initial_lat': str(trip.initial_lat),
                    'initial_long': str(trip.initial_long),
                    'last_lat': str(trip.last_lat),
                    'last_long': str(trip.last_long),
                    'duration': str(trip.duration),
                    'distance': str(trip.distance),
                    'csvPath': trip.csvPath,
                    'videoPath': trip.videoPath,
                    'endTime': trip.endTime,
                    'startTime': trip.startTime,
                    'sensorProcessed': trip.sensorProcessed,
                    'videoProcessed': trip.videoProcessed,
                    'tripScore': current_trip_score
                })

            average_trip_score = ''
            trip_scores = await sync_to_async(TripScores.objects.filter)(driver_id=driver)
            if await sync_to_async(trip_scores.exists)():
                average_trip_score = str((await sync_to_async(trip_scores.aggregate)(Avg('tripScore')))['tripScore__avg'])

            trips_json = json.dumps(trip_list)
            print(trips_json)


            score = f'data: {json.dumps({"type": "string", "data": average_trip_score})}\n\n'
            trips_message = f'data: {json.dumps({"type": "trips", "data": trips_json})}\n\n'

            yield score
            yield trips_message

            await asyncio.sleep(1)

    return StreamingHttpResponse(event_stream(driver_id), content_type='text/event-stream')

@csrf_exempt
def save_trip(request):
    if request.method == 'POST':
        driver_id = request.POST.get('driver_id')
        vehicle_id = request.POST.get('vehicle_id')
        initial_lat = request.POST.get('initial_lat')
        initial_long = request.POST.get('initial_long')
        last_lat = request.POST.get('last_lat')
        last_long = request.POST.get('last_long')
        # duration = request.POST.get('duration')
        distance = request.POST.get('distance')
        csvPath = request.POST.get('csvPath')
        videoPath = request.POST.get('videoPath')
        endTime = request.POST.get('endTime')
        startTime = request.POST.get('startTime')

        start_time = datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S.%f")
        end_time = datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S.%f")

        # Calculate the difference between the two times
        time_difference = end_time - start_time

        # Extract the total number of seconds
        total_seconds = time_difference.total_seconds()

        # Calculate minutes and seconds
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        duration = str(round(minutes)) + ":" + str(round(seconds))

        try:
            # Create a new Driver instance
            driver = Driver.objects.get(id = driver_id)
            vehicle = Vehicle.objects.get(driver = driver)
            trip = Trip.objects.create(
                driver_id=driver,
                vehicle_id= vehicle,
                initial_lat= float(initial_lat),
                initial_long= float(initial_long),
                last_lat = float(last_lat),
                last_long = float(last_long),
                duration = duration,
                distance = float(distance),
                csvPath = csvPath,
                videoPath = videoPath,
                startTime = startTime,
                endTime = endTime
    
            )

            # Create a new Vehicle instance associated with the driver


            return JsonResponse({'message': 'Sign up successful', 'success': True})
        except Exception as e:
            print(str(e))
            return JsonResponse({'message': str(e), 'success': False}, status=400)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)



@csrf_exempt
def getAllDriverTrips(request):
    if request.method == "POST":
        driver_id = request.POST.get("driver_id")

        try:
            print("the driver id is ", driver_id)

            driver = Driver.objects.get(id = driver_id)
            trips = Trip.objects.filter(driver_id = driver)
            print(len(trips))
            trip_list = []


            for trip in trips:
                trip_score = TripScores.objects.filter( trip_id = trip)
                current_trip_score = ''
                if trip_score.exists():
                    current_trip_score = str(trip_score.tripScore)
                trip_list.append({
                'id' : str(trip.id),
                'driver_id':str(trip.driver_id.id),
                'vehicle_id' : str(trip.vehicle_id.id),
                'initial_lat' :str(trip.initial_lat),
                'initial_long' : str(trip.initial_long),
                'last_lat' : str(trip.last_lat),
                'last_long' : str(trip.last_long),
                'duration' : str(trip.duration),
                'distance' : str(trip.distance),
                'csvPath' : trip.csvPath,
                'videoPath':  trip.videoPath,
                'endTime' : trip.endTime,
                'startTime': trip.startTime,
                'sensorProcessed': trip.sensorProcessed,
                'videoProcessed': trip.videoProcessed,
                "tripScore": current_trip_score
    
                })
            return JsonResponse({'message': 'Trips Fetched', 'success': True, 'tripData': trip_list}, status = 200)
        except Exception as e:
            error_message = traceback.format_exc()
            print(error_message)
            return JsonResponse({'message': 'An Error Occurred', 'success': False}, status=400)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)