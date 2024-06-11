import cv2
import numpy as np
from sklearn.cluster import KMeans
from keras.src.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from .models import Segment, SegmentType
from manageTrips.models import Trip
from authentication.models import Driver
import os
import numpy as np
import csv
import time
import cv2
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

# Function to extract features using a pre-trained CNN model
def extract_features(frame, model):
    # Preprocess the frame for the VGG16 model
    preprocessed_frame = preprocess_input(frame.astype(np.float32))
    # Expand dimensions to match VGG input shape (batch size of 1)
    preprocessed_frame = np.expand_dims(preprocessed_frame, axis=0)
    # Extract features from the last convolutional layer (block5_conv3) of VGG16
    features = model.predict(preprocessed_frame)
    return features.flatten()

# Function to read video and extract features from each frame
def extract_frame_features(video_path, model):
    cap = cv2.VideoCapture(video_path)
    features = []
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
        features.append(extract_features(frame, model))
    cap.release()
    return frames, np.array(features)

# Function to save segmented clips
def save_segmented_clips(video_path, frames, cluster_labels, trip_id, driver_id):
    # Ensure the 'segments' directory exists
    segments_dir = os.path.join(settings.MEDIA_ROOT, 'segments')
    if not os.path.exists(segments_dir):
        os.makedirs(segments_dir)

    for cluster_id in np.unique(cluster_labels):
        cluster_indices = np.where(cluster_labels == cluster_id)[0]
        start_frame = cluster_indices[0]
        end_frame = cluster_indices[-1]
        segmented_clip = frames[start_frame:end_frame + 1]
        timestamp = int(time.time())
     
        # File path for saving the segmented clip
        out_path = os.path.join(segments_dir, f'cluster_{cluster_id}_{timestamp}_{driver_id}_{trip_id}_segment.mp4')

        # VideoWriter to save the video
        out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), 30, (frames[0].shape[1], frames[0].shape[0]))
        
        for frame in segmented_clip:
            out.write(frame)
        out.release()
    
        trip = Trip.objects.get(id = trip_id)
        driver  =  Driver.objects.get(id =  driver_id)
        segtype = SegmentType.objects.get(id  = 1)
        Segment.objects.create(
            trip_id = trip,
            driver_id = driver,
            segment_path = out_path,
            Segment_type = segtype
        )


def csv2numpy(file_name):
    """Read multidimensional signal from file"""
    # Read data from file without skipping the header
    data = np.genfromtxt(file_name, delimiter=",")
    # Return all data including the header
    return data


def save_crops(file, length, discard_start, discard_end, trip_id, driver_id, padding_mode=None):
    """Return list with crops from file and save each crop to a CSV."""
    # Ensure the 'sensor_segments' directory exists
    segments_dir = os.path.join(settings.MEDIA_ROOT, 'sensor_segments')
    if not os.path.exists(segments_dir):
        os.makedirs(segments_dir)

   
    # Read from file
    signal = csv2numpy(file)
    # Crop start and end
    signal = signal[discard_start:(signal.shape[0] - discard_end)]
    windows, remainder = divmod(signal.shape[0], length)
    if padding_mode and remainder != 0:
        # Apply padding with given padding mode
        padding = length * (windows + 1) - signal.shape[0]
        signal = np.pad(signal, ((0, padding), (0, 0)), padding_mode)
    elif padding_mode is None:
        # Crop the end
        signal = signal[:(length * windows)]

    # Obtain crops from <discard_start> to <discard_end>
    for i in range(0, signal.shape[0], length):
        crop = signal[i:(i + length)]
        # crops.append([crop, class_])
        # Generate a unique file name using a timestamp and the crop index
        timestamp = int(time.time())
        crop_file_path = os.path.join(segments_dir, f'crop_{i//length}_{timestamp}_{driver_id}_{trip_id}.csv')
        with open(crop_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(crop)
        trip = Trip.objects.get(id = trip_id)
        driver  =  Driver.objects.get(id =  driver_id)
        segtype = SegmentType.objects.get(id  = 2)
        Segment.objects.create(
            trip_id = trip,
            driver_id = driver,
            segment_path = crop_file_path,
            Segment_type = segtype
        )
        
    

