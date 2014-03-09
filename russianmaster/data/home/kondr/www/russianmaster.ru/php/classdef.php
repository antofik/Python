﻿<?php 

User::$SQL_DB=new SQLDB('localhost','kondr_mfst','kondr_umfst','asdwtey29Gd');

MAIL::$SysAdmin='������������ ��������, ������������� �����.';
MAIL::$SysAdminMail='temp@rustea.com';

if ($_SERVER['SERVER_NAME']=='rm' or $_SERVER['SERVER_NAME']=='rm.ru') {
	MAIL::$WriteToFile=true;
	DBG::$Enable=true;
}

User::$VisInterval=10800;//�������� � ���, ����� �������� ������������� ����� �����. 3 ����=10800 ���

/**
 * ����������� � ���� ������
 *
 */
class SQLDB {
	public $SQL_DB_HOST;
	public $SQL_DB_NAME;
	public $SQL_USER;
	public $SQL_PW;
	
	/**
	 * ����������� � ���� ������
	 * @var resource
	 */
	private $dblink;
	private $dbres;
	
	/**
	 * �������� ������� ��� ����������� � ��
	 * @param string $host
	 * @param string $DBname
	 * @param string $user
	 * @param string $pw
	 * @return SQLDB
	 */
	public function SQLDB($host,$DBname,$user,$pw){
		$this->SQL_DB_HOST=$host;
		$this->SQL_DB_NAME=$DBname;
		$this->SQL_USER=$user;
		$this->SQL_PW=$pw;
	}
	/**
	 * ����������� � ����� ���� ������
	 * @return bool
	 */
	public function Connect(){
		if ($this->dblink = @mysql_connect($this->SQL_DB_HOST,$this->SQL_USER,$this->SQL_PW)){
			if (mysql_select_db($this->SQL_DB_NAME,$this->dblink)) {
				mysql_query("SET CHARACTER SET cp1251",$this->dblink);
				mysql_query("SET NAMES cp1251",$this->dblink);
				return true;
			}
			else return false;
		}else return false;
	}	
	/**
	 * ���������� �� ����
	 *
	 */
	public function Disconnect(){mysql_close($this->dblink);}
	/**
	 * ������ � ���� ������
	 * @param string $sql
	 * @return descriptor
	 */
	public function Query($sql){
		$this->dbres=@mysql_query($sql,$this->dblink);
		//DBG::AddInfo($sql);
		//DBG::AddInfo(mysql_error($this->dblink));
		return $this->dbres;
	}
	/**
	 * ���������� �������
	 * @return string
	 */
	public function __toString(){
		$s='';
		foreach ($this as $prop => $val) $s.=$prop.' = '.$val.'<br>';
		return ' <i>'.$s.'</i>';
	}
	
	public function ErrorInfo(){
		return mysql_error($this->dblink);
	}	
}

/**
 * ������ � ������������
 *
 */
class User{
	/**
	 * �������� � ���, ����� �������� ������������� ����� �����.
	 * @var int
	 */	
	public static $VisInterval;
	/**
	 * ������������� �������� ������������
	 * @var int
	 */
	public $id;
	/**
	 * ����� ������� ������ � ������� Unix
	 * @var int
	 */
	public $firstvis;	
	/**
	 * ����� ����������� ������ � ������� Unix
	 * @var int
	 */
	public $previs;
	/**
	 * ����� ����������� ������ �� ��������� 3 ���� � ������� Unix
	 * @var int
	 */
	public $lastvis;
	/**
	 * ���������� �������
	 * @var int
	 */
	public $visits;	
	/**
	 * ���������� ��� ������
	 * @var string
	 */	
	public $forum;		
	
	/**
	 * ������������� VIP ������������ (�������������������
	 * @var int
	 */
	public $idvip;
	/**
	 * email
	 * @var string
	 */
	public $email;
	/**
	 * ��� ������������
	 *
	 * @var string
	 */
	public $name;
	/**
	 * ������� ������������
	 * @var string
	 */
	public $sname;
	/**
	 * ��� ������������
	 * @var string
	 */
	public $nike;
	/**
	 * �����
	 * @var string
	 */
	public $city;
	
	/**
	 * md5 - ��� ������
	 * @var string
	 */
	public $pwh;
	/**
	 * md5 - ��� ������ ������
	 * @var string
	 */
	public $pwhnew;
	/**
	 * ���� ���������� � ������� ������
	 * @var int
	 */
	public $passwdate;
	/**
	 * ���� ������ 100 - ���������� ��������� ������� ����� ������
	 * ���� ������ 100 - ����� �� �������� ������������� ������
	 * @var int
	 */
	public $passwerr;
	/**
	 * ������ (����������) ������������
	 * @var int
	 */
	public $status;
	/**
	 * ���������� ����� �� ������������
	 * @var int
	 */
	public $complaint;
	
		
	/**
	 * ��������� ��� ������
	 * @var string
	 */
	public $forumset;
	/**
	 * ������ ���������������� ���������
	 * @var string
	 */
	public $userset;

	/**
	 * ������ �� ������ ���� ������
	 *
	 * @var SQLDB
	 */
	public static $SQL_DB;

	/**
	 * ����������, ������ �� ������������ VIP �����������
	 *
	 * @var bool
	 */
	public $Authorization;
	
	
	/**
	 * �������� ������������
	 * @return User
	 */
	public function User(){
		$this->idvip=0;
		//������������������ ������������
		if (array_key_exists('UserCook',$_COOKIE) and array_key_exists('UserHash',$_COOKIE)) {
			$this->UserCookiesRead($_COOKIE['UserCook'],$_COOKIE['UserHash']);		
		}else $this->UserInit();
		//���������������� (VIP) ������������
		if (array_key_exists('VIPkey',$_COOKIE)){
			$VIPkey=$_COOKIE['VIPkey'];
			$key=substr($VIPkey,0,32);
			$pwh=substr($VIPkey,32,32);
			$idvip=(int)substr($VIPkey,64);
			$this->UserSqlRead($idvip);
			if ($this->pwh==$pwh)$this->Authorization=true;
		}
		$this->UpdateUserVisits();
	}
	
	/**
	 * �������� cookies ����� ��� ������������������� (VIP) ������������
	 * @return string
	 */	
	public function GetVIPkey(){
		if ($this->Authorization){
			$key=$this->pwh.$this->idvip.'kjh98gfhj';
			return md5($key).$this->pwh.$this->idvip;
		}else return 'bad';
	}
	/**
	 * ��������� ������ ��� ������ ������������
	 *
	 */
	private function UserInit(){
		$f=fopen('count.txt','r+');
			$this->id=fgets($f)+1;
		fseek($f,0);
		fwrite($f,$this->id);
		fclose($f);
			$this->firstvis=time();
			$this->previs=$this->firstvis;
			$this->lastvis=$this->firstvis;
			$this->visits=1;
			$this->forum=0;	
	}

	/**
	 * ������ ������ �� cookies, �������� �� ������������ � ������� ���� md5
	 * @param string $data
	 * @param string $hash
	 */
	private function UserCookiesRead($data,$hash){
		$tmp=explode('@',$data);
		$us=array();
		foreach ($tmp as $key => $value){
			$param=explode('_',$value);
			switch ($param[0]) {
				case 'id': $this->id=(int)$param[1]; break;
				case 'previs': $this->previs=(int)$param[1]; break;
				case 'firstvis': $this->firstvis=(int)$param[1]; break;
				case 'lastvis': $this->lastvis=(int)$param[1]; break;
				case 'visits': $this->visits=(int)$param[1]; break;
				case 'forum': $this->forum=(int)$param[1]; break;
				default: break;
			}
		}
		if ($this->GetHash()!=$hash) $this->UserInit();
	}
	
	/**
	 * ��������� ���������� ������� � ����� ���������� ������. ��� VIP ������������� ���������� ������� � ��
	 *
	 */
	private function UpdateUserVisits(){
			if (time()>$this->lastvis+self::$VisInterval) {//���� ������ 3 ���� (10800 ���) � ������� ���������� ������ - ������������� ����� ����� � ����������� ����� ���������
				$this->previs=$this->lastvis;
				$this->lastvis=time();
				$this->visits++;
				if ($this->Authorization){
					$sqlstr="UPDATE user_reg SET lastvis=".$this->lastvis.", previs=".$this->previs.",visits=".$this->visits." WHERE idvip=".$this->idvip;
					self::$SQL_DB->Query($sqlstr);
				}
			}
	}
		
	/**
	 * ������ � ��������� ������� User �� ���� ������
	 * @param mix $mailORid 
	 * @return bool
	 */
	private function UserSqlRead($mailORid){
		if (is_int($mailORid)) $sqlstr="SELECT * FROM user_reg WHERE idvip=".$mailORid;
		else $sqlstr="SELECT * FROM user_reg WHERE email='".$mailORid."'";
	
		if (!self::$SQL_DB->Connect()) return 'ERR|<b>��������, �������� ������ ��� ����������� � ���� ������. �������� ��� ��������� �������� �� ������� ����������� ������. ����������, ����������� ������������������ ����� ��� �������� �������������� ����� �� ������ temp@rustea.com</b><br>';
		$qr=self::$SQL_DB->Query($sqlstr);
		if (mysql_num_rows($qr)>0) {
			$VIPdata=mysql_fetch_assoc($qr);
			foreach ($VIPdata as $key => $val){
				switch ($key) {
					case 'idvip':	$this->idvip=(int)$val;		break;
					case 'email':	$this->email=(string)$val;	break;
					case 'name':	$this->name=(string)$val;	break;
					case 'sname':	$this->sname=(string)$val;	break;
					case 'nike':	$this->nike=(string)$val;	break;
					case 'city':	$this->city=(string)$val;	break;
					case 'pwh':		$this->pwh=(string)$val;	break;
					case 'pwhnew':	$this->pwhnew=(string)$val;	break;
					case 'passwdate':$this->passwdate=(int)$val;break;
					case 'passwerr':$this->passwerr=(int)$val;break;
					case 'forumset':$this->forumset=(string)$val;break;
					case 'userset':	$this->userset=(string)$val;break;
					case 'status':	$this->status=(int)$val;	break;
					case 'complaint':$this->complaint=(int)$val;break;
					case 'id':		$this->id=(int)$val;		break;
					case 'firstvis':$this->firstvis=(int)$val;	break;
					case 'previs':	$this->previs=(int)$val;	break;
					case 'lastvis':	$this->lastvis=(int)$val;	break;
					case 'visits':	$this->visits=(int)$val;	break;
					default:break;}
			}return true;
		}else return false;
	}
		
	/**
	 * ��������� ���������� � ������������ � ������� JSON (JavaScript) ��� ������ � Coocies
	 * @return string
	 */
	public function GetJS_CoociesData(){		
		return 'User.Cook={id:'.$this->id.',firstvis:'.$this->firstvis.',previs:'.$this->previs.',lastvis:'.$this->lastvis.',visits:'.$this->visits.',forum:"'.$this->forum.'"};UserHash="'.$this->GetHash().'";';
	}
	
	/**
	 * ��������� ���������� � VIP ������������ � ������� JSON (JavaScript)
	 * �������� ������. ��� ������������� ��������� ������ ������
	 * @return string
	 */
	public function GetJS_VIPUserData(){
		if ($this->Authorization) 
			return 'User={VIP:true,email:"'.$this->email.'",name:"'.$this->name.'",sname:"'.$this->sname.'",nike:"'.$this->nike.
			'",city:"'.$this->city.'",passwdate:'.$this->passwdate.",forumset:'".$this->forumset."',userset:'".$this->userset."',status:".$this->status.
			',complaint:'.$this->complaint.',idvip:'.$this->idvip.',id:'.$this->id.',firstvis:'.$this->firstvis.',previs:'.$this->previs.',lastvis:'.$this->lastvis.',visits:'.$this->visits.'};';
		else return 'User={VIP:false,id:'.$this->id.',firstvis:'.$this->firstvis.',previs:'.$this->previs.',lastvis:'.$this->lastvis.',visits:'.$this->visits.'};';
	}
	
	/**
	 * �������� ������. ��� ������������� ��������� ������ ������
	 * @return string
	 */
	public function TestPassword(){
		$this->Authorization=false;
		$this->email=strtolower(trim($_POST['RegForm_login']));
		if ($this->UserSqlRead($this->email)){//���� ������ � ��������� mail ����������
			if ($this->passwerr<=10 or time()>$this->passwerr){//���������� ��������� �������
				$this->UpdateUserVisits();
				$pw=md5(trim($_POST['RegForm_pw']));
				if ($pw==$this->pwh) {//���������� �� ������ �������
					$this->passwerr=0;
					$sqlstr="UPDATE user_reg SET passwerr=0, lastvis=".$this->lastvis.", previs=".$this->previs.", visits=".$this->visits." WHERE idvip=".$this->idvip;
					self::$SQL_DB->Query($sqlstr);
					$this->Authorization=true;return '<span style="color:green">����� ����������!</span>';	
				}elseif ($pw==$this->pwhnew) {//���������� � ����� ������� (������ ������� ������ �� �����)
					$this->passwerr=0;
					$this->pwh=$this->pwhnew;
					$sqlstr="UPDATE user_reg SET passwerr=0, lastvis=".$this->lastvis.", previs=".$this->previs.", visits=".$this->visits.", pwh='".$this->pwh."' WHERE idvip=".$this->idvip;
					self::$SQL_DB->Query($sqlstr);
					$this->Authorization=true;return '<span style="color:green">����� ����������! �� ����������� ���� ����������� �� ����� �����!</span>';
				}else{
					if ($this->passwerr>=10) $this->passwerr=time()+30; else $this->passwerr++;//������� ��������� ������� ��� ������������� ����� ��������� ������� ����� 30���
					$sqlstr="UPDATE user_reg SET passwerr=".$this->passwerr." WHERE idvip=".$this->idvip;
					self::$SQL_DB->Query($sqlstr);
					return '<span style="color:red">�������� ������!</span>';
				}
			}else return '<span style="color:red">������� ����� ��������� ������� ����� ������. ���� ������� ������ ������ ������������� � ����� ������������� �� 30 ��� ����� ������ ��������� �������.</span>';
		}else return '<span style="color:red">�� �� ���������������� ���� ��������� ������ ��� ����� email!</span>';
	}
	
	/**
	 * ���������� ��������� md5 ���� �� "���������" ��������� 'KneD5W' ��� ������ �������� � Cookies ��������������������� ������������ 
	 * @return int
	 */
	private function GetHash(){
		return md5($this->id.'|'.$this->firstvis.'|'.$this->lastvis.'|'.$this->previs.'|'.$this->visits.'|'.$this->forum.'|'.'KneD5W');	
	}
	
	/**
	 * ����������� ������ ������������
	 *
	 * @param array $p $_POST 
	 * @param array $c $_COOKIE
	 */
	public function UserRegistration(){
		$p=$_POST; $c=$_COOKIE;
		$this->email=strtolower(trim($p['RegForm_email']));
		$this->name=trim($p['RegForm_name']);
		$this->sname=trim($p['RegForm_sname']);
		$this->city=trim($p['RegForm_city']);
		$this->nike=trim($p['RegForm_nike']);
		$SeqCode=trim($p['RegForm_SeqCode']);
		
		//�������� ����������� ����		
		if (array_key_exists('SeqCodeHesh',$c) and $c['SeqCodeHesh']==md5($SeqCode.'ljhg')) {			
			$num=crc32(md5($this->email));
			if ($num<0) $num*=-1;
			if ($num<100) $num+=100;
			if (substr($num,0,3)!=substr($SeqCode,0,3)) return 'ERR|����� ������� �� ����� - ������� 2';
		}
		else return 'ERR|<span style="color:red">����� ������� �� �����</span>';
		
		//�������� ������
		$s='';		
		if (!preg_match('/^[A-z\d_\.\-]+@[A-z\d_\.\-]+\.[A-z]{2,3}$/',$this->email)) $s.='����������� ����� <b>mail</b><br>';
		if (strlen($this->email)>64) $s.='��������, ��� <b>mail</b> ����� ����� ����� 64 �������� � ������� �� ����� �������������� ��� �����������.<br>';
		if (strlen($s)) return 'ERR|<span style="color:red">'.$s.'</span>';
		
		$sqlstr="SELECT passwdate FROM user_reg WHERE email='".$this->email."'";
		if (!self::$SQL_DB->Connect()) return 'ERR|<b>��������, �������� ������ ��� ����������� � ���� ������. �������� ��� ��������� �������� �� ������� ����������� ������. ����������, ����������� ������������������ ����� ��� �������� �������������� ����� �� ������ temp@rustea.com</b><br>';
		$qr=self::$SQL_DB->Query($sqlstr);
		if (mysql_num_rows($qr)>0) {//���� email ��� ���������������
			
			//��������� ��������� �������� ������ 
			$this->passwdate=mysql_result($qr,0);
			if (time()>$this->passwdate+21600){//�� ���� ��� ��� � 6 ����� 21600
				
				//��������� � �������� ������ ������
				$pw=substr(md5(rand(0,99999999)),0,8);
				$messag="��� ��� ������������ ����� ������ ��� ����� �� ���� ".$_SERVER['SERVER_NAME'].", �.�. ��� Email ��� ������ � ������.\n���� ��� ������ ������� ��������, �� �� �������� ������ ������������ ������ ������.\n\n���� �� ����������� ������, ���������� ����, ������ ������ ������ ��������������".
					"\n\n��� ����� ������ = $pw\n\n� ���������, ".MAIL::$SysAdmin;
				if (!MAIL::SendMail($this->email,'���������� ����������� �� ����� '.$_SERVER['SERVER_NAME'],$messag)) return 'ERR|<b>������ ��� �������� ��������� ���������</b>';
				
				//���������� ������ ������������
				$sqlstr="UPDATE user_reg SET passwdate=".time().",pwhnew='".md5($pw)."' WHERE email='".$this->email."'";
				$qr=self::$SQL_DB->Query($sqlstr);
				return 'OK|<span style="color:blue"><b>�� ��� ���� ���������������� �����. ��� �������� ������ ������.</b></span>';
			}else{
				return 'ERR|<span style="color:red"><b>�� ��� ���������������� � ������ ������� ��� ��� ������ ������. ��������� �������� ������ �������� ������ ����� 6 �����</b></span>';
			}
		}
		else {//���� email �� ���������������
			if (!preg_match('/^[A-z�-���\- ]{2,32}$/',$this->name)) $s.='����������� ������� <b>���</b> ��� �������� � ����� ����� 32<br>';
			if (!preg_match('/^[A-z�-���\- ]{2,32}$/',$this->sname)) $s.='����������� ������� <b>�������</b> ��� �������� � ������ ����� 32<br>';
			if (!preg_match('/^[A-z\d�-���\- ]{2,32}$/',$this->nike)) $s.='����������� ������ <b>���</b> ��� �������� � ���� ����� 32<br>';
			if (!preg_match('/^[A-z�-���\- ]{2,32}$/',$this->city)) $s.='����������� ������ <b>�����</b> ��� �������� � �������� ������ ����� 32<br>';
			
			$sqlstr="SELECT nike FROM user_reg WHERE nike='".$this->nike."'";//�������� ������������� ����
			$qr=self::$SQL_DB->Query($sqlstr);
			if (mysql_num_rows($qr)>0) $s.='��������, <b>��������� ���� ��� ��� ������������</b>, ���������� �������� ���� ������ ���.<br>';
			
			if (strlen($s)) return $s='ERR|<span style="color:red">'.$s.'</span>';//���� ��������� ������ ��� ��������

			//��������� � �������� ������
			$pw=substr(md5(rand(0,99999999)),0,8);
			$messag="������������!\n\n".
				'�� ���������������� �� ����� '.$_SERVER['SERVER_NAME']." �.�. ��� �������� ����� ������ ��� ���������� ������.\n".
				"���� �� �� ���������������� �� ����� �����, ����������� ��� ������ � ��������� ����������� ����� �������.\n".
				"��� ������������� �����������, ����������, ������� �� ��� ���� ��������� ������, ��������� ����, � ������� 36 ����� � ������� �����������.\n\n".
				"��� ������ = $pw \n����� ����������� - ".date('d F Y H:i')."\n\n���� � ��� �������� ������� � ����� � ������������, �� ������ ��������� �� � �������� ������, �� ������� ��������� ������!\n\n� ��������, ".MAIL::$SysAdmin;
			if (!MAIL::SendMail($this->email,'����������� �� ����� '.$_SERVER['SERVER_NAME'],$messag)) return 'ERR|<b>������ ��� �������� ��������� ���������</b>';

			//������ � ���� ������
			$this->pwh=md5('NoRegUser523');
			$this->pwhnew=md5($pw);
			$this->passwdate=time();
			$this->status=0xFF;
			
			$sqlstr="INSERT INTO user_reg SET ".
					"email='".$this->email."', ".
					"name='".$this->name."', ".
					"sname='".$this->sname."', ".
					"nike='".$this->nike."', ".
					"city='".$this->city."', ".
					"firstvis=".$this->firstvis.", ".
					"previs=".$this->previs.", ".
					"lastvis=".$this->lastvis.", ".
					"visits=".$this->visits.", ".
					"id=".$this->id.", ".
					"passwdate=".$this->passwdate.", ".
					"pwh='".$this->pwh."', ".
					"pwhnew='".$this->pwhnew."', ".
					"status=".$this->status;
			$res=self::$SQL_DB->Query($sqlstr);
			if ($res) {
				$this->Authorization=true;
				return 'OK|<span style="color:green"><b>�����������! �� ������� ����������������. ������ ��� ����� ������ ��� �� �����.</b><br>���� �� �� �������� ������ � ������� � ������� 10-20 �����, ��������� ������ �� agent@dance007.ru c �������� ������� ������.</span>';
			}
			else return 'ERR|<b>��������, �������� ������ ��� ������ � ���� ������. �������� ��� ��������� �������� �� ������� ����������� ������. ����������, ����������� ������������������ ����� ��� �������� �������������� ����� �� ������ temp@rustea.com</b><br>';	
		}	
	}
		
	/**
	 * ����� ���� ������ ������������ � ������
	 * @return string
	 */
	public function __toString(){
		$s='';
		foreach ($this as $prop => $val) $s.=$prop.' = '.$val.'<br>';
		return $s;
	}
}

/**
 * ����� ���������� ���������
 *
 */
class DBG {
	private static $Mess;
	/**
	 * ��������� �������� ��������� ���������� ���������
	 *
	 * @var unknown_type
	 */
	public static $Enable=false;

	/**
	 * ���������� ���������� ��� ����������� ������
	 *
	 * @param string $mess
	 */
	public static function AddInfo($mess) {
		self::$Mess.='<br>'.$mess;
	}
	/**
	 * ����� ���� ����������� ����������
	 *
	 * @return string
	 */
	public static function toString(){
		return self::$Mess;		
	}
}

class MAIL {
	public static $Header="Content-type: text/plain; charset=Windows-1251\nContent-Transfer-Encoding: 8bit\n";
	
	public static $WriteToFile=false;
	public static $SysAdmin='������������� �����';
	public static $SysAdminMail='';

	/**
	 * ���������� �������� ���������. ��� �������� �������� ���������� true
	 * � ������ ������� ���������� ��������� � ���� mail.txt
	 * @param string $mail
	 * @param string $title
	 * @param string $mess
	 * @return bool
	 */
	public static function SendMail($mail,$title,$mess) {
		if (self::$WriteToFile) {
			$f=fopen('mail.txt','a');
			fwrite($f,"\n\n------------------\n\n".'To:'.$mail."\t".$title."\t".$mess."\n");
			fclose($f);
			return true;
		}
		else {
			mail(self::$SysAdminMail,"$title $mail",$mess,self::$Header."From: ".self::$SysAdminMail."\n");
			return mail($mail,$title,$mess,self::$Header."From: ".self::$SysAdminMail."\n");
		}
	}
}

?>