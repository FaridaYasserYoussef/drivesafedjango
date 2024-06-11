from .models import Trip
from segmentor.models import *
from classifier.models import *

def get_trip_scored_events(trip_id):
    try:
        trip = Trip.objects.get(id = trip_id)
        seg_type =  SegmentType.objects.get(id = 1)
        segments = Segment.objects.filter(trip_id = trip, Segment_type = seg_type)
        
        trip_events = []

        for segment in segments:
            class_event = SegmentClass.objects.get(segment_id = segment)
            trip_events.append(class_event.segment_class)
        

        counts = {
        'TwoHands': 0,
        'OneHand': 0,
        'Drinking': 0,
        'Smoking': 0,
        'Eating': 0,
        'PhoneCall': 0,
        'PhoneUse': 0,
        'NoHanded': 0
        }

        for item in trip_events:
            if item in counts:
                counts[item] += 1

# Step 3: Extract the counts in the specified order

        ordered_keys = ['TwoHands', 'OneHand', 'Drinking', 'Smoking', 'Eating', 'PhoneCall', 'PhoneUse', 'NoHanded']
        ordered_counts = [counts[key] for key in ordered_keys]

        model = joblib.load(r"D:\FlutterProjects\graduationproject\drivesafedjango\drivesafedjango\media\ai_models\linear_regression_model.joblib")
        assert len(ordered_counts) == 8

# Reshape ordered_counts into a 2D numpy array with shape (1, 8)
        input_data = np.array(ordered_counts).reshape(8, 1)

# Make predictions using the loaded model
        prediction = model.predict(input_data)[0]
        trip = Trip.objects.get(id = trip_id)
        TripScores.objects.create(
            trip_id = trip,
            tripScore = prediction
        )
        
        trip.sensorProcessed = True
        trip.videoProcessed = True

# Save the changes to the database
        trip.save()




        # return JsonResponse({'message': 'Events Fetched', 'success': True, 'eventData': trip_events}, status = 200)
    except Exception as e:
        pass
    #         error_message = traceback.format_exc()
    #         print(error_message)
    #         return JsonResponse({'message': 'An Error Occurred', 'success': False}, status=400)
    # else:
    #     return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)
