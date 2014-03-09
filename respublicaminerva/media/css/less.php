<?php
$files = array('stylesheet.less.css');
foreach ($files as $file) 
	$hashs[$file] = '';

for (;;) {
	usleep(100000);
	foreach ($files as $file) {
		$t = md5_file($file);
		if ($t != $hashs[$file]) {
			$hashs[$file] = $t;
			$target = str_replace('.less.', '.', $file);
			`lessc $file 1> $target`;
			echo date("H:s")."	$file changed\n";
		}
	}
}

