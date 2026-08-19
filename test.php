<?php

$ch = curl_init("https://api.telegram.org");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_TIMEOUT, 15);
curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 10);

$response = curl_exec($ch);

echo "HTTP: " . curl_getinfo($ch, CURLINFO_HTTP_CODE) . "<br>";
echo "ERROR: " . curl_errno($ch) . "<br>";
echo "ERROR MSG: " . htmlspecialchars(curl_error($ch)) . "<br>";
echo "RESPONSE: " . htmlspecialchars($response ?? 'NULL');

curl_close($ch);
?>
