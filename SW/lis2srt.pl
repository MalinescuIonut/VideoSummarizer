$step=$ARGV[0];
$msg=$ARGV[1];
$s2=0;
$cont=1;
while ($_=<stdin>) {
	chomp;
	if ($step>1) {
		$s2=$_;
		if  (eof(stdin)) {
		} else {
			$_=<stdin>;
			chomp;
			}
		$s1=$_;
	} else {
		$s1=$_;
		}
	printf stdout "%d\n",$cont;
	printf stdout "%02d:%02d:%02d,%03d --> ",
		int($s2/3600), int(($s2%3600)/60), int($s2%60), int(($s2-int $s2)*1000);
	printf stdout "%02d:%02d:%02d,%03d\n$msg $cont\n\n",
		int($s1/3600), int(($s1%3600)/60), int($s1%60), int(($s1-int $s1)*1000);
	$cont++;
	$s2=$s1;
	}
