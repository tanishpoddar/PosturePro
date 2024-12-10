# PosturePro Python Application

This directory contains the desktop version of PosturePro built with Python, OpenCV, and MediaPipe.

## Prerequisites
- Python 3.8 or higher
- Webcam
- Operating System: Windows/Linux/macOS

## Installation

1. **Navigate to the Python app directory**
```bash
cd python-app
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv venv

# For Windows
venv\Scripts\activate

# For Unix or MacOS
source venv/bin/activate
```

3. **Install Required Packages**
```bash
pip install -r requirements.txt
```

## Running the Application

1. **Start the application**
```bash
python posture_detection.py
```

2. **Using the Application**
- Allow camera access when prompted
- Position yourself so that your upper body is visible in the frame
- The application will begin tracking your posture automatically
- Follow the on-screen instructions for optimal posture detection

## Troubleshooting

If you encounter any issues:

1. **Camera not detected**
- Ensure your webcam is properly connected
- Check if other applications are using the camera
- Try running the script with administrator privileges

2. **Dependencies Issues**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## Performance Notes
- Recommended to use in well-lit conditions
- Keep your face and upper body clearly visible
- Maintain a reasonable distance from the camera (approximately arm's length)

For more details about the project, visit the [main README](../README.md).