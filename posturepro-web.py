import cv2
import time
import math as m
import mediapipe as mp
import streamlit as st
import numpy as np

def findDistance(x1, y1, x2, y2):
    dist = m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist

def findAngle(x1, y1, x2, y2):
    theta = m.acos((y2 - y1) * (-y1) / (m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))
    degree = int(180 / m.pi) * theta
    return degree

def sendWarning():
    # Implement your warning mechanism (e.g., sound alert or message display)
    st.warning("Warning: Bad posture detected for too long!")

# Initialize variables
good_frames = 0
bad_frames = 0

font = cv2.FONT_HERSHEY_SIMPLEX

blue = (255, 127, 0)
red = (50, 50, 255)
green = (127, 255, 0)
dark_blue = (127, 20, 0)
light_green = (127, 233, 100)
yellow = (0, 255, 255)
pink = (255, 0, 255)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

st.title("Posture Detection App")

# Create a placeholder for video frames
frame_placeholder = st.empty()

# Start the webcam
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    st.error("Error: Could not open video.")
    st.stop()

fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_size = (width, height)

# Main loop
while True:
    success, image = cap.read()
    if not success:
        st.error("Skipping empty frame.")
        continue  # Skip empty frames

    # Convert the image color space
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    keypoints = pose.process(image_rgb)

    # Check if pose landmarks are detected
    if not keypoints.pose_landmarks:
        cv2.putText(image, "No pose detected", (10, 30), font, 0.9, red, 2)
        frame_placeholder.image(image, channels="BGR", use_column_width=True)
        time.sleep(0.1)
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

        good_time = (1 / fps) * good_frames
        bad_time = (1 / fps) * bad_frames

        if bad_time > 180:
            sendWarning()

        if good_time > 0:
            cv2.putText(image, f'Good Posture Time: {round(good_time, 1)}s', (10, h - 20), font, 0.9, green, 2)
        else:
            cv2.putText(image, f'Bad Posture Time: {round(bad_time, 1)}s', (10, h - 20), font, 0.9, red, 2)

        # Draw landmarks and lines on the image
        cv2.circle(image, (l_shldr_x, l_shldr_y), 7, yellow, -1)
        cv2.circle(image, (l_ear_x, l_ear_y), 7, yellow, -1)
        cv2.circle(image, (r_shldr_x, r_shldr_y), 7, pink, -1)
        cv2.circle(image, (l_hip_x, l_hip_y), 7, yellow, -1)
        cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), color, 4)
        cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), color, 4)

    except Exception as e:
        st.error(f"Error: {e}")

    # Show the frame in Streamlit
    frame_placeholder.image(image, channels="BGR", use_column_width=True)
    time.sleep(1 / fps)

    # Exit condition: Press 'q' to stop the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
