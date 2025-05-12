


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



const jobId = "{{ request.args.get('job_id') }}";
const chatBox = document.getElementById("chat-box");
const inputField = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const startBtn = document.getElementById("startInterview");

// Disable input initially
inputField.disabled = true;
sendBtn.disabled = true;

function appendMessage(sender, message) {
    const msgDiv = document.createElement("div");
    msgDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
let currentUtterance = null;

function speak(text) {
    return new Promise(resolve => {
        if ('speechSynthesis' in window) {
            // Cancel current speech if any
            if (currentUtterance) {
                window.speechSynthesis.cancel();
            }
            
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 1.0;
            utterance.pitch = 1.0;
            utterance.volume = 1.0;
            
            utterance.onend = resolve;
            currentUtterance = utterance;
            window.speechSynthesis.speak(utterance);
        }
    });
}

function stopSpeaking() {
    if (window.speechSynthesis.speaking && currentUtterance) {
        window.speechSynthesis.cancel();
    }
}

// function sendToBot(userInput = "") {
//     fetch("/dashinter", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ user_input: userInput, job_id: jobId })
//     })
//     .then(res => res.json())
//     .then(data => {
//         if (data.error) {
//             appendMessage("Error", data.error);
//             return;
//         }
//         if (userInput) appendMessage("You", userInput);
//         appendMessage("HR", data.bot_reply);
        

//         if (data.finished) {
//             inputField.disabled = true;
//             sendBtn.disabled = true;
//             appendMessage("System", "✅ Interview finished. Thank you!");
//         }
//     })
//     .catch(err => {
//         appendMessage("Error", "Something went wrong.");
//         console.error(err);
//     });
// }

function sendToBot(userInput = "") {
    fetch("/dashinter", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_input: userInput, job_id: jobId })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            appendMessage("Error", data.error);
            return;
        }
        
        if (userInput) appendMessage("You", userInput);
        appendMessage("HR", data.bot_reply);

        // Speak the bot reply immediately
        if (data.bot_reply) {
            speak(data.bot_reply).catch(err => {
                console.error('Speech error:', err);
            });
        }

        if (data.finished) {
            inputField.disabled = true;
            sendBtn.disabled = true;
            appendMessage("System", "✅ Interview finished. Thank you!");
        }
    })
    .catch(err => {
        appendMessage("Error", "Something went wrong.");
        console.error(err);
    });
}

// Start Interview
startBtn.addEventListener("click", () => {
    inputField.disabled = false;
    sendBtn.disabled = false;
    startBtn.disabled = true;
    sendToBot(); // Kick off with the first bot question
});

// Send user answer
sendBtn.addEventListener("click", () => {
    const userInput = inputField.value.trim();
    if (!userInput) return;
    inputField.value = "";
    sendToBot(userInput);
});

// Optional: Press Enter to send
inputField.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        sendBtn.click();
    }
});



        