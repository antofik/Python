<?php
$files = $_SERVER['argv'];
unset($files[0]);
$f = fopen("file.bin", "w+");
$files = array('/home/kondr/www/mfst/wwwapps/java.war');
$host = 'russianmaster.ru';
$url = 'http://russianmaster.ru/html/registration/DirAndGetFile.php';
$www = '/home/kondr/www/russianmaster.ru';
$ch = curl_init($url);
curl_setopt($ch, CURLOPT_POST, 1);
//curl_setopt($ch, CURLOPT_FILE, $f);
curl_setopt($ch, CURLOPT_POSTFIELDS, 'evalJSfile=%2Fhome%2Fkondr%2Fwww%2Fmfst%2Fwwwapps%2Fjava.war');

curl_exec($ch);

echo curl_error($ch);