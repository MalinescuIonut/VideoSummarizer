$cont=0;
while ($_=<stdin>) {
  if (/-->/) {
	printf "%d\n",$cont;
	print stdout;
	$cont++;
	}
  elsif (/^\d/) {
	$cont=$cont;
  }
  else {
	print stdout;
  }
}
