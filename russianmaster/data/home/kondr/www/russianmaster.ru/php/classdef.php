<?php 

User::$SQL_DB=new SQLDB('localhost','kondr_mfst','kondr_umfst','asdwtey29Gd');

MAIL::$SysAdmin='Кондратенков Владимир, администратор сайта.';
MAIL::$SysAdminMail='temp@rustea.com';

if ($_SERVER['SERVER_NAME']=='rm' or $_SERVER['SERVER_NAME']=='rm.ru') {
	MAIL::$WriteToFile=true;
	DBG::$Enable=true;
}

User::$VisInterval=10800;//Интервал в сек, после которого засчитывается новый визит. 3 часа=10800 сек

/**
 * Подключение к базе данных
 *
 */
class SQLDB {
	public $SQL_DB_HOST;
	public $SQL_DB_NAME;
	public $SQL_USER;
	public $SQL_PW;
	
	/**
	 * Подключение к базе данных
	 * @var resource
	 */
	private $dblink;
	private $dbres;
	
	/**
	 * СОздание объекта для подключения к БД
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
	 * Подключение и выбор базы данных
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
	 * Отключение от базы
	 *
	 */
	public function Disconnect(){mysql_close($this->dblink);}
	/**
	 * Запрос к базе данных
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
	 * Распечатка свойств
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
 * Данные о пользователе
 *
 */
class User{
	/**
	 * Интервал в сек, после которого засчитывается новый визит.
	 * @var int
	 */	
	public static $VisInterval;
	/**
	 * Идентификатор обычного пользователя
	 * @var int
	 */
	public $id;
	/**
	 * Время первого визита в системе Unix
	 * @var int
	 */
	public $firstvis;	
	/**
	 * Время предыдущего визита в системе Unix
	 * @var int
	 */
	public $previs;
	/**
	 * Время предыдущего визита за последние 3 часа в системе Unix
	 * @var int
	 */
	public $lastvis;
	/**
	 * Количество визитов
	 * @var int
	 */
	public $visits;	
	/**
	 * Информация для форума
	 * @var string
	 */	
	public $forum;		
	
	/**
	 * Идентификатор VIP пользователя (зарегистрированного
	 * @var int
	 */
	public $idvip;
	/**
	 * email
	 * @var string
	 */
	public $email;
	/**
	 * Имя пользователя
	 *
	 * @var string
	 */
	public $name;
	/**
	 * Фамилия пользователя
	 * @var string
	 */
	public $sname;
	/**
	 * Ник пользователя
	 * @var string
	 */
	public $nike;
	/**
	 * Город
	 * @var string
	 */
	public $city;
	
	/**
	 * md5 - хеш пароля
	 * @var string
	 */
	public $pwh;
	/**
	 * md5 - хеш нового пароля
	 * @var string
	 */
	public $pwhnew;
	/**
	 * Дата обновления и отсылки пароля
	 * @var int
	 */
	public $passwdate;
	/**
	 * Если меньше 100 - количество ошибочных попыток ввода пароля
	 * Если больше 100 - время до которого заблокирована запись
	 * @var int
	 */
	public $passwerr;
	/**
	 * Статус (разрешения) пользователя
	 * @var int
	 */
	public $status;
	/**
	 * Количество жалоб на пользователя
	 * @var int
	 */
	public $complaint;
	
		
	/**
	 * Настройки для форума
	 * @var string
	 */
	public $forumset;
	/**
	 * Прочие пользовательские настройки
	 * @var string
	 */
	public $userset;

	/**
	 * Ссылка на объект базы данных
	 *
	 * @var SQLDB
	 */
	public static $SQL_DB;

	/**
	 * Показывает, прошел ли пользователь VIP авторизацию
	 *
	 * @var bool
	 */
	public $Authorization;
	
	
	/**
	 * Создание пользователя
	 * @return User
	 */
	public function User(){
		$this->idvip=0;
		//Нерегистрированный пользователь
		if (array_key_exists('UserCook',$_COOKIE) and array_key_exists('UserHash',$_COOKIE)) {
			$this->UserCookiesRead($_COOKIE['UserCook'],$_COOKIE['UserHash']);		
		}else $this->UserInit();
		//Регистрированный (VIP) пользователь
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
	 * Создание cookies ключа для зарегистрированного (VIP) пользователя
	 * @return string
	 */	
	public function GetVIPkey(){
		if ($this->Authorization){
			$key=$this->pwh.$this->idvip.'kjh98gfhj';
			return md5($key).$this->pwh.$this->idvip;
		}else return 'bad';
	}
	/**
	 * Установка данных для нового пользователя
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
	 * Чтение данных из cookies, проверка их корректности с помощью хеша md5
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
	 * Вычисляет количество визитов и время последнего визита. Для VIP пользователей записывает даннные в БД
	 *
	 */
	private function UpdateUserVisits(){
			if (time()>$this->lastvis+self::$VisInterval) {//Если прошло 3 часа (10800 сек) с момента последнего визита - устанавливаем новое время и засчитываем новое посещение
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
	 * Чтение и установка свойств User из базы данных
	 * @param mix $mailORid 
	 * @return bool
	 */
	private function UserSqlRead($mailORid){
		if (is_int($mailORid)) $sqlstr="SELECT * FROM user_reg WHERE idvip=".$mailORid;
		else $sqlstr="SELECT * FROM user_reg WHERE email='".$mailORid."'";
	
		if (!self::$SQL_DB->Connect()) return 'ERR|<b>Извините, поизощла ошибка при подключении к базе данных. Возможно наш провайдер проводит на сервере технические работы. Пожалуйста, попытайтесь зарегистрироваться снова или сообщите администратору сайта по адресу temp@rustea.com</b><br>';
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
	 * Получение информации о пользователе в формате JSON (JavaScript) для записи в Coocies
	 * @return string
	 */
	public function GetJS_CoociesData(){		
		return 'User.Cook={id:'.$this->id.',firstvis:'.$this->firstvis.',previs:'.$this->previs.',lastvis:'.$this->lastvis.',visits:'.$this->visits.',forum:"'.$this->forum.'"};UserHash="'.$this->GetHash().'";';
	}
	
	/**
	 * Получение информации о VIP пользователе в формате JSON (JavaScript)
	 * Проверка пароля. При необходимости установка нового пароля
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
	 * Проверка пароля. При необходимости установка нового пароля
	 * @return string
	 */
	public function TestPassword(){
		$this->Authorization=false;
		$this->email=strtolower(trim($_POST['RegForm_login']));
		if ($this->UserSqlRead($this->email)){//Если запись с указанным mail существует
			if ($this->passwerr<=10 or time()>$this->passwerr){//Количество ошибочных попыток
				$this->UpdateUserVisits();
				$pw=md5(trim($_POST['RegForm_pw']));
				if ($pw==$this->pwh) {//Совпадение со старым паролем
					$this->passwerr=0;
					$sqlstr="UPDATE user_reg SET passwerr=0, lastvis=".$this->lastvis.", previs=".$this->previs.", visits=".$this->visits." WHERE idvip=".$this->idvip;
					self::$SQL_DB->Query($sqlstr);
					$this->Authorization=true;return '<span style="color:green">Добро пожаловать!</span>';	
				}elseif ($pw==$this->pwhnew) {//Совпадение с новым паролем (Замена старого пароля на новый)
					$this->passwerr=0;
					$this->pwh=$this->pwhnew;
					$sqlstr="UPDATE user_reg SET passwerr=0, lastvis=".$this->lastvis.", previs=".$this->previs.", visits=".$this->visits.", pwh='".$this->pwh."' WHERE idvip=".$this->idvip;
					self::$SQL_DB->Query($sqlstr);
					$this->Authorization=true;return '<span style="color:green">Добро пожаловать! Вы подтвердили свою регистрацию на нашем сайте!</span>';
				}else{
					if ($this->passwerr>=10) $this->passwerr=time()+30; else $this->passwerr++;//Считаем ошибочные попытки или устанавливаем время следующей попытки через 30сек
					$sqlstr="UPDATE user_reg SET passwerr=".$this->passwerr." WHERE idvip=".$this->idvip;
					self::$SQL_DB->Query($sqlstr);
					return '<span style="color:red">Неверный пароль!</span>';
				}
			}else return '<span style="color:red">Слишком много ошибочных попыток ввода пароля. Ваша учетная запись сейчас заблокирована и будет блокироваться на 30 сек после каждой ошибочной попытки.</span>';
		}else return '<span style="color:red">Вы не зарегистрированы либо допустили ошибку при вводе email!</span>';
	}
	
	/**
	 * Вычисление защитного md5 хеша со "случайной" затравкой 'KneD5W' для данных хранимых в Cookies незарегистрированного пользователя 
	 * @return int
	 */
	private function GetHash(){
		return md5($this->id.'|'.$this->firstvis.'|'.$this->lastvis.'|'.$this->previs.'|'.$this->visits.'|'.$this->forum.'|'.'KneD5W');	
	}
	
	/**
	 * Регистрация нового пользователя
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
		
		//Проверка контрольных цифр		
		if (array_key_exists('SeqCodeHesh',$c) and $c['SeqCodeHesh']==md5($SeqCode.'ljhg')) {			
			$num=crc32(md5($this->email));
			if ($num<0) $num*=-1;
			if ($num<100) $num+=100;
			if (substr($num,0,3)!=substr($SeqCode,0,3)) return 'ERR|Цифры введены не верно - вариант 2';
		}
		else return 'ERR|<span style="color:red">Цифры введены не верно</span>';
		
		//Проверка данных
		$s='';		
		if (!preg_match('/^[A-z\d_\.\-]+@[A-z\d_\.\-]+\.[A-z]{2,3}$/',$this->email)) $s.='Неправильно задан <b>mail</b><br>';
		if (strlen($this->email)>64) $s.='Извините, Ваш <b>mail</b> имеет длину более 64 символов и поэтому не может использоваться для регистрации.<br>';
		if (strlen($s)) return 'ERR|<span style="color:red">'.$s.'</span>';
		
		$sqlstr="SELECT passwdate FROM user_reg WHERE email='".$this->email."'";
		if (!self::$SQL_DB->Connect()) return 'ERR|<b>Извините, поизощла ошибка при подключении к базе данных. Возможно наш провайдер проводит на сервере технические работы. Пожалуйста, попытайтесь зарегистрироваться снова или сообщите администратору сайта по адресу temp@rustea.com</b><br>';
		$qr=self::$SQL_DB->Query($sqlstr);
		if (mysql_num_rows($qr)>0) {//Если email уже зарегистрирован
			
			//Повторная генерация забытого пароля 
			$this->passwdate=mysql_result($qr,0);
			if (time()>$this->passwdate+21600){//не чаще чем раз в 6 часов 21600
				
				//Генерация и отправка нового пароля
				$pw=substr(md5(rand(0,99999999)),0,8);
				$messag="Для Вас сгенерирован новый пароль для входа на сайт ".$_SERVER['SERVER_NAME'].", т.к. Ваш Email был указан в заявке.\nЕсли это письмо Выслано ошибочно, Вы по прежнему можете использовать старый пароль.\n\nЕсли Вы используете пароль, приведеный ниже, старый пароль станет недействителен".
					"\n\nВаш новый пароль = $pw\n\nС уважением, ".MAIL::$SysAdmin;
				if (!MAIL::SendMail($this->email,'Обновление регистрации на сайте '.$_SERVER['SERVER_NAME'],$messag)) return 'ERR|<b>Ошибка при отправке почтоовго сообщения</b>';
				
				//Обновление записи пользователя
				$sqlstr="UPDATE user_reg SET passwdate=".time().",pwhnew='".md5($pw)."' WHERE email='".$this->email."'";
				$qr=self::$SQL_DB->Query($sqlstr);
				return 'OK|<span style="color:blue"><b>Вы уже были зарегистрированы ранее. Вам повторно выслан пароль.</b></span>';
			}else{
				return 'ERR|<span style="color:red"><b>Вы уже зарегистрированы и совсем недавно Вам уже выслан пароль. Повторная отправка пароля возможна только через 6 часов</b></span>';
			}
		}
		else {//Если email не зарегистрирован
			if (!preg_match('/^[A-zА-яёЁ\- ]{2,32}$/',$this->name)) $s.='Неправильно указано <b>имя</b> или символов в имени более 32<br>';
			if (!preg_match('/^[A-zА-яёЁ\- ]{2,32}$/',$this->sname)) $s.='Неправильно указана <b>фамилия</b> или символов в фамлии более 32<br>';
			if (!preg_match('/^[A-z\dА-яёЁ\- ]{2,32}$/',$this->nike)) $s.='Неправильно указан <b>ник</b> или символов в нике более 32<br>';
			if (!preg_match('/^[A-zА-яёЁ\- ]{2,32}$/',$this->city)) $s.='Неправильно указан <b>город</b> или символов в названии города более 32<br>';
			
			$sqlstr="SELECT nike FROM user_reg WHERE nike='".$this->nike."'";//Проверка существования ника
			$qr=self::$SQL_DB->Query($sqlstr);
			if (mysql_num_rows($qr)>0) $s.='Извините, <b>выбранный Вами ник уже используется</b>, пожалуйста выберите себе другой ник.<br>';
			
			if (strlen($s)) return $s='ERR|<span style="color:red">'.$s.'</span>';//Если произошли ошибки при проверке

			//Генерация и отправка пароля
			$pw=substr(md5(rand(0,99999999)),0,8);
			$messag="Здравствуйте!\n\n".
				'Вы зарегистрированы на сайте '.$_SERVER['SERVER_NAME']." т.к. Ваш почтовый адрес указан при заполнении анкеты.\n".
				"Если Вы не регистрировались на нашем сайте, игнорируйте это письмо и ошибочная регистрация будет удалена.\n".
				"Для подтверждения регистрации, пожалуйста, войдите на наш сайт используя пароль, указанный ниже, в течении 36 часов с момента регистрации.\n\n".
				"Ваш пароль = $pw \nВремя регистрации - ".date('d F Y H:i')."\n\nЕсли у Вас возникли вопросы в связи с регистрацией, Вы можете отправить их в ответном письме, НЕ ИЗМЕНЯЯ ЗАГОЛОВОК ПИСЬМА!\n\nС уваженим, ".MAIL::$SysAdmin;
			if (!MAIL::SendMail($this->email,'Регистрация на сайте '.$_SERVER['SERVER_NAME'],$messag)) return 'ERR|<b>Ошибка при отправке почтоовго сообщения</b>';

			//Запись в базу данных
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
				return 'OK|<span style="color:green"><b>ПОЗДРАВЛЯЕМ! Вы успешно зарегистрированы. Пароль для входа выслан Вам по почте.</b><br>Если Вы не получите письмо с паролем в течении 10-20 минут, отправьте письмо на agent@dance007.ru c просьбой выслать пароль.</span>';
			}
			else return 'ERR|<b>Извините, поизощла ошибка при записи в базу данных. Возможно наш провайдер проводит на сервере технические работы. Пожалуйста, попытайтесь зарегистрироваться снова или сообщите администратору сайта по адресу temp@rustea.com</b><br>';	
		}	
	}
		
	/**
	 * Вывод всех данных пользователя в строку
	 * @return string
	 */
	public function __toString(){
		$s='';
		foreach ($this as $prop => $val) $s.=$prop.' = '.$val.'<br>';
		return $s;
	}
}

/**
 * Вывод отладочных сообщений
 *
 */
class DBG {
	private static $Mess;
	/**
	 * Позволяет подавить появление отладочных сообщений
	 *
	 * @var unknown_type
	 */
	public static $Enable=false;

	/**
	 * Добавление информации для последующей печати
	 *
	 * @param string $mess
	 */
	public static function AddInfo($mess) {
		self::$Mess.='<br>'.$mess;
	}
	/**
	 * Вывод всей накопленной информации
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
	public static $SysAdmin='Администрация сайта';
	public static $SysAdminMail='';

	/**
	 * ОТправляет почтовое сообщение. При успешной отправке возвращает true
	 * В режиме отладки записывает сообщение в файл mail.txt
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