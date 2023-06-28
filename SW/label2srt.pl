$cont=1;
$_=<stdin>;
while ($_=<stdin>) {
	chomp;
	@c=split(/\t/,$_);
	$msg=$c[0];
	$s2=$c[1];
	$s1=$c[2];
	printf stdout "%d\n",$cont;
	printf stdout "%02d:%02d:%02d,%03d --> ",
		int($s2/3600), int(($s2%3600)/60), int($s2%60), int(($s2-int $s2)*1000);
	printf stdout "%02d:%02d:%02d,%03d\n$msg $cont\n\n",
		int($s1/3600), int(($s1%3600)/60), int($s1%60), int(($s1-int $s1)*1000);
	$cont++;
	}
