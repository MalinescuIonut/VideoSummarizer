$cont=0;
$startFrame[0]=0;
open(my $fh, "<", $ARGV[0])
	or die "Can't open file: $!";
while ($_=<$fh>) {
    chomp;
	$endFrame[$cont]=$_;
	$cont++;
	$startFrame[$cont]=$_;
  }
close($fh)
    || warn "close failed: $!";

$numSTR=1;
while ($_=<stdin>) {
	chomp;
	if (/^$/) {
		} 
	elsif (/-->/) {
		@c=split(/[\s\:\,\.]/,$_);
		$s1=$c[0]*3600+$c[1]*60+$c[2]+$c[3]/1000;
		$s2=$c[5]*3600+$c[6]*60+$c[7]+$c[8]/1000;
		$lineStartFrame[$numSTR]=0;
		$lineEndFrame[$numSTR]=0;
		for ($i=0; $i<$cont; $i++) {
			if ($startFrame[$i]<=$s1 && $endFrame[$i]>=$s2) {
				$lineStartFrame[$numSTR]=$startFrame[$i];
				$lineEndFrame[$numSTR]=$endFrame[$i];
				last;
			}
			elsif ($startFrame[$i]>=$s1) {
				last;
				}
			}
		$lineNumber[$numSTR]=$numSTR;
		$lineStartRange[$numSTR]=sprintf ("%02d:%02d:%02d,%03d",
			int($s1/3600), int(($s1%3600)/60), int($s1%60), int(($s1-int $s1)*1000));
		$lineEndRange[$numSTR]=sprintf ("%02d:%02d:%02d,%03d",
			int($s2/3600), int(($s2%3600)/60), int($s2%60), int(($s2-int $s2)*1000));
		$lineText[$numSTR]="";
		} 
	elsif (/^\d/) {
		$numSTR=$_;
		}
	else {
		$lineText[$numSTR].=$_."   ";
		}
	}

$contLine=1;
#printf stdout "A %s FRAME %s-%s %s\n",$contLine,$lineStartFrame[$contLine],$lineEndFrame[$contLine],$lineNumber[$contLine];
#printf stdout "B %s FRAME %s-%s %s -> ",$contLine,$lineStartFrame[$contLine],$lineEndFrame[$contLine],$lineStartRange[$contLine];
printf stdout "%s\n",$contLine;
printf stdout "%s --> ",$lineStartRange[$contLine];
$line=$lineText[$contLine];
for ($i=2;$i<=$numSTR; $i++) {
	if ($lineEndFrame[$i] ne 0 && $lineStartFrame[$i] eq $lineStartFrame[$i-1] && $lineEndFrame[$i] eq $lineEndFrame[$i-1]) {
		if (length ($line)<180) {
			$line.=$lineText[$i];
			}
		else {
			printf stdout "%s\n",$lineEndRange[$i-1];
			printf stdout "%s\n\n",$line;
			$contLine++;
			printf stdout "%s\n",$contLine;
			printf stdout "%s --> ",$lineStartRange[$i];
			$line=$lineText[$i];
			}
		}
	else {
		printf stdout "%s\n",$lineEndRange[$i-1];
		printf stdout "%s\n\n",$line;
		$contLine++;
		printf stdout "%s\n",$contLine;
		printf stdout "%s --> ",$lineStartRange[$i];
		$line=$lineText[$i];
#		$contLine++;
#		printf stdout "A %s FRAME %s-%s %s\n",$contLine,$lineStartFrame[$i],$lineEndFrame[$i],$lineNumber[$i];
#		printf stdout "B %s FRAME %s-%s %s -> ",$contLine,$lineStartFrame[$contLine],$lineEndFrame[$contLine],$lineStartRange[$contLine];
#		$line=$lineText[$i];
#		printf stdout "%s\n",$lineEndRange[$i-1];
#		printf stdout "C %d FRAME %s-%s %s\n",$contLine,$lineStartFrame[$i-1],$lineEndFrame[$i-1],$line;
		}
	}
printf stdout "%s\n",$lineEndRange[$numSTR];
printf stdout "%s\n",$line;
#printf stdout "C %d FRAME %s-%s %s\n",$contLine,$lineStartFrame[$numSTR],$lineEndFrame[$numSTR],$line;
