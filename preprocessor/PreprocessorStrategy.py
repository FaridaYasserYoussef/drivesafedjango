from abc import ABC, abstractmethod
import cv2
import numpy as np
import pandas as pd
from pykalman import KalmanFilter
import tensorflow
from tensorflow import keras




class Preprocessingstrategy(ABC):
    @abstractmethod
    def preprocessData(self, path):
        pass

class FramePreprocessorStrategy(Preprocessingstrategy):
    def preprocessData(self, path):
         # Open the video file
        cap = cv2.VideoCapture(path)

        # Get the total number of frames
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        frames = []

        if total_frames == 33:
            # Process all 33 frames
            for _ in range(33):
                ret, frame = cap.read()
                if ret:
                    # Resize the frame to 128x128
                    resized_frame = cv2.resize(frame, (128, 128))

                    # Normalize the frame by dividing by 255
                    normalized_frame = resized_frame / 255.0

                    # Append the processed frame to the list
                    frames.append(normalized_frame)
        elif total_frames > 33:
            # Calculate the start and end frame indices for the middle 33 frames
            start_frame = (total_frames - 33) // 2
            end_frame = start_frame + 33

            # Skip frames until the start_frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

            for _ in range(33):
                ret, frame = cap.read()
                if ret:
                    # Resize the frame to 128x128
                    resized_frame = cv2.resize(frame, (128, 128))

                    # Normalize the frame by dividing by 255
                    normalized_frame = resized_frame / 255.0

                    # Append the processed frame to the list
                    frames.append(normalized_frame)
                else:
                    break
        else:
            # Process all available frames
            for _ in range(total_frames):
                ret, frame = cap.read()
                if ret:
                    # Resize the frame to 128x128
                    resized_frame = cv2.resize(frame, (128, 128))

                    # Normalize the frame by dividing by 255
                    normalized_frame = resized_frame / 255.0

                    # Append the processed frame to the list
                    frames.append(normalized_frame)
                else:
                    break

            # Pad the frames with the last frame until they are 33 frames
            last_frame = frames[-1] if frames else np.zeros((128, 128, 3))  # Use a black frame if no frames are read
            while len(frames) < 33:
                frames.append(last_frame)

        cap.release()

        # Convert the list of frames to a NumPy array
        frames_array = np.array(frames)

        return frames_array


class SensorPreprocessorStrategy(Preprocessingstrategy):
    def preprocessData(self, path):
         # Read the CSV file without headers
        data = pd.read_csv(path)

        # Extract gyroscope data (second, third, fourth columns)
        gyroscope_data = data.iloc[:, 1:4].values

        # Extract accelerometer data (fifth, sixth, seventh columns)
        accelerometer_data = data.iloc[:, 4:7].values

        # Initialize Kalman Filter for accelerometer
        kf_acc = KalmanFilter(initial_state_mean=np.zeros(3), n_dim_obs=3)
        kf_acc = kf_acc.em(accelerometer_data, n_iter=5)
        smoothed_acc_data, _ = kf_acc.smooth(accelerometer_data)

        # Initialize Kalman Filter for gyroscope
        kf_gyro = KalmanFilter(initial_state_mean=np.zeros(3), n_dim_obs=3)
        kf_gyro = kf_gyro.em(gyroscope_data, n_iter=5)
        smoothed_gyro_data, _ = kf_gyro.smooth(gyroscope_data)

        # Combine smoothed accelerometer and gyroscope data
        smoothed_data = np.hstack((smoothed_gyro_data, smoothed_acc_data))

        return smoothed_data

class Preprocessor:
    def _init_(self, strategy: Preprocessingstrategy = None):
        self._strategy = strategy

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Preprocessingstrategy):
        self._strategy = strategy

    def preprocess(self, path):
        if not self._strategy:
            raise ValueError("Preprocessing strategy not set")
        return self._strategy.preprocessData(path)

# Example usage
# if name == "main":
#     # Creating different strategies
#     frame_preprocessor = FramePreprocessorStrategy()
#     sensor_preprocessor = SensorPreprocessorStrategy()

#     # Creating the context with a specific strategy
#     preprocessor = Preprocessor(strategy=frame_preprocessor)

#     # Using the context to segment data
#     data = "some_frame_data"
#     preprocessed_data =  preprocessor.preprocess(data)
#     print(preprocessed_data)

#     # Changing the strategy at runtime
#     preprocessor.strategy =sensor_preprocessor
#     data = "some_sensor_data"
#     preprocessed_data  =preprocessor.preprocess(data)
#     print(preprocessed_data )