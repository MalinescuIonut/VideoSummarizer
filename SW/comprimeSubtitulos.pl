$t11=0;
$t12=0;
$ini="";
$cont=0;
while ($_=<stdin>) {
 if (/\d\d\:\d\d\:\d\d\,\d\d\d \-\-\> \d\d\:\d\d\:\d\d\,\d\d\d/)
	{
	@c=split(/[\:\,\s]/,$_);
#	print;
	$t21=$c[0]*3600+$c[1]*60+$c[2]+0.001*$c[3];
	$t22=$c[5]*3600+$c[6]*60+$c[7]+0.001*$c[8];
	$T=($t21+$t22)/2;
#	printf stdout "%d %d %d ->%d %d %d\n",$c[0],$c[1],$c[2],$c[5],$c[6],$c[7];
#	printf stdout "%d -> %d\n",$t1,$t2;
	if ($t12>0 && $t21-$t12>1)
		{
		for ($i=0; $i<$cont: $i++)
			{
			printf stdout "%02d: %d %d ->%d %d %d\n",$c[0],$c[1],$c[2],$c[5],$c[6],$c[7];
			print stdout $array[$i];
			}
		}
	else
		{
		}
	printf stdout "%f\n",$T;
#	exit 0;
	}
 elsif (/^[\s\t\n\r]+$/)
	{
	}
 else
	{
	$array[$cont]=$_;
	$cont++;
	}
}