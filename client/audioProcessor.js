let audioContext;
let mediaStream;
let websocket;
let isCapturing = false;
const bufferSize = 4096;

document.getElementById('connectBtn').addEventListener('click', toggleCapture);

async function toggleCapture() {
    if (isCapturing) {
        stopCapture();
    } else {
        await startCapture();
    }
}

async function startCapture() {
    const url = document.getElementById('urlInput').value;
    
    try {
        // Initialize WebSocket connection
        websocket = new WebSocket(url);
        websocket.binaryType = 'arraybuffer';
        
        websocket.onopen = () => {
            console.log('WebSocket connection established');
        };
        
        websocket.onerror = (error) => {
            console.error('WebSocket error:', error);
            stopCapture();
        };
        
        // Initialize audio context and stream
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        const source = audioContext.createMediaStreamSource(mediaStream);
        const processor = audioContext.createScriptProcessor(bufferSize, 1, 1);
        
        source.connect(processor);
        processor.connect(audioContext.destination);
        
        processor.onaudioprocess = (e) => {
            if (websocket.readyState === WebSocket.OPEN) {
                const inputData = e.inputBuffer.getChannelData(0);
                const dataToSend = convertFloat32ToInt16(inputData);
                websocket.send(dataToSend);
            }
        };
        
        isCapturing = true;
        updateCaptureStatus();
        console.log('Audio capture started');
    } catch (error) {
        console.error('Error starting audio capture:', error);
    }
}

function stopCapture() {
    if (mediaStream) {
        mediaStream.getTracks().forEach(track => track.stop());
    }
    
    if (audioContext) {
        audioContext.close();
    }
    
    if (websocket) {
        websocket.close();
    }
    
    isCapturing = false;
    updateCaptureStatus();
    console.log('Audio capture stopped');
}

function updateCaptureStatus() {
    const statusElement = document.getElementById('captureStatus');
    statusElement.textContent = isCapturing ? 'capturing' : 'enable capture';
}

function convertFloat32ToInt16(float32Array) {
    const int16Array = new Int16Array(float32Array.length);
    for (let i = 0; i < float32Array.length; i++) {
        const s = Math.max(-1, Math.min(1, float32Array[i]));
        int16Array[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
    }
    return int16Array.buffer;
}