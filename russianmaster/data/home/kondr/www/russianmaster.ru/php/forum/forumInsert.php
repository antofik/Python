<?php 
require_once('data.php');
require_once('forumFunc.php');

header("Content-Type: text/html; charset=windows-1251");

if (array_key_exists('fmfrm_text',$_POST) and array_key_exists('fmfrm_parent',$_POST) and array_key_exists('fmfrm_rpl',$_POST) ){
	$idfm_replace=$_POST['fmfrm_rpl'];
	$FM_parent=$_POST['fmfrm_parent'];	
	
	//JS код для разблокировки кнопок формы
	$EnableButtonFunc="frm=d.getElementById('FMMesForm');if (frm) Dialog.EnableButton(frm,true);";
	
	//Проверка и подготовка данных
	if (strlen($_POST['fmfrm_text'])>5000) exit($EnableButtonFunc."FM.ShowInsertAnsver('Ваше сообщение содержит более 5000 символов - пожалуйста сократите текст сообщения или упростите форматирование текста.');") ;
	
	$FM_messag=$_POST['fmfrm_text'];
	if (!PrepareText($FM_messag)) exit($EnableButtonFunc."FM.ShowInsertAnsver('$FM_messag')");
	
	//Предварительный посмотр
	if (array_key_exists('write',$_POST))$write=$_POST['write'];	
	else exit("alert('Отсутствует параметр <b>write</b>. Обратитесь к администратору сайта')");
	if ($write!='true') {
		if (array_key_exists('fmfrm_SeqCode',$_POST) and array_key_exists('SeqCodeHesh',$_COOKIE)){
			//Проврка хеш кода
			if (md5($_POST['fmfrm_SeqCode'].'ljhg'.round(time(),-3))!=$_COOKIE['SeqCodeHesh'] and md5($_POST['fmfrm_SeqCode'].'ljhg'.round(time()-1000,-3))!=$_COOKIE['SeqCodeHesh']){
				exit($EnableButtonFunc."FM.ShowInsertAnsver('Неверный код, пожалуйста введите код заново');c=d.getElementById('imgSCode');if (c) c.src='/php/SeqCode.php?rnd='+Math.round(Math.random()*1000);") ;
			}
		}

		if (array_key_exists('fmfrm_Part',$_POST)) $FM_part=$_POST['fmfrm_Part'];
		else $FM_part=0;
		exit($EnableButtonFunc."FM.btnDemo=true;var fm=new FM(0,0,$FM_part,0,$FM_parent,1,0,'$FM_messag',".time().",(User.VIP)?User.nike:'User-'+User.id,".time().");".
				"fm.parfm=(fm.parid!=0);fm.showlng=true;".			
				"FM.ShowInsertAnsver('<div class=ForumBOX>'+fm.toHTML()+'</div>');FM.btnDemo=false;c=d.getElementById('imgSCode');if (c) c.src='/php/SeqCode.php?rnd='+Math.round(Math.random()*1000);");		
	}
	//подключение к БД	
	$link = @mysql_connect("localhost",$DBLogin,$DBPassword);
	mysql_select_db($DataBaseName,$link)."<br>";
	mysql_query("SET CHARACTER SET cp1251",$link);
	mysql_query("SET NAMES cp1251",$link);
	
	//Получение ника и статуса пользователя
	$idvip=GetIDVIPfromVIPkey();
	$User=UserCookiesRead();
	if ($idvip>=0) {//Зарегистрированный пользователь
		$qr=mysql_query("SELECT nike, status FROM user_reg WHERE idvip=".$idvip,$link);
		$User_nike=mysql_result($qr,0,'nike');
		$User_status=mysql_result($qr,0,'status');
		if ($User_status==0 ) exit("FM.ShowInsertAnsver('Ваша учетная запись заблокирована. Пожалуйста обратитесь к администратору сайта.');") ;		
		$FM_status=$User_status;
	}elseif ($User and ($User['firstvis']+86400)<time()) {//Не зарегистрированный пользователь, который приходил на сайт более 24 часов назад
		$User_nike='User-'.$User['id'];
		$FM_status=0;
		if (array_key_exists('fmfrm_SeqCode',$_POST) and array_key_exists('SeqCodeHesh',$_COOKIE)){
			//Проврка хеш кода
			if (md5($_POST['fmfrm_SeqCode'].'ljhg'.round(time(),-3))!=$_COOKIE['SeqCodeHesh'] and md5($_POST['fmfrm_SeqCode'].'ljhg'.round(time()-1000,-3))!=$_COOKIE['SeqCodeHesh']){
				exit($EnableButtonFunc."FM.ShowInsertAnsver('Пожалуйста введите код заново');c=d.getElementById('imgSCode');if (c) c.src='/php/SeqCode.php?rnd='+Math.round(Math.random()*1000);") ;
			}
		}else exit("FM.ShowInsertAnsver('Не заданы параметры для проверки защитного кода');") ;
	}else {
		exit("FM.ShowInsertAnsver('Не зарегистрированные пользователи могут отправлять сообщения спустя 24 часа, после первого визита на сайт, при условии что Вы не запретили сохранение личных данных на своем компьютере. Это необходимо для защиты от создания одним пользователем иллюзии массовости');") ;
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
		//Вставка записи	
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
		//Возврат записи для вставки
		if ($FM_parent==0) echo 'FM.PageNum=1;';
		echo "Dialog.Hide();FM.Add(true,[".GetFM('LAST_INSERT_ID()',$link)."]);";
	}else {
		//Внесение изменений в запись
		$sqlstr="UPDATE forum_mes SET ".
			"fmtime=".time().",".
			"pubtime=".time().",".
			"text='".$FM_messag."'".
			" WHERE idfm=".$idfm_replace;
		$qr=mysql_query($sqlstr,$link);
		//Возврат записи для замены
		if ($FM_parent==0) echo 'FM.PageNum=1;';
		echo "Dialog.Hide();FM.Update(true,".GetFM($idfm_replace,$link).");";
	}
	
}else {
	echo "alert('Отсутствуют данные. Обратитесь к администратору сайта')";
}

?>