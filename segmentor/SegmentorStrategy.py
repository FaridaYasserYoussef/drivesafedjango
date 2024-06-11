from abc import ABC, abstractmethod
import cv2
import numpy as np
from sklearn.cluster import KMeans
import tensorflow
from tensorflow import keras
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import VGG16
from .helperFunctions import *


class SegmentationStrategy(ABC):
    @abstractmethod
    def segmentData(self, path, trip_id, driver_id):
        pass

class FrameDataSegmentorStrategy(SegmentationStrategy):
    def segmentData(self, path, trip_id, driver_id):
        model = VGG16(weights='imagenet', include_top=False)
        frames, frame_features = extract_frame_features(path, model)
        kmeans = KMeans(n_clusters=15)
        kmeans.fit(frame_features)
        cluster_labels = kmeans.labels_

    # Post-processing to merge adjacent frames in the same cluster
        merged_labels = np.copy(cluster_labels)
        for i in range(1, len(merged_labels)):
            if merged_labels[i] == merged_labels[i - 1]:
                merged_labels[i] = -1

        save_segmented_clips(path, frames, merged_labels, trip_id, driver_id)


class SensorDataSegmentorStrategy(SegmentationStrategy):
    def segmentData(self, path,  trip_id, driver_id):
        save_crops(path, 500, 50, 50, trip_id, driver_id)

class Segmentor:
    def __init__(self, strategy: SegmentationStrategy = None):
        self._strategy = strategy

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: SegmentationStrategy):
        self._strategy = strategy

    def segment(self, path,  trip_id, driver_id):
        if not self._strategy:
            raise ValueError("Segmentation strategy not set")
        return self._strategy.segmentData(path,  trip_id, driver_id)

# Example usage
# if __name__ == "__main__":
#     # Creating different strategies
#     frame_segmentor = FrameDataSegmentorStrategy()
#     sensor_segmentor = SensorDataSegmentorStrategy()

#     # Creating the context with a specific strategy
#     segmentor = Segmentor(strategy=frame_segmentor)

#     # Using the context to segment data
#     data = "some_frame_data"
#     segmented_data = segmentor.segment(data)
#     print(segmented_data)

#     # Changing the strategy at runtime
#     segmentor.strategy = sensor_segmentor
#     data = "some_sensor_data"
#     segmented_data = segmentor.segment(data)
#     print(segmented_data)
