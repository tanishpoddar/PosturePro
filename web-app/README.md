# PosturePro Web Application

This directory contains the web version of PosturePro, built with HTML, CSS, and JavaScript using MediaPipe for pose detection.

## Prerequisites
- Modern web browser (Chrome recommended)
- Webcam
- Internet connection (for MediaPipe libraries)

## Setup Instructions

1. **Navigate to the web app directory**
```bash
cd web-app
```

2. **Running Locally**

```bash
# Install live-server if you haven't
npm install -g live-server

# Run the server
live-server
```

3. **Access the Application**
- Open your web browser
- Navigate to `http://localhost:8000`
- Allow camera access when prompted

## File Structure
```
web-app/
├── index.html
├── style.css
└── script.js
```

## Troubleshooting

1. **Camera Access Issues**
- Ensure you've granted camera permissions in your browser
- Check if other applications are using the camera
- Try refreshing the page

2. **Performance Issues**
- Close other resource-intensive browser tabs
- Ensure you have a stable internet connection
- Update your browser to the latest version

For more details about the project, visit the [main README](../README.md).
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