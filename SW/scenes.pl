$step=10000;
$prevT=0;
while ($_=<stdin>) {
	s/[\n\r]//g;
	if (/\d+/) {
		if ($prevT>0) {
			$T=($_+$prevT)/2;
#			if ($_-$prevT>$step) {
#				for ($i=$prevT+$step/2; $i<$_-$step/2; $i+=$step) {
#					printf stdout "%f\n",$i;
#					}
#				}
#			else {
				printf stdout "%f\n",$T;
#				}
			}
		else {
			printf stdout "%f\n",$_;
			}
		$prevT=$_;
		}
	}
	printf stdout "%f\n",$prevT;
