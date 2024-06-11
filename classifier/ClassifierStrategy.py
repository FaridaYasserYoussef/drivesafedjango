from abc import ABC, abstractmethod
import keras
from .models import SegmentClass
from segmentor.models import Segment
import numpy as np
class ClassificationStrategy(ABC):
    @abstractmethod
    def classifyData(self, data, segment_id):
        model = keras.load_model(r"D:\FlutterProjects\graduationproject\drivesafedjango\drivesafedjango\media\ai_models\CNNFinalClassifier.keras")
        predicted_behavior  = model.predict(data)
        segment = Segment.objects.get(id = segment_id)
        if np.argmax(predicted_behavior) == 0:
            SegmentClass.objects.create(
              segment_id = segment,
              segment_class = "zigzag"
            )
        elif  np.argmax(predicted_behavior) == 1:
            SegmentClass.objects.create(
              segment_id = segment,
              segment_class = "sharpturn"
            )
        elif  np.argmax(predicted_behavior) == 2:
            SegmentClass.objects.create(
              segment_id = segment,
              segment_class = "suddenbraking"
            )
        elif  np.argmax(predicted_behavior) == 3:
            SegmentClass.objects.create(
              segment_id = segment,
              segment_class = "pothole"
            )

class FrameClassifierStrategy(ClassificationStrategy):
    def classifyData(self, data, segment_id):
        model = keras.load_model(r"D:\FlutterProjects\graduationproject\drivesafedjango\drivesafedjango\media\ai_models\CNN_LSTM_3.h5")
        predicted_behavior  = model.predict(data)
        segment = Segment.objects.get(id = segment_id)
        if np.argmax(predicted_behavior, axis= 2)[:, 0] == 0:
            SegmentClass.objects.create(
              segment_id = segment,
              segment_class = "Drinking"
            )
        elif  np.argmax(predicted_behavior, axis= 2)[:, 0] == 1:
            SegmentClass.objects.create(
              segment_id = segment,
              segment_class = "Eating"
            )
        elif  np.argmax(predicted_behavior, axis= 2)[:, 0] == 2:
            SegmentClass.objects.create(
              segment_id = segment,
              segment_class = "PhoneUse"
            )
        elif  np.argmax(predicted_behavior, axis= 2)[:, 0] == 3:
            SegmentClass.objects.create(
              segment_id = segment,
              segment_class = "NoHanded"
            )
        elif  np.argmax(predicted_behavior, axis= 2)[:, 0] == 4:
            SegmentClass.objects.create(
              segment_id = segment,
              segment_class = "OneHand"
            )
        elif  np.argmax(predicted_behavior, axis= 2)[:, 0] == 5:
            SegmentClass.objects.create(
              segment_id = segment,
              segment_class = "PhoneCall"
            )
        elif  np.argmax(predicted_behavior, axis= 2)[:, 0] == 6:
            SegmentClass.objects.create(
              segment_id = segment,
              segment_class = "Smoking"
            )
        elif  np.argmax(predicted_behavior, axis= 2)[:, 0] == 7:
            SegmentClass.objects.create(
              segment_id = segment,
              segment_class = "TwoHands"
            )
        




            
class SensorClassifierStrategy(ClassificationStrategy):
    def classifyData(self, data, segment_id):
        pass
        

class Classifier:
    def __init__(self, strategy: ClassificationStrategy = None):
        self._strategy = strategy

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: ClassificationStrategy):
        self._strategy = strategy

    def classify(self, data, segment_id):
        if not self._strategy:
            raise ValueError("Classification strategy not set")
        return self._strategy.classifyData(data, segment_id)

# # Example usage
# if __name__ == "__main__":
#     frame_classifier = FrameClassifierStrategy()
#     sensor_classifier = SensorClassifierStrategy()

#     classifier = Classifier(strategy=frame_classifier)
#     data = "frame data sample"
#     classified_data = classifier.classify(data)
#     print(classified_data)

#     classifier.strategy = sensor_classifier
#     data = "sensor data sample"
#     classified_data = classifier.classify(data)
#     print(classified_data)
