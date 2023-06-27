import pysrt
starts=[]
ends=[]
# Loading the Subtitle
def srtTime():
	subs = pysrt.open('file.srt.old')

	for i in range(len(subs)):
	#  print(i);
	  sub = subs[i]
	# Subtitle text
	  text = sub.text
	  text_without_tags = sub.text_without_tags

	# Start and End time
	  start = sub.start.to_time()
	  end = sub.end.to_time()
	  starts.append(start);
	  ends.append(end);
	#  subs[i].text="";
	# Removing line and saving
	#  del subs[j]

	print("starts=[ ",end="")
	for i in range(len(subs)):
	  print("'",starts[i],"', ",sep='',end="");  
	print("'00:00:00.000000']")
	print("ends=[ ",end="")
	for i in range(len(subs)):
	  print("'",ends[i],"', ",sep='',end="");  
	print("'00:00:00.000000']")
	#subs.save('file.srt.tpos')

	from datetime import datetime
	tpo = datetime.strptime('12:34:56.789012',"%H:%M:%S.%f")
	#print(tpo)

srtTime()

import sys
sys.path.append("C:/Users/gth/Documents/aMule Downloads")
from fileTpos import starts,ends
