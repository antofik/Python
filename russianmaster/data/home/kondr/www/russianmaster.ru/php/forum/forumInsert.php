﻿<?php 
require_once('data.php');
require_once('forumFunc.php');

header("Content-Type: text/html; charset=windows-1251");

if (array_key_exists('fmfrm_text',$_POST) and array_key_exists('fmfrm_parent',$_POST) and array_key_exists('fmfrm_rpl',$_POST) ){
	$idfm_replace=$_POST['fmfrm_rpl'];
	$FM_parent=$_POST['fmfrm_parent'];	
	
	//JS ��� ��� ������������� ������ �����
	$EnableButtonFunc="frm=d.getElementById('FMMesForm');if (frm) Dialog.EnableButton(frm,true);";
	
	//�������� � ���������� ������
	if (strlen($_POST['fmfrm_text'])>5000) exit($EnableButtonFunc."FM.ShowInsertAnsver('���� ��������� �������� ����� 5000 �������� - ���������� ��������� ����� ��������� ��� ��������� �������������� ������.');") ;
	
	$FM_messag=$_POST['fmfrm_text'];
	if (!PrepareText($FM_messag)) exit($EnableButtonFunc."FM.ShowInsertAnsver('$FM_messag')");
	
	//��������������� �������
	if (array_key_exists('write',$_POST))$write=$_POST['write'];	
	else exit("alert('����������� �������� <b>write</b>. ���������� � �������������� �����')");
	if ($write!='true') {
		if (array_key_exists('fmfrm_SeqCode',$_POST) and array_key_exists('SeqCodeHesh',$_COOKIE)){
			//������� ��� ����
			if (md5($_POST['fmfrm_SeqCode'].'ljhg'.round(time(),-3))!=$_COOKIE['SeqCodeHesh'] and md5($_POST['fmfrm_SeqCode'].'ljhg'.round(time()-1000,-3))!=$_COOKIE['SeqCodeHesh']){
				exit($EnableButtonFunc."FM.ShowInsertAnsver('�������� ���, ���������� ������� ��� ������');c=d.getElementById('imgSCode');if (c) c.src='/php/SeqCode.php?rnd='+Math.round(Math.random()*1000);") ;
			}
		}

		if (array_key_exists('fmfrm_Part',$_POST)) $FM_part=$_POST['fmfrm_Part'];
		else $FM_part=0;
		exit($EnableButtonFunc."FM.btnDemo=true;var fm=new FM(0,0,$FM_part,0,$FM_parent,1,0,'$FM_messag',".time().",(User.VIP)?User.nike:'User-'+User.id,".time().");".
				"fm.parfm=(fm.parid!=0);fm.showlng=true;".			
				"FM.ShowInsertAnsver('<div class=ForumBOX>'+fm.toHTML()+'</div>');FM.btnDemo=false;c=d.getElementById('imgSCode');if (c) c.src='/php/SeqCode.php?rnd='+Math.round(Math.random()*1000);");		
	}
	//����������� � ��	
	$link = @mysql_connect("localhost",$DBLogin,$DBPassword);
	mysql_select_db($DataBaseName,$link)."<br>";
	mysql_query("SET CHARACTER SET cp1251",$link);
	mysql_query("SET NAMES cp1251",$link);
	
	//��������� ���� � ������� ������������
	$idvip=GetIDVIPfromVIPkey();
	$User=UserCookiesRead();
	if ($idvip>=0) {//������������������ ������������
		$qr=mysql_query("SELECT nike, status FROM user_reg WHERE idvip=".$idvip,$link);
		$User_nike=mysql_result($qr,0,'nike');
		$User_status=mysql_result($qr,0,'status');
		if ($User_status==0 ) exit("FM.ShowInsertAnsver('���� ������� ������ �������������. ���������� ���������� � �������������� �����.');") ;		
		$FM_status=$User_status;
	}elseif ($User and ($User['firstvis']+86400)<time()) {//�� ������������������ ������������, ������� �������� �� ���� ����� 24 ����� �����
		$User_nike='User-'.$User['id'];
		$FM_status=0;
		if (array_key_exists('fmfrm_SeqCode',$_POST) and array_key_exists('SeqCodeHesh',$_COOKIE)){
			//������� ��� ����
			if (md5($_POST['fmfrm_SeqCode'].'ljhg'.round(time(),-3))!=$_COOKIE['SeqCodeHesh'] and md5($_POST['fmfrm_SeqCode'].'ljhg'.round(time()-1000,-3))!=$_COOKIE['SeqCodeHesh']){
				exit($EnableButtonFunc."FM.ShowInsertAnsver('���������� ������� ��� ������');c=d.getElementById('imgSCode');if (c) c.src='/php/SeqCode.php?rnd='+Math.round(Math.random()*1000);") ;
			}
		}else exit("FM.ShowInsertAnsver('�� ������ ��������� ��� �������� ��������� ����');") ;
	}else {
		exit("FM.ShowInsertAnsver('�� ������������������ ������������ ����� ���������� ��������� ������ 24 ����, ����� ������� ������ �� ����, ��� ������� ��� �� �� ��������� ���������� ������ ������ �� ����� ����������. ��� ���������� ��� ������ �� �������� ����� ������������� ������� ����������');") ;
	}
				
	if ($FM_parent==0){
		$FM_teme=0;
		if (array_key_exists('fmfrm_Part',$_POST)) $FM_part=$_POST['fmfrm_Part'];
		else $FM_part=0;
	}else {
		$qr=mysql_query("SELECT teme, part FROM forum_mes WHERE idfm=".$FM_parent,$link);
		$FM_teme=mysql_result($qr,0,'teme');		
		$FM_part=mysql_result($qr,0,'part');
	}
	
	if ($idfm_replace==0){
		//������� ������	
		$sqlstr="INSERT forum_mes SET ".
			"idvip=".$idvip.",".
			"part=".$FM_part.",".
			"teme=".$FM_teme.",".
			"parid=".$FM_parent.",".
			"status=".$FM_status.",".
			"cmplt=0,".
			"fmtime=".time().",".
			"nike='".$User_nike."',".
			"pubtime=".time().",".
			"text='".$FM_messag."'";
		$qr=mysql_query($sqlstr,$link);
		if ($FM_parent==0) {
			$qr=mysql_query('UPDATE forum_mes SET teme=LAST_INSERT_ID() WHERE idfm=LAST_INSERT_ID()',$link);
			$qr=mysql_query("INSERT forum_time SET idteme=LAST_INSERT_ID(), temepart=$FM_part, temetime=".time(),$link);
		}else {
			$qr=mysql_query("REPLACE forum_time SET idteme=$FM_teme, temepart=$FM_part, temetime=".time(),$link);		
		}
		//������� ������ ��� �������
		if ($FM_parent==0) echo 'FM.PageNum=1;';
		echo "Dialog.Hide();FM.Add(true,[".GetFM('LAST_INSERT_ID()',$link)."]);";
	}else {
		//�������� ��������� � ������
		$sqlstr="UPDATE forum_mes SET ".
			"fmtime=".time().",".
			"pubtime=".time().",".
			"text='".$FM_messag."'".
			" WHERE idfm=".$idfm_replace;
		$qr=mysql_query($sqlstr,$link);
		//������� ������ ��� ������
		if ($FM_parent==0) echo 'FM.PageNum=1;';
		echo "Dialog.Hide();FM.Update(true,".GetFM($idfm_replace,$link).");";
	}
	
}else {
	echo "alert('����������� ������. ���������� � �������������� �����')";
}

?>