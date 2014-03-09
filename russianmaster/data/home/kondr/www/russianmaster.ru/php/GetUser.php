<?php 
require_once('classdef.php');

header("Content-Type: text/html; charset=windows-1251");

$User=new User();

echo $User->GetJS_VIPUserData();//Данные о VIP пользователе формате JSON
echo $User->GetJS_CoociesData();//Данные о обычном пользователе в формате JSON для записи в Cookies

/******************* Вывод текста персональных новостей*************/ echo '|';

readfile('../news/news.html');

//Прием данных о ссылке на наш сайт и ключевые слова 
if (array_key_exists('dref',$_POST)) $referrer=$_POST['dref'];else $referrer='';

//Запись статистики в лог файл
$f=fopen('logs/User.txt','a');
fwrite($f,date('Y.m.d S H:i:s')."\t".$User->id."\t".$User->idvip."\t".$_SERVER['REMOTE_ADDR']."\t".$referrer."\n");
fclose($f);

echo DBG::toString();
?>