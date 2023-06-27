$cont=0;
while ($_=<stdin>) {
  if (/-->/) {
	printf "%d\n",$cont;
	$cont++;
	}
  print stdout;
  }

