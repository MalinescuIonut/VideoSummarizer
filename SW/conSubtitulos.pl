%conSubtitulos=('0'=> '0');
#printf stdout ":: %%conSubtitulos=('0'=> '0'\n";
open(my $fh, "<", $ARGV[0])
	or die "Can't open file: $!";
while ($_=<$fh>) {
    chomp;
	@c=split(/\./,$_);
#	printf stdout ":: '%d' => '1'\n",$c[0];
	$conSubtitulos{$c[0]}='1';
  }
close($fh)
    || warn "close failed: $!";
#printf stdout ":: );\n";

while ($_=<stdin>) {
    chomp;
	@c=split(/\./,$_);
	if ($conSubtitulos{$c[0]} ne '1') {
		printf stdout "copy %s\\%d.*.jpg %s\\ \n",$ARGV[1],$c[0],$ARGV[2];
	}
	else{
#		printf stdout ":: copy %s\\%d*.jpg %s\\ \n",$ARGV[1],$c[0],$ARGV[2];
	}
  }

