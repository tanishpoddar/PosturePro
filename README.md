# PosturePro: Real-Time Posture Detection System

PosturePro is a real-time posture detection tool designed to help users maintain healthy posture by identifying and alerting them to poor posture. Our system offers both a Python GUI application and a web-based solution to cater to different user preferences.

## Project Overview

- **Purpose**: Detect poor posture among university staff in real-time and provide instant feedback to promote healthier sitting habits.
- **Technology**: Uses computer vision and machine learning for accurate posture detection
- **Key Features**:
  - Real-time posture analysis and alerts
  - Visual feedback indicating good or poor posture
  - Tracking of neck and torso angles for detailed posture assessment
  - Available in both desktop and web formats

## Applications

The project contains two main applications:

1. **Python GUI Application** (`/python-app`)
   - Desktop-based solution using OpenCV and MediaPipe
   - Direct webcam integration
   - Low-latency processing
   - [Setup Instructions](./python-app/README.md)

2. **Web Application** (`/web-app`)
   - Browser-based solution using MediaPipe
   - No installation required
   - Cross-platform compatibility
   - [Setup Instructions](./docs/README.md)

## How It Works

- **Body Tracking**: Utilizes advanced computer vision to detect key body points like shoulders, neck, and hips
- **Posture Analysis**: Calculates metrics such as shoulder width and neck and torso angles
- **Feedback**: Real-time alerts are displayed for poor posture, with colors indicating alignment status

## License

**All Rights Reserved.** Unauthorized use, reproduction, or distribution of this code is prohibited.

## Disclaimer

This project is provided for educational purposes. For any additional use or modifications, please contact the author.