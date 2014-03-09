<?php 
header("Content-Type: text/html; charset=windows-1251");

//Список файлов JS
if (array_key_exists('filetype',$_POST)){
	echo "files=[\n";
	if ($handle = opendir('datafile/')) {
	    while (false !== ($file = readdir($handle))) {
	        if (preg_match('/.js$/',$file)) {
	            echo "'$file',\n";
	        }
	    }
	    closedir($handle);
	}
	echo ",null];files.pop();\n\n";
}
//Список файлов c результатами
if (array_key_exists('filesRes',$_POST)){
	echo "filesRes=[\n";
	if ($handle = opendir('datafile/result/')) {
	    while (false !== ($file = readdir($handle))) echo "'$file',\n";
	    closedir($handle);
	}
	echo ",null];filesRes.pop();\n\n";
}

//Читаем и посылаем для разбора JS файл

if (array_key_exists('evalJSfile',$_POST)){
	$evalJSfile=$_POST['evalJSfile'];
	readfile($evalJSfile);
}

?>