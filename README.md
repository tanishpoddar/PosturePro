# PosturePro: Real-Time Posture Detection System

PosturePro is a real-time posture detection tool designed to help users maintain healthy posture by identifying and alerting them to poor posture. Built using a webcam and computer vision techniques, this tool tracks key body points to analyze alignment and provides feedback, making it ideal for people who sit for extended periods, such as university staff.

## Project Overview
- **Purpose**: Detect poor posture among university staff in real-time and provide instant feedback to promote healthier sitting habits.
- **Technology**: Uses a webcam, the Mediapipe library for body landmark detection, and OpenCV for video processing.
- **Key Features**:
  - Real-time posture analysis and alerts
  - Visual feedback indicating good or poor posture
  - Tracking of neck and torso angles for detailed posture assessment

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/tanishpoddar/PosturePro
   cd PosturePro
   ```

2. **Install Required Packages**
   Ensure you have Python installed, then install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```
   - **Required Libraries**: `mediapipe`, `opencv-python`

3. **Run the Project**
   ```bash
   python posture_detection.py
   ```

## Usage
1. Connect a webcam.
2. Run the code to begin posture monitoring.
3. Adjust your posture as needed based on feedback from the system.

## How It Works
- **Body Tracking**: The Mediapipe library detects key body points like shoulders, neck, and hips.
- **Posture Analysis**: Calculates metrics such as shoulder width and neck and torso angles.
- **Feedback**: Alerts are displayed for poor posture, with colours indicating alignment status (e.g., green for good posture, red for poor posture).

## Future Enhancements
Plans include integrating IoT features such as LED indicators, which will provide an additional visual alert when poor posture is detected.

## License
**All Rights Reserved.** Unauthorized use, reproduction, or distribution of this code is prohibited.

## Disclaimer
This project is provided for educational purposes. For any additional use or modifications, please contact the author.

---
