import os
import cv2
import re
import sys
import pysrt
import math
import pyttsx3
import shutil

FFMPEG="SW\\ffmpeg"

 
def buscaSubt(subs,currtime):
  for sub in subs:
    if currtime>=(sub.start.ordinal/1000.0) and currtime<=(sub.end.ordinal/1000.0):
      print("TXT "+str(currtime)+" ("+str(sub.start.ordinal/1000)+"-"+str(sub.end.ordinal/1000)+") "+sub.text)
      return sub.text
  print("OJO DUR "+str(1)+" "+str(currtime))
  return "AAAAAAAAAA"

def TTS(texto1,filename,veloc,velocTTS):
  if len(texto1)==0:
    texto1="a"
  print("TEXTO1: "+texto1)
  texto2=texto1.replace(" ---"," a ")
  print("TEXTO2: "+texto2)
  texto3=texto2.replace(",",' <break strength="none"/>')
  texto="<speak> "+texto3.replace(".",' <break strength="weak"/>')+" </speak>"
  print("TEXTO: "+texto)
  engine = pyttsx3.init()
  engine.setProperty('voice', 'spanish') 
  engine.setProperty('rate', velocTTS)
  engine.save_to_file(texto, "dep/dep1.mp3")
#  print("TXT: "+texto+" "+filename+".mp3")
#  engine.save_to_file(texto, filename+".mp3")
  engine.runAndWait()
  os.system(FFMPEG + " -i dep/dep1.mp3 -af silenceremove=start_periods=1:start_duration=0.1:start_threshold=-80dB:detection=peak,aformat=dblp,areverse,silenceremove=start_periods=1:start_duration=0.1:start_threshold=-80dB:detection=peak,aformat=dblp,areverse -y "+filename+".mp3")
  from mutagen.mp3 import MP3
  print("MP3: "+filename+".mp3")
  audio = MP3(filename+".mp3")
  dur=audio.info.length
  return dur
  
if len(sys.argv) == 7:
  #path = sys.argv[1]+sys.argv[2]+sys.argv[3]
  path = "summarized"+sys.argv[3]+"/"+sys.argv[2]+sys.argv[3]
  pathBase = "summarized"+sys.argv[3]+"/"
  durSHOT=int(sys.argv[4])
  velocTTS=int(sys.argv[5])
  veloc=int(sys.argv[6])
#  umbralLargos=int(sys.argv[7])
#  factorLargos=int(sys.argv[8])
else:
#  print("python CreaVideo.py <relatPath> summarized4 <name> <durSHOT> <durSTR> <veloc> <umbralLargos> <factorLargos>")
  print("python CreaVideo.py <relatPath> summarized4 <name> <durSHOT> <velocTTS> <veloc> ")
  exit(1)

try: 
  shutil.rmtree('dep')
except OSError as error:
    print(error) 
try: 
  os.mkdir("dep")
except OSError as error:
    print(error) 
#filename = sys.argv[3]+".mp3"
#texto="Esto es una prueba de conversión texto habla en español."
#TTS(texto,sys.argv[3],veloc)
#input("pulsa")
subs = pysrt.open(pathBase+sys.argv[3]+'.srt')

archivos = sorted(os.listdir(path))
print(path + "Path of the files")
archivos.sort(key=lambda f: int(re.sub('\D', '', f)))
print(archivos)
input("Press any key...")
img_array = []
time_array = []
with open("dep/videos.lis", 'w') as f:
  for x in range(0, len(archivos)):
    nomArchivo = archivos[x]
    dirArchivo = path + "/" + str(nomArchivo)
    if re.search('[\d]+\.[\d]+', archivos[x]):
      currtime=float(re.search('[\d]+\.[\d]+', archivos[x]).group(0))
    else:
        currtime = float(re.search('^[\d]+', archivos[x]).group(0))
    img = cv2.imread(dirArchivo)
    height, width = img.shape[:2]
    match = re.search('SRT', nomArchivo)
    if match:
      texto=buscaSubt(subs,currtime)
      #dur=math.ceil(len(texto)/40)*durSRT
#      print(str(currtime)+" "+str(dur), file=sys.stderr)
#      print("SRT "+str(dur)+"/"+str(veloc))
      video = cv2.VideoWriter("dep/"+sys.argv[3]+"_"+str(x)+'.mp4',cv2.VideoWriter_fourcc(*'mp4v'),veloc,(width, height))
      durTTS=math.ceil(veloc*TTS(texto,"dep/"+sys.argv[3]+"_"+str(x),veloc,velocTTS))
      dur=durTTS+1
      print("DUR "+str(dur)+"/"+str(veloc))

      for i in range(dur):
#        img_array.append(img)
#        time_array.append(float(re.search('[\d]+\.[\d]+', nomArchivo).group(0)))
        video.write(img)
      video.release()
      print("MP4 ("+str(dur)+"): dep/"+sys.argv[3]+"_"+str(x)+".mp4")
      #input("dur: "+str(dur)+" durTTS: "+str(durTTS))  
    else:
      dur=durSHOT
      print("DUR "+str(currtime)+" "+str(dur), file=sys.stderr)
      video = cv2.VideoWriter("dep/"+sys.argv[3]+"_"+str(x)+'.mp4',cv2.VideoWriter_fourcc(*'mp4v'),veloc,(width, height))
      for i in range(dur):
#        img_array.append(img)
#        time_array.append(float(re.search('[\d]+\.[\d]+', nomArchivo).group(0)))
        video.write(img)
      video.release()
      print("MP4 ("+str(dur)+"): dep/"+sys.argv[3]+"_"+str(x)+".mp4")
      os.system(FFMPEG + " -f lavfi -i anullsrc=r=22050:cl=mono -t "+str(dur/veloc)+" -q:a 9 -acodec libmp3lame dep/"+sys.argv[3]+"_"+str(x)+".mp3")
      print("MP3 ("+str(dur)+"/"+str(veloc)+"): dep/"+sys.argv[3]+"-"+str(x)+".mp4")
    os.system(FFMPEG + " -i dep/"+sys.argv[3]+"_"+str(x)+".mp4 -i dep/"+sys.argv[3]+"_"+str(x)+".mp3 -c:v copy -map 0:v -map 1:a  -shortest -y dep/"+sys.argv[3]+"-"+str(x)+".mp4")
    print("-MP4: dep/"+sys.argv[3]+"-"+str(x)+".mp4")
    f.write("file '"+sys.argv[3]+"-"+str(x)+".mp4"+ "'"+'\r'+ '\n')
    #if x==4:
    #  input("pulse2")
    


#print("Video writer")
#video = cv2.VideoWriter(sys.argv[3]+'-bis.mp4', cv2.VideoWriter_fourcc(*'mp4v'), veloc, (width, height))
#print("Video writing")
#for i in range(0, len(img_array)):
#  if i%100==0:
#    print('archivo '+str(i), file=sys.stderr)
#  video.write(img_array[i])
#video.release()

os.system(FFMPEG + " -f concat -i dep/videos.lis -c copy -y SUM_"+sys.argv[3]+'.mp4')


