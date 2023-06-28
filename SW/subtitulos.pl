$step=$ARGV[0];
$todos=$ARGV[1];
$prevT=0;
while ($_=<stdin>) {
 if (/\d\d\:\d\d\:\d\d\,\d\d\d \-\-\> \d\d\:\d\d\:\d\d\,\d\d\d/) {
	@c=split(/[\:\,\s]/,$_);
#	print;
	$t1=$c[0]*3600+$c[1]*60+$c[2]+0.001*$c[3];
	$t2=$c[5]*3600+$c[6]*60+$c[7]+0.001*$c[8];
	$T=($t1+$t2)/2;
	if ($T-$prevT>$step) {
		for ($i=$prevT+$step/2; $i<$T-$step/2; $i+=$step) {
			printf stdout "%f\n",$i;
			}
		}
	else {
#		printf stdout "%d %d %d ->%d %d %d\n",$c[0],$c[1],$c[2],$c[5],$c[6],$c[7];
#		printf stdout "%d -> %d\n",$t1,$t2;
		if ($todos>0) {
			for ($i=int($t1); $i<=int($t2); $i+=$todos) {
				printf stdout "%d.0\n",$i;
				}
			}
		else {
				printf stdout "%f\n",$T;
			}
#		exit 0;
		}
	$prevT=$T;
	}
}