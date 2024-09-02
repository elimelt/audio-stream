const channelId = window.location.pathname.split('/')[2];
let produceSocket, consumeSocket;
let audioContext, mediaStream;

document.getElementById('startProduceBtn').onclick = startProduce;
document.getElementById('stopProduceBtn').onclick = stopProduce;
document.getElementById('startConsumeBtn').onclick = startConsume;
document.getElementById('stopConsumeBtn').onclick = stopConsume;

async function startProduce() {
    try {
        produceSocket = new WebSocket(`wss://${location.host}/channel/${channelId}/produce`);
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const source = audioContext.createMediaStreamSource(mediaStream);
        const processor = audioContext.createScriptProcessor(4096, 1, 1);
        source.connect(processor);
        processor.connect(audioContext.destination);
        processor.onaudioprocess = (e) => {
            if (produceSocket.readyState === WebSocket.OPEN) {
                const inputData = e.inputBuffer.getChannelData(0);
                produceSocket.send(inputData.buffer);
            }
        };
        document.getElementById('startProduceBtn').disabled = true;
        document.getElementById('stopProduceBtn').disabled = false;
    } catch (error) {
        console.error('Error starting production:', error);
    }
}

function stopProduce() {
    if (mediaStream) {
        mediaStream.getTracks().forEach(track => track.stop());
    }
    if (audioContext) {
        audioContext.close();
    }
    if (produceSocket) {
        produceSocket.close();
    }
    document.getElementById('startProduceBtn').disabled = false;
    document.getElementById('stopProduceBtn').disabled = true;
}

async function startConsume() {
    try {
        consumeSocket = new WebSocket(`wss://${location.host}/channel/${channelId}/consume`);
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        consumeSocket.binaryType = 'arraybuffer';
        consumeSocket.onmessage = (event) => {
            const audioData = new Float32Array(event.data);
            const buffer = audioContext.createBuffer(1, audioData.length, audioContext.sampleRate);
            buffer.getChannelData(0).set(audioData);
            const source = audioContext.createBufferSource();
            source.buffer = buffer;
            source.connect(audioContext.destination);
            source.start();
        };
        document.getElementById('startConsumeBtn').disabled = true;
        document.getElementById('stopConsumeBtn').disabled = false;
    } catch (error) {
        console.error('Error starting consumption:', error);
    }
}

function stopConsume() {
    if (audioContext) {
        audioContext.close();
    }
    if (consumeSocket) {
        consumeSocket.close();
    }
    document.getElementById('startConsumeBtn').disabled = false;
    document.getElementById('stopConsumeBtn').disabled = true;
}