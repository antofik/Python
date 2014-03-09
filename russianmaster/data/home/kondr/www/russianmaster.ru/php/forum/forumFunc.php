<?php 

//Проверка VIPkey и возврат idvip
function GetIDVIPfromVIPkey(){
	if (array_key_exists('VIPkey',$_COOKIE)){
		$VIPkey=$_COOKIE['VIPkey'];
		$key=substr($VIPkey,0,32);
		$pwh=substr($VIPkey,32,32);
		$idvip=(int)substr($VIPkey,64);
		if ($key==md5($pwh.$idvip.'kjh98gfhj')) return $idvip;
		else return -1;
	}else return -1;
}
//Подготовка текста
function PrepareText(&$text){
	//Недопустимые слова
	$serch='/(хуй|буха|муда|пизд|хуя|хуё|хуе|ебат|гавн|ебл|ебал|хрен|нафиг|фиго|тошни|блева|придур|дерьм|идиот|быдло|отстой|кретин|критин|дура|придур|хамл)/i';
	$replace='<font color=red><b>$1</b></font>';
	$str=preg_replace($serch,$replace,htmlspecialchars(trim($text), ENT_QUOTES),-1,$count);
	if ($count>0) {
		$text= str_replace("\\",'',str_replace("\n",'<br>',str_replace("\r\n",'<br>',$str)));
		$text='<b style="color:darkred">Извините, в Вашем сообщении найдены недопустимые сочетания символов:</b><br>'.$text;
		return false;
	}else {
		$serch= array();$replace=array();
		$serch[]='_\r\n_';			$replace[]="\n";
		$serch[]='_\n+_';		$replace[]="\n";
		
		$serch[]='_^%(.{3,200})$_m';$replace[]='<h4>\1</h4>';
		$serch[]='_^[-—•](.+)$_m';	$replace[]='<li>\1</li>';
		$serch[]='_^&gt;(.+)$_m';	$replace[]='<p class=cit>\1</p>';
		$serch[]='_^([^<].+)$_m';	$replace[]='<p>\1</p>';
		$serch[]='_!([A-zА-я]+)_';$replace[]='<b>\1</b>';
		$serch[]='_>\n<_';			$replace[]='><';
		$serch[]='_\n_';			$replace[]='<br>';
		$serch[]='_(<li>.+</li>)_';	$replace[]='<ul>\1</ul>';	
		$serch[]='_ [-–] _';			$replace[]=' — ';
		$serch[]='_ *,_';			$replace[]=', ';
		$serch[]='_ +_';			$replace[]=' ';
		$serch[]='_(http://[^ \n<]+)_';$replace[]='<u>\1</u>';
		
	
		$text=preg_replace($serch,$replace,$str);
	}
	
	return true;
}

function GetFM($id,$link){
	$qr=mysql_query("SELECT idfm,idvip,part,teme,parid,status,cmplt,text,fmtime,nike,pubtime, voit1, voit0 FROM forum_mes WHERE idfm=".$id,$link);

	if ($row=mysql_fetch_row($qr)){
		return "new FM(".$row[0].",".$row[1].",".$row[2].",".$row[3].",".$row[4].",".$row[5].",".$row[6].",'".$row[7]."',".$row[8].",'".$row[9]."',".$row[10].",".$row[11].",".$row[12].")";						
	}else return 'null';
}

function UserCookiesRead(){
	if (array_key_exists('UserCook',$_COOKIE) and array_key_exists('UserHash',$_COOKIE)) {
		$User=array();
	}else return null;
	
	$data=$_COOKIE['UserCook'];
	$hash=$_COOKIE['UserHash'];
	$tmp=explode('@',$data);
	$us=array();
	foreach ($tmp as $key => $value){
		$param=explode('_',$value);
		$User[$param[0]]=(int)$param[1];
	}
	if (GetHash($User)==$hash) return $User;
	else return null;
}
function GetHash($User){
	return md5($User['id'].'|'.$User['firstvis'].'|'.$User['lastvis'].'|'.$User['previs'].'|'.$User['visits'].'|'.$User['forum'].'|'.'KneD5W');	
}

?>