// ================================
// CONFIG
// ================================
const API_URL = "http://127.0.0.1:8000/identify";

// ================================
// GLOBALS
// ================================
let mediaRecorder;
let audioChunks = [];

// ================================
// UI ELEMENTS
// ================================
const recordBtn = document.getElementById("recordBtn");
const stopBtn = document.getElementById("stopBtn");
const statusText = document.getElementById("status");
const resultDiv = document.getElementById("result");

// ================================
// START RECORDING
// ================================
recordBtn.onclick = async () => {
  try {
    audioChunks = [];

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();

    statusText.innerText = "🎙️ Recording... (play a song)";
    recordBtn.disabled = true;
    stopBtn.disabled = false;

    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data);
    };

  } catch (err) {
    console.error(err);
    statusText.innerText = "❌ Microphone access denied";
  }
};

// ================================
// STOP RECORDING
// ================================
stopBtn.onclick = async () => {
  mediaRecorder.stop();

  recordBtn.disabled = false;
  stopBtn.disabled = true;
  statusText.innerText = "⏳ Processing audio...";

  mediaRecorder.onstop = async () => {
    try {
      const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
      const wavBlob = await convertToWav(audioBlob);
      await sendToBackend(wavBlob);
    } catch (err) {
      console.error(err);
      statusText.innerText = "❌ Error processing audio";
    }
  };
};

// ================================
// SEND AUDIO TO BACKEND
// ================================
async function sendToBackend(wavBlob) {
  const formData = new FormData();
  formData.append("file", wavBlob, "recording.wav");

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      throw new Error(await response.text());
    }

    const data = await response.json();

    if (!data.song) {
      resultDiv.innerHTML = "<h3>❌ No match found</h3>";
    } else {
      resultDiv.innerHTML = `
        <h3>🎵 Match Found</h3>
        <p><b>Song:</b> ${data.song}</p>
        <p><b>Score:</b> ${data.score}</p>
      `;
    }

    statusText.innerText = "✅ Done";
  } catch (err) {
    console.error(err);
    statusText.innerText = "❌ Error identifying song";
  }
}

// ================================
// CONVERT AUDIO TO WAV
// ================================
async function convertToWav(blob) {
  const arrayBuffer = await blob.arrayBuffer();
  const audioContext = new AudioContext();
  const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);

  const samples = audioBuffer.getChannelData(0);
  return encodeWAV(samples, audioBuffer.sampleRate);
}

// ================================
// WAV ENCODER
// ================================
function encodeWAV(samples, sampleRate) {
  const buffer = new ArrayBuffer(44 + samples.length * 2);
  const view = new DataView(buffer);

  function writeString(offset, str) {
    for (let i = 0; i < str.length; i++) {
      view.setUint8(offset + i, str.charCodeAt(i));
    }
  }

  writeString(0, "RIFF");
  view.setUint32(4, 36 + samples.length * 2, true);
  writeString(8, "WAVE");
  writeString(12, "fmt ");
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, 1, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * 2, true);
  view.setUint16(32, 2, true);
  view.setUint16(34, 16, true);
  writeString(36, "data");
  view.setUint32(40, samples.length * 2, true);

  let offset = 44;
  for (let i = 0; i < samples.length; i++, offset += 2) {
    let s = Math.max(-1, Math.min(1, samples[i]));
    view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7fff, true);
  }

  return new Blob([view], { type: "audio/wav" });
}


// async function identify() {
//   const fileInput = document.getElementById("audioFile");
//   const status = document.getElementById("status");
//   const result = document.getElementById("result");

//   if (!fileInput.files.length) {
//     alert("Please select an audio file");
//     return;
//   }

//   status.innerText = "Uploading & identifying...";
//   result.innerHTML = "";

//   const formData = new FormData();
//   formData.append("file", fileInput.files[0]);

//   try {
//     const response = await fetch("http://127.0.0.1:8000/identify", {
//       method: "POST",
//       body: formData
//     });

//     if (!response.ok) {
//       const text = await response.text();
//       throw new Error(text);
//     }

//     const data = await response.json();

//     if (!data.song) {
//       result.innerHTML = "<h3>❌ No match found</h3>";
//     } else {
//       result.innerHTML = `
//         <h3>🎵 Match Found</h3>
//         <p><b>Song:</b> ${data.song}</p>
//         <p><b>Score:</b> ${data.score}</p>
//       `;
//     }

//     status.innerText = "Done!";
//   } catch (err) {
//     status.innerText = "Error identifying song";
//     console.error("FRONTEND ERROR:", err);
//   }
// }
