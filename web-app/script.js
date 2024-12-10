class PostureDetector {
    constructor() {
        this.video = document.getElementById('video');
        this.canvas = document.getElementById('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.startBtn = document.getElementById('startBtn');
        this.stopBtn = document.getElementById('stopBtn');
        this.warning = document.getElementById('warning');
        this.goodFrames = 0;
        this.badFrames = 0;
        this.lastFrameTime = Date.now();
        
        this.setupEventListeners();
    }

    setupEventListeners() {
        this.startBtn.addEventListener('click', () => this.startCamera());
        this.stopBtn.addEventListener('click', () => this.stopCamera());
    }

    async startCamera() {
        try {
            document.getElementById('loadingMessage').style.display = 'none';
            const stream = await navigator.mediaDevices.getUserMedia({ 
                video: { 
                    width: 640,
                    height: 480,
                    facingMode: 'user'
                } 
            });
            this.video.srcObject = stream;
            await this.video.play();
            
            this.startBtn.disabled = true;
            this.stopBtn.disabled = false;

            this.canvas.width = this.video.videoWidth;
            this.canvas.height = this.video.videoHeight;

            this.startDetection();
        } catch (err) {
            console.error('Error accessing camera:', err);
            alert('Error accessing camera. Please make sure you have a camera connected and have granted permission.');
        }
    }

    stopCamera() {
        if (this.video.srcObject) {
            const stream = this.video.srcObject;
            const tracks = stream.getTracks();
            tracks.forEach(track => track.stop());
            this.video.srcObject = null;
        }
        
        this.startBtn.disabled = false;
        this.stopBtn.disabled = true;
        
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }

    findDistance(x1, y1, x2, y2) {
        return Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
    }

    findAngle(x1, y1, x2, y2) {
        const theta = Math.acos((y2 - y1) * (-y1) / 
            (Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * y1));
        return parseInt(180 / Math.PI * theta);
    }

    updateStats(neckAngle, torsoAngle, shoulderOffset) {
        document.getElementById('neckAngle').textContent = `${Math.round(neckAngle)}°`;
        document.getElementById('torsoAngle').textContent = `${Math.round(torsoAngle)}°`;
        document.getElementById('shoulderOffset').textContent = `${Math.round(shoulderOffset)}px`;
        
        const currentTime = Date.now();
        const deltaTime = (currentTime - this.lastFrameTime) / 1000;
        this.lastFrameTime = currentTime;

        if (neckAngle < 40 && torsoAngle < 10) {
            this.goodFrames++;
            this.badFrames = 0;
            document.getElementById('postureTimer').textContent = 
                `${(this.goodFrames * deltaTime).toFixed(1)}s (Good)`;
            document.getElementById('postureTimer').className = 'good';
        } else {
            this.badFrames++;
            this.goodFrames = 0;
            document.getElementById('postureTimer').textContent = 
                `${(this.badFrames * deltaTime).toFixed(1)}s (Bad)`;
            document.getElementById('postureTimer').className = 'bad';
        }

        if (this.badFrames * deltaTime > 180) {
            this.warning.style.display = 'block';
            setTimeout(() => {
                this.warning.style.display = 'none';
            }, 3000);
        }
    }

    async startDetection() {
        const pose = new Pose({
            locateFile: (file) => {
                return `https://cdn.jsdelivr.net/npm/@mediapipe/pose@0.5.1675469404/${file}`;
            }
        });

        pose.setOptions({
            modelComplexity: 1,
            smoothLandmarks: true,
            enableSegmentation: false,
            smoothSegmentation: true,
            minDetectionConfidence: 0.5,
            minTrackingConfidence: 0.5
        });

        pose.onResults((results) => {
            this.drawResults(results);
        });

        const camera = new Camera(this.video, {
            onFrame: async () => {
                await pose.send({image: this.video});
            },
            width: 640,
            height: 480
        });

        camera.start();
    }

    drawResults(results) {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        if (!results.poseLandmarks) return;

        const landmarks = results.poseLandmarks;
        const leftShoulder = landmarks[11];
        const rightShoulder = landmarks[12];
        const leftEar = landmarks[7];
        const leftHip = landmarks[23];
        const width = this.canvas.width;
        const height = this.canvas.height;
        const points = {
            leftShoulder: {
                x: leftShoulder.x * width,
                y: leftShoulder.y * height
            },
            rightShoulder: {
                x: rightShoulder.x * width,
                y: rightShoulder.y * height
            },
            leftEar: {
                x: leftEar.x * width,
                y: leftEar.y * height
            },
            leftHip: {
                x: leftHip.x * width,
                y: leftHip.y * height
            }
        };

        const shoulderOffset = this.findDistance(
            points.leftShoulder.x, points.leftShoulder.y,
            points.rightShoulder.x, points.rightShoulder.y
        );

        const neckInclination = this.findAngle(
            points.leftShoulder.x, points.leftShoulder.y,
            points.leftEar.x, points.leftEar.y
        );

        const torsoInclination = this.findAngle(
            points.leftHip.x, points.leftHip.y,
            points.leftShoulder.x, points.leftShoulder.y
        );

        this.updateStats(neckInclination, torsoInclination, shoulderOffset);

        this.drawLandmark(points.leftShoulder, '#FFD700');
        this.drawLandmark(points.rightShoulder, '#FF69B4');
        this.drawLandmark(points.leftEar, '#FFD700');
        this.drawLandmark(points.leftHip, '#FFD700');

        const color = (neckInclination < 40 && torsoInclination < 10) ? '#90EE90' : '#FF0000';
        
        this.drawConnection(points.leftShoulder, points.leftEar, color);
        this.drawConnection(points.leftHip, points.leftShoulder, color);
    }

    drawLandmark(point, color) {
        this.ctx.beginPath();
        this.ctx.arc(point.x, point.y, 5, 0, 2 * Math.PI);
        this.ctx.fillStyle = color;
        this.ctx.fill();
    }

    drawConnection(start, end, color) {
        this.ctx.beginPath();
        this.ctx.moveTo(start.x, start.y);
        this.ctx.lineTo(end.x, end.y);
        this.ctx.strokeStyle = color;
        this.ctx.lineWidth = 2;
        this.ctx.stroke();
    }
}

window.addEventListener('load', () => {
    if (window.Pose && window.Camera) {
        new PostureDetector();
    } else {
        console.error('MediaPipe libraries not loaded properly');
        alert('Error: Required libraries not loaded. Please check your internet connection and try again.');
    }
});