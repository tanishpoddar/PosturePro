import streamlit as st
import cv2
import time
import math as m
import mediapipe as mp
from io import BytesIO

# Function to calculate distance
def findDistance(x1, y1, x2, y2):
    dist = m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist

# Function to calculate angle
def findAngle(x1, y1, x2, y2):
    theta = m.acos((y2 - y1) * (-y1) / (m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))
    degree = int(180 / m.pi) * theta
    return degree

# Function to send a warning message
def sendWarning():
    st.warning("Warning: Bad posture detected for too long!")

# Initialize MediaPipe pose detection
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Set up the Streamlit page
st.set_page_config(page_title="PosturePro - Real-time Posture Detection", layout="wide")

# Title for the app
st.title("PosturePro - Real-Time Posture Detection System")

# Initialize the session state for video stream
if 'video_started' not in st.session_state:
    st.session_state.video_started = False

# Main loop
if __name__ == "__main__":

    # Start/Stop video button
    start_stop_button = st.button("Start/Stop Video", key="start_stop_video")
    
    if start_stop_button:
        st.session_state.video_started = not st.session_state.video_started
    
    if st.session_state.video_started:

        # Capture video from webcam using OpenCV
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            st.error("Error: Could not open video.")
            st.stop()

        # Get video frame rate
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Process frames in real-time
        good_frames = 0
        bad_frames = 0

        font = cv2.FONT_HERSHEY_SIMPLEX
        blue = (255, 127, 0)
        red = (50, 50, 255)
        green = (127, 255, 0)
        light_green = (127, 233, 100)

        frame_placeholder = st.empty()  # Placeholder for displaying frames

        while True:
            success, image = cap.read()
            if not success:
                st.write("Skipping empty frame.")
                continue

            # Convert the image to RGB for processing with Mediapipe
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            keypoints = pose.process(image_rgb)

            # Check if pose landmarks are detected
            if not keypoints.pose_landmarks:
                cv2.putText(image, "No pose detected", (10, 30), font, 0.9, red, 2)
                frame_placeholder.image(image, channels="BGR", use_column_width=True)
                continue

            lm = keypoints.pose_landmarks
            lmPose = mp_pose.PoseLandmark

            h, w = image.shape[:2]

            # Calculate relevant keypoints
            try:
                l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w)
                l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)
                r_shldr_x = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w)
                r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)
                l_ear_x = int(lm.landmark[lmPose.LEFT_EAR].x * w)
                l_ear_y = int(lm.landmark[lmPose.LEFT_EAR].y * h)
                l_hip_x = int(lm.landmark[lmPose.LEFT_HIP].x * w)
                l_hip_y = int(lm.landmark[lmPose.LEFT_HIP].y * h)

                offset = findDistance(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y)
                if offset < 100:
                    cv2.putText(image, str(int(offset)) + ' Aligned', (w - 150, 30), font, 0.9, green, 2)
                else:
                    cv2.putText(image, str(int(offset)) + ' Not Aligned', (w - 150, 30), font, 0.9, red, 2)

                neck_inclination = findAngle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
                torso_inclination = findAngle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)

                angle_text_string = f'Neck : {int(neck_inclination)}  Torso : {int(torso_inclination)}'

                if neck_inclination < 40 and torso_inclination < 10:
                    bad_frames = 0
                    good_frames += 1
                    color = light_green
                else:
                    good_frames = 0
                    bad_frames += 1
                    color = red

                cv2.putText(image, angle_text_string, (10, 30), font, 0.9, color, 2)

                # Time calculation for good and bad posture
                good_time = (1 / fps) * good_frames
                bad_time = (1 / fps) * bad_frames

                if bad_time > 180:
                    sendWarning()

                # Display time stats on screen
                if good_time > 0:
                    cv2.putText(image, f'Good Posture Time: {round(good_time, 1)}s', (10, h - 20), font, 0.9, green, 2)
                else:
                    cv2.putText(image, f'Bad Posture Time: {round(bad_time, 1)}s', (10, h - 20), font, 0.9, red, 2)

                # Draw landmarks and lines on the image
                cv2.circle(image, (l_shldr_x, l_shldr_y), 7, light_green, -1)
                cv2.circle(image, (l_ear_x, l_ear_y), 7, light_green, -1)
                cv2.circle(image, (r_shldr_x, r_shldr_y), 7, red, -1)
                cv2.circle(image, (l_hip_x, l_hip_y), 7, light_green, -1)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), color, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), color, 4)

            except Exception as e:
                st.write(f"Error: {e}")

            # Display the frame on the Streamlit app
            frame_placeholder.image(image, channels="BGR", use_column_width=True)

        cap.release()
        cv2.destroyAllWindows()

    else:
        st.write("Click the button above to start video stream.")