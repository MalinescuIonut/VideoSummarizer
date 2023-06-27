#perl "C:\Users\gth\Google Drive\SW\extraeShots.pl" directorio < index.html
$dir=$ARGV[0];
printf stdout "set \"FOLDERSW=C:\\Users\\%%USER%%\\Google Drive\\SW\"\n";
while ($_=<stdin>) {
chop;
$flag=0;
if (/srcset/ && /lets\-review\-5\-w\-number/) {
  $flag=1;
  s/^(.*?)href\=\"(.*?)\"(.*?)srcset\=\"(.*?)\"(.*?)lets\-review\-5\-w\-number\"\>(.*?)\<.*$/$6 $4 $2/g;
}
if (/srcset/ && /lets\-review\-ext\-5/) {
  $flag=1;
  s/^(.*?)href\=\"(.*?)\"(.*?)srcset\=\"(.*?)\"(.*?)lets\-review\-ext\-5\"\>(.*?)\<.*$/$6 $4 $2/g;
}
if ($flag>0) {
  @c=split(/ /,$_);
  @c1=split(/\//,$c[$#c]);
  $value=$c[0];
  $film=$c1[$#c1];
  for ($i=0; $i<$#c; $i++) {
	 $_=$c[$i];
	 if (/\./) {
		@c2=split(/\//,$c[$i]);
		$shot=$c1[$#c1];
       printf stdout "::value %d %s\n\"%%FOLDERSW%%\\bash-win32\\wget64.exe\" --no-check-certificate -O %s\\%s %s\n",$value,$film,$dir,$c2[$#c2],$c[$i];
#       printf stdout "#value %d %s\nwget %s\n",$value,$film,$c[$i];
	   }
	 }
  printf stdout "\n";
  } 
}
