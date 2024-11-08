import cv2
import math as m
import mediapipe as mp
import streamlit as st

# Helper functions for posture detection
def findDistance(x1, y1, x2, y2):
    return m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def findAngle(x1, y1, x2, y2):
    theta = m.acos((y2 - y1) * (-y1) / (m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))
    degree = int(180 / m.pi) * theta
    return degree

# Initialize Mediapipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Streamlit UI
st.title("Posture Detection with Camera")
camera_source = st.sidebar.selectbox("Select Camera Source", ["Default Camera", "External Camera 1"])
camera_index = 0 if camera_source == "Default Camera" else 1

# Run Detection
run_detection = st.checkbox("Run Posture Detection")

if run_detection:
    good_frames = 0
    bad_frames = 0

    # Open video capture with selected camera index
    cap = cv2.VideoCapture(camera_index)
    frame_window = st.image([])

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            st.warning("Unable to access camera.")
            break

        # Convert image for Mediapipe processing
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        keypoints = pose.process(image_rgb)

        # Check if pose landmarks are detected
        if keypoints.pose_landmarks:
            lm = keypoints.pose_landmarks
            lmPose = mp_pose.PoseLandmark

            h, w = image.shape[:2]
            
            # Extract relevant keypoints
            try:
                l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w)
                l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)
                r_shldr_x = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w)
                r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)
                l_ear_x = int(lm.landmark[lmPose.LEFT_EAR].x * w)
                l_ear_y = int(lm.landmark[lmPose.LEFT_EAR].y * h)
                l_hip_x = int(lm.landmark[lmPose.LEFT_HIP].x * w)
                l_hip_y = int(lm.landmark[lmPose.LEFT_HIP].y * h)

                # Calculate shoulder alignment
                offset = findDistance(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y)
                if offset < 100:
                    posture_text = f"Aligned: {int(offset)}"
                    color = (127, 255, 0)  # green
                else:
                    posture_text = f"Not Aligned: {int(offset)}"
                    color = (50, 50, 255)  # red

                # Calculate neck and torso inclination
                neck_inclination = findAngle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
                torso_inclination = findAngle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)

                if neck_inclination < 40 and torso_inclination < 10:
                    good_frames += 1
                    bad_frames = 0
                    color = (127, 233, 100)  # light green
                else:
                    bad_frames += 1
                    good_frames = 0
                    color = (50, 50, 255)  # red

                # Warning message if bad posture time exceeds 3 minutes (180 seconds)
                if (1 / cap.get(cv2.CAP_PROP_FPS)) * bad_frames > 180:
                    st.warning("Warning: Poor posture detected for over 3 minutes!")

                # Display feedback on the frame
                cv2.putText(image, posture_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                cv2.putText(image, f"Neck: {int(neck_inclination)} | Torso: {int(torso_inclination)}", 
                            (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                # Mark key points on the frame
                cv2.circle(image, (l_shldr_x, l_shldr_y), 7, (0, 255, 255), -1)
                cv2.circle(image, (l_ear_x, l_ear_y), 7, (0, 255, 255), -1)
                cv2.circle(image, (r_shldr_x, r_shldr_y), 7, (255, 0, 255), -1)
                cv2.circle(image, (l_hip_x, l_hip_y), 7, (0, 255, 255), -1)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), color, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), color, 4)

            except Exception as e:
                st.error(f"Error processing keypoints: {e}")

        # Display the frame in Streamlit
        frame_window.image(image, channels="BGR")

    cap.release()
