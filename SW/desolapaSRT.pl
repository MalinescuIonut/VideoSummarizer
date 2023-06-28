$prev=0;
while ($_=<stdin>) {
  if (/-->/) {
    chomp;
	@c=split(/[\s\:\,]/,$_);
	$s1=$c[0]*3600+$c[1]*60+$c[2]+$c[3]/1000;
	$s2=$c[5]*3600+$c[6]*60+$c[7]+$c[8]/1000;
	if ($s1<$prev) {
	  $s1=$prev;
	  }
	if ($s2<$prev) {
	  $s2=$prev;
	  }
	$prev=$s2;
    printf stdout "%02d:%02d:%02d,%03d --> %02d:%02d:%02d,%03d\n", 
		int($s1/3600), int(($s1%3600)/60), int($s1%60), int(($s1-int $s1)*1000), 
		int($s2/3600), int(($s2%3600)/60), int($s2%60), int(($s2-int $s2)*1000);
	}
	elsif (/^\d/) {
	printf stdout "\n";
	print stdout;
	}
	else {
	print stdout;
	}
}
