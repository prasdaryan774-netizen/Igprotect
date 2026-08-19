<?php

$token = "8802775389:AAGn7eRc1-v9v0bwxbcYb4Wtxu23jF39zik";
$chat_id = "8730143288";

$url = "https://api.telegram.org/bot" . $token . "/sendMessage";

$data = [
    "chat_id" => $chat_id,
    "text" => "Test message from Render"
];

$ch = curl_init($url);

curl_setopt_array($ch, [
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => http_build_query($data),
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT => 20,
    CURLOPT_CONNECTTIMEOUT => 10,
]);

$response = curl_exec($ch);

echo "HTTP: " . curl_getinfo($ch, CURLINFO_HTTP_CODE) . "<br>";
echo "ERROR: " . curl_errno($ch) . "<br>";
echo "ERROR MSG: " . htmlspecialchars(curl_error($ch)) . "<br>";
echo "<pre>" . htmlspecialchars($response ?? 'NULL') . "</pre>";

curl_close($ch);
?>
