use utf8;
$\='\n';
while ($_=<stdin>) {
  s/\r//g;
  printf stdout $_;
#  printf stdout "\r\n";
}