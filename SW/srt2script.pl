$NAME=$ARGV[0];
$EXT=$ARGV[1];
$FICH=$NAME.".".$EXT;
printf stdout "mkdir summarized%s\\speech\n",$NAME;
$step=15;
$flag=0;
$iniAnt=0;
$finAnt=0;
$msgAnt="";
while ($_=<stdin>) {
  if (/-->/) {
    chomp;
	@c=split(/[\s\:\,]/,$_);
	$ini=$c[0]*3600+$c[1]*60+$c[2]+$c[3]/1000;
	$fin=$c[5]*3600+$c[6]*60+$c[7]+$c[8]/1000;
	$_=<stdin>;
	if ($flag>0){
		$ini=$iniAnt;
		$_=$_.$msgAnt;
	}
	$s1=$ini;
	$s2=$ini+$step;
	for (; $s2<=$fin; $s1=$s2-1,$s2+=$step)  #split long chunks
		{
			$ini2=$s1-1;
			if ($ini2<0) {
				$ini2=0;
				}
			$dur=$s2-$s1+2;
		if (/^male/) {
			printf stdout "ffmpeg -i %s -ac 2 -ss %f -t %f summarized%s\\speech\\%s-%f-%f-male.wav\n", $FICH, $ini2,$dur,$NAME,$NAME,$s2-$step,$s2;
			}
		elsif (/^female/) {
			printf stdout "ffmpeg -i %s -ac 2 -ss %f -t %f summarized%s\\speech\\%s-%f-%f-female.wav\n", $FICH, $ini2,$dur,$NAME,$NAME,$s2-$step,$s2;
			}
		elsif (/^music/) {
			printf stdout "ffmpeg -i %s -ac 2 -ss %f -t %f summarized%s\\speech\\%s-%f-%f-music.wav\n", $FICH, $ini2,$dur,$NAME,$NAME,$s2-$step,$s2;
			}
		elsif (/^noise/) {
			printf stdout "ffmpeg -i %s -ac 2 -ss %f -t %f summarized%s\\speech\\%s-%f-%f-noise.wav\n", $FICH, $ini2,$dur,$NAME,$NAME,$s2-$step,$s2;
			}
		else {
			printf stdout "ffmpeg -i %s -ac 2 -ss %f -t %f summarized%s\\speech\\%s-%f-%f-else.wav\n", $FICH, $ini2,$dur,$NAME,$NAME,$s2-$step,$s2;
			}
		}
	$s1=$s2-$step;
	$ini2=$s1-1;
	$s2=$fin;
	$dur=$s2-$s1+1;
	if ($ini2<0) {
		$ini2=0;
		}
	if ($dur<10) {
		$flag=1;
		$iniAnt=$s1;
		$finAnt=$s2;
		$msgAnt=$_;
	}
	else {
		$flag=0;
	if (/^male/) {
		printf stdout "ffmpeg -i %s -ac 2 -ss %f -t %f summarized%s\\speech\\%s-%f-%f-male.wav\n", $FICH, $ini2,$dur,$NAME,$NAME,$s1,$s2;
		}
	elsif (/^female/) {
		printf stdout "ffmpeg -i %s -ac 2 -ss %f -t %f summarized%s\\speech\\%s-%f-%f-female.wav\n", $FICH, $ini2,$dur,$NAME,$NAME,$s1,$s2;
		}
	elsif (/^music/) {
		printf stdout "ffmpeg -i %s -ac 2 -ss %f -t %f summarized%s\\speech\\%s-%f-%f-music.wav\n", $FICH, $ini2,$dur,$NAME,$NAME,$s1,$s2;
		}
	elsif (/^noise/) {
		printf stdout "ffmpeg -i %s -ac 2 -ss %f -t %f summarized%s\\speech\\%s-%f-%f-noise.wav\n", $FICH, $ini2,$dur,$NAME,$NAME,$s1,$s2;
		}
	else {
		printf stdout "ffmpeg -i %s -ac 2 -ss %f -t %f summarized%s\\speech\\%s-%f-%f-else.wav\n", $FICH, $ini2,$dur,$NAME,$NAME,$s1,$s2;
		}
	}
	
	}
  }

