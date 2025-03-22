let videoElement = document.getElementById("video");
let startInterviewButton = document.getElementById("startInterview");
let muteButton = document.getElementById("muteButton");
let videoButton = document.getElementById("videoButton");
let endCallButton = document.getElementById("endCallButton");
let fullscreenButton = document.getElementById("fullscreenButton");

let stream;
let audioTrack;
let videoTrack;

// Function to start the camera and microphone
async function startCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        videoElement.srcObject = stream;

        // Get audio and video tracks
        audioTrack = stream.getAudioTracks()[0];
        videoTrack = stream.getVideoTracks()[0];
    } catch (err) {
        console.error("Error accessing camera/microphone: ", err);
        alert("Please allow camera and microphone access.");
    }
}

// Start Interview - Request access to camera & mic
startInterviewButton.addEventListener("click", () => {
    startCamera();
});

// Mute/Unmute audio
muteButton.addEventListener("click", () => {
    if (audioTrack) {
        audioTrack.enabled = !audioTrack.enabled;
        muteButton.textContent = audioTrack.enabled ? "🔊" : "🔇";
    }
});

// Toggle video on/off
videoButton.addEventListener("click", () => {
    if (videoTrack) {
        videoTrack.enabled = !videoTrack.enabled;
        videoButton.textContent = videoTrack.enabled ? "📷" : "🚫";
    }
});

// End call - Stop all tracks
endCallButton.addEventListener("click", () => {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        videoElement.srcObject = null;
    }
});

// Fullscreen Toggle
fullscreenButton.addEventListener("click", () => {
    if (!document.fullscreenElement) {
        videoElement.requestFullscreen().catch(err => {
            console.error("Error enabling fullscreen: ", err);
        });
    } else {
        document.exitFullscreen();
    }
});