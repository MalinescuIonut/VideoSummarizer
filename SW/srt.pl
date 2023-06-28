#$DELAY=$ARGV[0];
#$NUM=$ARGV[1];
#$DEN=$ARGV[2];

while ($_=<stdin>) {
  if (/-->/) {
    chomp;
	@c=split(/[\s\:\,]/,$_);
	#printf stdout "$c[0] $c[1] $c[2] $c[3]\n";
	#printf stdout "$c[5] $c[6] $c[7] $c[8]\n";
	$s1=$c[0]*3600+$c[1]*60+$c[2]+$c[3]/1000-$DELAY;
    $s1=$s1*$NUM/$DEN;
	$s2=$c[5]*3600+$c[6]*60+$c[7]+$c[8]/1000-$DELAY;
    $s2=$s2*$NUM/$DEN;
	if ($s1<0) {
	  $s1=0;
	}
	if ($s2<0) {
	  $s2=0;
	}
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

