$/ = "\r";
$cont=0;
while ($_=<stdin>) {
  s/[\n\r]//;chomp;
  if (/-->/) {
	s/\./,/g;
	print stdout;
	printf stdout "\n";
	}
  elsif (/^\d/) {
	if ($cont>0) {
		printf stdout "\n";
	}
	print stdout;
	printf stdout "\n";
	}
  elsif (/[a-zA-Z0-9]/) {
	print stdout;
	printf stdout "\n";
	}
  else {
	}
  $cont++;
  }

