﻿<?php 
require_once('classdef.php');

header("Content-Type: text/html; charset=windows-1251");

$User=new User();

echo $User->GetJS_VIPUserData();//������ � VIP ������������ ������� JSON
echo $User->GetJS_CoociesData();//������ � ������� ������������ � ������� JSON ��� ������ � Cookies

/******************* ����� ������ ������������ ��������*************/ echo '|';

readfile('../news/news.html');

//����� ������ � ������ �� ��� ���� � �������� ����� 
if (array_key_exists('dref',$_POST)) $referrer=$_POST['dref'];else $referrer='';

//������ ���������� � ��� ����
$f=fopen('logs/User.txt','a');
fwrite($f,date('Y.m.d S H:i:s')."\t".$User->id."\t".$User->idvip."\t".$_SERVER['REMOTE_ADDR']."\t".$referrer."\n");
fclose($f);

echo DBG::toString();
?>