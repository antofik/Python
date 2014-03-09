﻿<?php 

header("Content-Type: text/html; charset=windows-1251");

if (array_key_exists('IDgr',$_GET))$IDgr=$_GET['IDgr'];else $IDgr=31;
if (array_key_exists('year',$_GET))$year=$_GET['year'];else $year=2009;

$fprefics="../cup/cup$year/".GetDataFileName($IDgr);

//��������
if (!file_exists($fprefics."_cont.txt")) exit("if (box=d.getElementById('CupResult')) box.innerHTML='<br><br><br><br><span style=\"color:red\"><b>��������, ��� ������� �� ������ ������ �� ����������� ������.<br>���������� ������ �������� ������� ������ ���� ��������.</b></span>'");
$f=fopen($fprefics."_cont.txt",'r');
echo "CCs=[\n";
while (!feof($f)){
	$d=str_replace("'",'&#039',explode("\t",fgets($f,4096)));
	if ($d[0]==$IDgr) echo "new CC($d[0],$d[1],$d[2],'$d[3]','$d[4]','$d[5]','$d[6]','$d[7]',$d[8],'$d[9]',$d[10],'$d[11]','$d[12]','".trim($d[13],"\n\r")."'),\n";
}
echo "null];CCs.pop();";
fclose($f);

//����������
if (!file_exists($fprefics."_SKR.txt")) exit("alert('���� ������ ID=$IDgr �� ������');");
$f=fopen($fprefics."_SKR.txt",'r');
echo "CPs=[null,[],[],null,null,null,null,null,[],[],[]];\n";
while (!feof($f)){
	$d=str_replace("'",'&#039',explode("\t",fgets($f,4096)));
	if ($d[0]==$IDgr) echo "CPs[$d[1]].push(new CP($d[0],$d[1],$d[2],'$d[3]','$d[4]','$d[5]','$d[6]','$d[7]','$d[8]','$d[9]',".
		"'$d[10]','$d[11]','$d[12]','$d[13]','$d[14]','$d[15]',$d[16],".
		"['$d[17]','$d[18]','$d[19]','$d[20]','$d[21]','$d[22]','$d[23]','$d[24]','$d[25]','$d[26]'],".
		"['$d[27]','$d[28]','$d[29]','$d[30]','$d[31]','$d[32]','$d[33]','$d[34]','$d[35]','$d[36]'],".
		"['$d[37]','$d[38]','$d[39]','$d[40]','$d[41]','$d[42]','$d[43]','$d[44]','$d[45]','$d[46]'],".
		"'".trim($d[47],"\n\r")."'));\n";
}
fclose($f);

//��������� ��������
if (!file_exists($fprefics."_wel.txt")) exit("alert('���� ������ ID=$IDgr �� ������');");
$f=fopen($fprefics."_wel.txt",'r');
while (!feof($f)){
	$var=trim(fgets($f,4096));
	if (strlen($var)>1) echo "CUP.$var;\n";
}
fclose($f);
echo "CUP.ShowResult();";


function GetDataFileName($IDgr){
	$dfn=array();
	$dfn[11]='AS16';//���������� ���� �����, 237-41-86, maloletnev@mtu-net.ru
	$dfn[31]='B16';//�������� ������ ���������, 218-30-5, danceboy@rambler.ru
	$dfn[32]='BA15';//���������� ���� �����, ���. 237-41-86, maloletnev@mtu-net.ru
	$dfn[41]='C16';//�������� ������, Interprize@yandex.ru
	$dfn[42]='C1415';//���������� ���� �����������, 527-16-27, sharovatova@bk.ru
	$dfn[43]='C13';//�������� ���� �������������, (495)3937029, (926)5468287, mb-mia@yandex.ru
	$dfn[51]='D16';//������� ������� ����������, 932-55-64, topdance@mtu-net.ru
	$dfn[52]='D1415';//������� ��������� ��������, 256-69-4, inna@ibcenter.ru
	$dfn[53]='D1213';//������� ������ �����������, 583-42-83, ganeeva@rambler.ru
	$dfn[54]='D11';//������������� �������
	$dfn[61]='E14';//���� �����, master@machaon-dance.ru
	$dfn[63]='E2115';//���� ������, annatitovav@mail.ru
	$dfn[64]='E1011';//�������� ���� �������������, (495)3937029, (926)5468287, mb-mia@yandex.ru
	$dfn[65]='E9';//������� �������� �������, 614-01-88, supertim2004@mail.ru
	$dfn[72]='N1011_N14';//������ �����, kravez_alena@mail.ru
	$dfn[73]='N9_N1215';//������ �������
	$dfn[74]='N1011_N14';//������ �����, kravez_alena@mail.ru
	$dfn[75]='N9_N1215';//������ �������'
	
	$dfn[101]='mash';//Mashkov'
	$dfn[102]='mash';//Mashkov'
	$dfn[103]='mash';//Mashkov'
	$dfn[104]='mash';//Mashkov'
	$dfn[105]='mash';//Mashkov'
	$dfn[106]='mash';//Mashkov'
	$dfn[107]='mash';//Mashkov'
	return $dfn[$IDgr];
}

?>