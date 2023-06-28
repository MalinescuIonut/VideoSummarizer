import os
import shutil
import re
from time import time

start_time_total = time() #Comienza a contar el timepo de programa

## Parámetros del programa

NAME=""
EXTENS=""

TRACKSUBT=0
TRACKAUDIO=0
SCENETHRESHOLD=0.4
SUBTITLETHRESHOLD=0.2


swDirectory=""
workingDir=""
FFMPEG="ffmpeg"
FFPROBE="ffprobe"
PERL="perl"
REDUNDANCY=0


copyResolution=0 #original=0 
samplingRate=10 # seconds


## Lectura de fichero de configuración

with open("summarizeConfiguration.txt",mode='r',encoding='utf8', newline='\r\n') as input:
   data=[]
   lineas=input.read().splitlines()
   for line in lineas:
      data.append(line.split("=")[1])
#   data.append(line.split("=")[1].rsplit()[0])
   NAME=data[0]
   EXTENS=data[1]
   TRACKSUBT=int(data[2])
   TRACKAUDIO=int(data[3])
   SCENETHRESHOLD=float(data[4])
   SUBTITLETHRESHOLD=float(data[5])

   copyResolution=int(data[6])
   samplingRate=int(data[7])
   REDUNDANCY=int(data[8])


   swDirectory=data[9]
   workingDir=data[10]
   FFMPEG=data[11]
   FFPROBE=data[12]
   FFPROBE=data[12]
   PERL=data[13]
   





FILE=os.path.join(workingDir, NAME + "." + EXTENS)

os.chdir(workingDir)

f = open ('summarize.log','w') #Fichero de registro de tiempos

##Creación de directorio principal y subdirectorios

folder=os.path.join(workingDir, "summarized"+NAME) # Directorio principal
folder0=os.path.join(folder, "summarized0"+NAME)   # Subdirectorio keyframes
folder1=os.path.join(folder, "summarized1"+NAME)   # Subdirectorio subtítulos
folder2=os.path.join(folder, "summarized2"+NAME)   # Subdirectorio muestreo
folder3=os.path.join(folder, "summarized3"+NAME)   # Subdirectorio escenas
folder4=os.path.join(folder, "summarized4"+NAME)   # Subdirectorio final

#Si no existe. se crea
print("Folder: "+folder)
if not os.path.exists(folder):
   os.mkdir(folder)
if not os.path.exists(folder0):
   os.mkdir(folder0)
if not os.path.exists(folder1):
   os.mkdir(folder1)
if not os.path.exists(folder2):
   os.mkdir(folder2)
if not os.path.exists(folder3):
   os.mkdir(folder3)
if not os.path.exists(folder4):
   os.mkdir(folder4)

# Copia de seguridad de srt

srtOriginal = os.path.join(workingDir,NAME+".srt") 
srtCopia= os.path.join(workingDir,NAME+"-ORIG.srt")

# Si el srt está vacío, intenta extraerlo del archivo de vídeo

if os.stat(srtOriginal).st_size != 0:
    shutil.copy2(srtOriginal, srtCopia)
else:
  os.system(FFMPEG + ' -i ' + FILE + ' -map 0:s:' + str(TRACKSUBT) +' -y '+ os.path.join(workingDir,NAME+'.srt'))

# Duración de la película en segundos

command=FFPROBE + ' -i '+FILE+' -show_entries format=duration -v quiet -of csv="p=0"'
result=os.popen(command).read()
duration=int(float(result.rstrip()))+1

# os.system(FFMPEG + " -i " + FILE + " -y " + os.path.join(folder,NAME+".mp3"))

# os.system(FFMPEG + " -i " + FILE + ' -af silencedetect=n=-50dB:d=0.5,ametadata=print:file=' + NAME +'_SILENCE.dep -map 0:a:'+str(TRACKAUDIO)+" -y " + NAME + "_SILENCE.mp3")
# os.remove(NAME+ "_SILENCE.mp3")

# pattern_silence = "(?<=silence_start=)[0-9.]*|(?<=silence_end=)[0-9.]*"

# with open(os.path.join(workingDir,NAME+'_SILENCE.dep')) as input:
#     with open(os.path.join(folder,NAME+'_SILENCE.lis'),"w") as output:
#         data=input.read()
#         words=re.findall(pattern_silence,data)
        
#         for line in words:
#             output.write(line+"\n")


# os.system(PERL+" "+ os.path.join(swDirectory,"lis2srt.pl")+" 2 SILENCE < "+os.path.join(folder,NAME+"_SILENCE.lis") + " > " + os.path.join(folder,NAME+"_SILENCE.srt"))




# os.system(FFMPEG + " -i " + FILE + ' -vf blackdetect=d=0.1:pix_th=.1,metadata=print:file=' + NAME +'_BLACK.dep -y ' + NAME + "_BLACK."+EXTENS)

# pattern_black = "(?<=black_start=)[0-9.]*|(?<=black_end=)[0-9.]*"

# with open(os.path.join(workingDir,NAME+'_BLACK.dep')) as input:
#     with open(os.path.join(folder,NAME+'_BLACK.lis'),"w") as output:
#         data=input.read()
#         words=re.findall(pattern_black,data)
        
#         for line in words:
#             output.write(line+"\n")


## Llamada de FFmpeg para detectar cambios de secuencia
start_time = time()

command=FFMPEG + " -i " + FILE + " -filter_complex \"select=gt'(scene,"+str(SUBTITLETHRESHOLD)+")',metadata=print:file=" + NAME +'sequenceORIG.dep\" -vsync vfr -y dep'+NAME+"."+EXTENS
print("Command: "+command)
os.system(command)

elapsed_time = time() - start_time 

f.write("Tiempo detector de secuencias: %.2f segundos.\n" % elapsed_time)

pattern_sequence = "(?<=pts_time:)[0-9.]*"  #Patrón del dato

## Recorrido del fichero buscando el patrón

with open(os.path.join(workingDir,NAME+'sequenceORIG.dep')) as input:   
    with open(os.path.join(folder,NAME+'sequenceORIG.lis'),"w") as output:
        data=input.read()  
        words=re.findall(pattern_sequence,data)
        
        for line in words:
            output.write(line+"\n")



start_time = time()

##Inicio del algoritmo de cambios de escena##

## Llamada de FFmpeg para detectar cambios de escena
command=FFMPEG +" -i " + FILE + " -filter_complex \"select=gt'(scene,"+str(SCENETHRESHOLD)+")',metadata=print:file=" + NAME +'scenesORIG.dep\" -vsync vfr -y dep'+NAME+"."+EXTENS
print("Command: "+command)
os.system(command)

elapsed_time = time() - start_time

f.write("Tiempo detector de escenas: %.2f segundos.\n" % elapsed_time)

pattern_scene = "(?<=pts_time:)[0-9.]*"  #Patrón del dato

## Recorrido del fichero buscando el patrón

with open(os.path.join(workingDir,NAME+'scenesORIG.dep')) as input:
    with open(os.path.join(folder,NAME+'scenesORIG.lis'),"w") as output:
        data=input.read()
        words=re.findall(pattern_scene,data)
        start_time = time()
        
        for line in words:
        ## Llamada de FFmpeg para extraer fotogramas de cambios de escena
            command=FFMPEG + " -ss " + line + " -i "+ FILE + " -vframes 1 -vsync vfr -y " + os.path.join(folder3,line + "-" + NAME + "-SHOT.jpg")
            print("Command: "+command)
            os.system(command)
         
            output.write(line+"\n")
        elapsed_time = time() - start_time
        f.write("Tiempo bucle 3: %.2f segundos.\n" % elapsed_time)


## Compactador de subtítulos
command="echo " + str(duration) + ' >> ' + os.path.join(folder, NAME + "scenesORIG.lis")
print("Command: " + command)
os.system(command)
command=PERL+' ' + os.path.join(swDirectory, "inScene.pl") + ' ' + os.path.join(folder, NAME + "scenesORIG.lis") + ' < ' + os.path.join(workingDir, NAME + ".srt") + ' > ' +  os.path.join(folder, NAME + ".srt.dep" )
print("Command: " + command)
os.system(command)
command=PERL+' '+ os.path.join(swDirectory, "subtitulos.pl ") + ' 100000 0 <' + os.path.join(folder, NAME + ".srt.dep") + ' >' + os.path.join(folder, NAME + "srt.lis")
print("Command: " + command)
os.system(command)
shutil.copy2(os.path.join(folder, NAME + ".srt.dep"),os.path.join(folder, NAME + ".srt"))




FILE2=""

start_time = time()

##Vídeo con subtitulos compactados en pantalla

os.chdir(folder)

if copyResolution==0:
   command=FFMPEG + " -i " + FILE + " -vcodec libx264 -acodec aac -map 0:a:" + str(TRACKAUDIO) + " -map 0:v:0 -vf subtitles=" + NAME +'.srt -y '+ os.path.join(folder,NAME+"ORIG.mp4")
   print("Command: " + command)
   os.system(command)
   FILE2=os.path.join(folder,NAME+"ORIG.mp4")
else:
   command=FFMPEG + " -i " + FILE + " -vcodec libx264 -acodec aac -map 0:a:" + str(TRACKAUDIO) + " -map 0:v:0 -vf subtitles=" + NAME +".srt,scale="+str(copyResolution)+':-2 -y '+ os.path.join(folder,NAME+"-ORIG.mp4")
   print("Command: " + command)
   os.system(command)
   FILE2=os.path.join(folder,NAME+"-ORIG.mp4")

os.chdir(workingDir)

elapsed_time = time() - start_time
f.write("Tiempo copia mp4: %.2f segundos.\n" % elapsed_time)

start_time = time()

## Inicio algoritmo keyframes ## 

## Llamada de FFmpeg para detectar keyframes
command=FFMPEG + " -i " + FILE + " -filter_complex \"select=eq'(pict_type,PICT_TYPE_I)'\" -vsync vfr -y " +NAME+"dep."+EXTENS+" 2> "+ os.path.join(folder, NAME + "iframes"+EXTENS+".dep")
print("Command: "+command)
os.system(command)

pattern_iframes= "(?<=time=)[0-9]*\:[0-9]*\:[0-9.]*"  # Patrón del dato

## Recorrido del fichero buscando el patrón
print(folder, NAME+"iframes"+EXTENS+".dep")
with open(os.path.join(folder, NAME + "iframes"+EXTENS+".dep")) as input:
   with open(os.path.join(folder, NAME + "iframes" + EXTENS + ".lis"),"w") as output:
      data=input.read()
      words=re.findall(pattern_iframes,data)
        
      for line in words:
         timepts=line.split(":")
         timesec=format ( int ( timepts[0])*3600 + int(timepts[1])*60 + float(timepts[2]) , ".2f" )
         
         ## Llamada de FFmpeg para extraer keyframes
         command=FFMPEG + " -ss " + timesec + " -i "+ FILE + " -vf \"drawtext=fontsize=10:fontcolor=yellow:box=1:boxcolor=black:x=(W-tw)/4:y=H-th-2: text=' TIME=" + timesec + "'\" -vframes 1 -vsync vfr -y \"" + os.path.join(folder0,timesec + "-" + NAME + "-IFRAME.jpg\"")
         print("Command: " + command)
         os.system(command)
        
         output.write(timesec+"\n")

elapsed_time = time() - start_time

f.write("Tiempo bucle 0: %.2f segundos.\n" % elapsed_time)

start_time = time()

##Inicio del algoritmo de subtítulos

##Recorrido de fichero marcas de tiempo
with open(os.path.join(folder, NAME + "srt.lis")) as input:

   for line in input:
      line2=line.rstrip()

      ## Llamada de FFmpeg para extraer fotogramas de subtítulo
      command=FFMPEG + " -ss " + line2 + " -i "+ FILE2 + " -vf \"drawtext=fontsize=10:fontcolor=yellow:box=1:boxcolor=black:x=(W-tw)/4:y=H-th-2: text=' TIME=" + line2 + "'\" -vframes 1 -vsync vfr -y \"" + os.path.join(folder1,line2 + "-" + NAME + "-SRT.jpg\"")
      print("Command: "+command)
      os.system(command)
        
  
elapsed_time = time() - start_time
f.write("Tiempo bucle 1: %.2f segundos.\n" % elapsed_time)

start_time = time()

## Inicio del algoritmo de muestreo ##

for second in range(1,duration,samplingRate): #Desde 1 hasta el final, cada samplingRate

   #Llamada a FFmpeg para extracción de fototgramas de muestreo

   os.system(FFMPEG + " -ss " + str(second) + " -i "+ FILE + " -vf \"drawtext=fontsize=10:fontcolor=yellow:box=1:boxcolor=black:x=(W-tw)/4:y=H-th-2: text=' TIME=" + str(second)  + "'\" -vframes 1 -vsync vfr -y \"" + os.path.join(folder2,str(second) + ".0-" + NAME + "-TIME.jpg\""))


elapsed_time = time() - start_time
f.write("Tiempo bucle 2: %.2f segundos.\n" % elapsed_time)

start_time = time()

## Inicio de algoritmo final ##

# Guardado de imagenes en listas, ordenadas
imgs0 = os.listdir(folder0)                                   # Keyframes
imgs0 = sorted(imgs0, key=lambda x: float(x.split("-")[0]))
imgs1 = os.listdir(folder1)                                   # Subtítulos
imgs1 = sorted(imgs1, key=lambda x: float(x.split("-")[0]))
imgs2 = os.listdir(folder2)                                   # Escenas
imgs2 = sorted(imgs2, key=lambda x: float(x.split("-")[0]))
imgs3 = os.listdir(folder3)                                   # Muestreo
imgs3 = sorted(imgs3, key=lambda x: float(x.split("-")[0]))

pattern_subtitles= "[0-9]*\:[0-9]*\:[0-9.]*" #Patrón fichero subtítulos

usedSecondsList=[]   #Lista segundos utilizados

subtitleInit=1 #Flag dato inicio/final
secondInit=0   #Segundo del dato inicio de subtítulo
secondFinish=0 #Segundo del dato final de subtítulo

##Recorrido de fichero de subtítulos

with open(os.path.join(folder, NAME +".srt"), encoding="utf8" ) as input:
    data=input.read()
    words=re.findall(pattern_subtitles,data)

    
   
    for line in words:
        
      
        timesub=line.split(":")
        
        timesec=int ( timesub[0])*3600 + int(timesub[1])*60 + float(timesub[2]) # HH:MM:SS -> Segundos


        if(subtitleInit==1):       # Si es inicio 
            secondInit=timesec
            subtitleInit=0
        else:                   # Si es final
            secondFinish=timesec
            subtitleInit=1

            for second in range (int(secondInit),int(secondFinish)+1): # Desde incio hasta el final, añado los segundos a la lista
                usedSecondsList.append(second)
for line in usedSecondsList:
    print(line)


for image_file in imgs1:

   # Copia de fotogramas de subtítulos a conjnto final

   shutil.copy2(os.path.join(folder1,image_file), os.path.join(folder4,image_file))



for image_file in imgs3:
   if not (int(image_file.split("-")[0].split(".")[0]) in usedSecondsList): #Si el segundo no ha sido extraído
      #Añado el segundo a la lista
      usedSecondsList.append(int(image_file.split("-")[0].split(".")[0]))
      # Copia el fotograma de subtítulos a conjunto final
      shutil.copy2(os.path.join(folder3,image_file), os.path.join(folder4,image_file))


for image_file in imgs0:
    print(int(image_file.split("-")[0].split(".")[0]))
    usedSecond=0
    for seconds in range(REDUNDANCY*(-1),REDUNDANCY+1):
        
        if ((int(image_file.split("-")[0].split(".")[0]) + seconds) in usedSecondsList): #Si es un fotograma redundante
            usedSecond=1

    if (usedSecond==0):                                              #Si no es un fotograma redundante    
        #Añado el segundo a la lista
        usedSecondsList.append(int(image_file.split("-")[0].split(".")[0]))
        # Copia el keyframe a conjunto final
        shutil.copy2(os.path.join(folder0,image_file), os.path.join(folder4,image_file))   

for image_file in imgs2:
    usedSecond=0
    for seconds in range(REDUNDANCY*(-1),REDUNDANCY+1):


        if ((int(image_file.split("-")[0].split(".")[0]) + seconds) in usedSecondsList): #Si el segundo no ha sido extraído
            usedSecond=1

    if (usedSecond==0):  
        #Añado el segundo a la lista
        usedSecondsList.append(int(image_file.split("-")[0].split(".")[0]))
        # Copia de fotograma de muestreo a conjunto final
        shutil.copy2(os.path.join(folder2,image_file), os.path.join(folder4,image_file))
      
      

elapsed_time = time() - start_time
f.write("Tiempo bucle 4: %.2f segundos.\n" % elapsed_time)

tiempo_programa = time() - start_time_total
f.write("Tiempo total programa: %.2f segundos.\n" % tiempo_programa)

f.close()

print("Summaryze completed")

f = open ('summarize.log','r')
mensaje = f.read()
print(mensaje)
f.close()



# -------------------------------------


import os
import cv2
import re
import sys
import pysrt
import math
import pyttsx3
import shutil

FFMPEG = "SW\\ffmpeg"


def buscaSubt(subs, currtime):
    for sub in subs:
        if currtime >= (sub.start.ordinal / 1000.0) and currtime <= (sub.end.ordinal / 1000.0):
            print("TXT " + str(currtime) + " (" + str(sub.start.ordinal / 1000) + "-" + str(
                sub.end.ordinal / 1000) + ") " + sub.text)
            return sub.text
    print("OJO DUR " + str(1) + " " + str(currtime))
    return "AAAAAAAAAA"


def TTS(texto1, filename, veloc, velocTTS):
    if len(texto1) == 0:
        texto1 = "a"
    print("TEXTO1: " + texto1)
    texto2 = texto1.replace(" ---", " a ")
    print("TEXTO2: " + texto2)
    texto3 = texto2.replace(",", ' <break strength="none"/>')
    texto = "<speak> " + texto3.replace(".", ' <break strength="weak"/>') + " </speak>"
    print("TEXTO: " + texto)
    engine = pyttsx3.init()
    engine.setProperty('voice', 'spanish')
    engine.setProperty('rate', velocTTS)
    engine.save_to_file(texto, "dep/dep1.mp3")
    #  print("TXT: "+texto+" "+filename+".mp3")
    #  engine.save_to_file(texto, filename+".mp3")
    engine.runAndWait()
    os.system(
        FFMPEG + " -i dep/dep1.mp3 -af silenceremove=start_periods=1:start_duration=0.1:start_threshold=-80dB:detection=peak,aformat=dblp,areverse,silenceremove=start_periods=1:start_duration=0.1:start_threshold=-80dB:detection=peak,aformat=dblp,areverse -y " + filename + ".mp3")
    from mutagen.mp3 import MP3
    print("MP3: " + filename + ".mp3")
    audio = MP3(filename + ".mp3")
    dur = audio.info.length
    return dur


if len(sys.argv) == 7:
    # path = sys.argv[1]+sys.argv[2]+sys.argv[3]
    path = "summarized" + sys.argv[3] + "/" + sys.argv[2] + sys.argv[3]
    pathBase = "summarized" + sys.argv[3] + "/"
    durSHOT = int(sys.argv[4])
    velocTTS = int(sys.argv[5])
    veloc = int(sys.argv[6])
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
# filename = sys.argv[3]+".mp3"
# texto="Esto es una prueba de conversión texto habla en español."
# TTS(texto,sys.argv[3],veloc)
# input("pulsa")
subs = pysrt.open(pathBase + sys.argv[3] + '.srt')

archivos = sorted(os.listdir(path), key=lambda f: float(re.search(r"(\d+\.\d+)", f).group(1)))
print(path + "Path of the files")
# archivos.sort(key=lambda f: int(re.sub('\D', '', f)))
print(archivos)
# input("Press any key...")
img_array = []
time_array = []
with open("dep/videos.lis", 'w') as f:
    for x in range(0, len(archivos)):
        nomArchivo = archivos[x]
        dirArchivo = path + "/" + str(nomArchivo)
        if re.search('[\d]+\.[\d]+', archivos[x]):
            currtime = float(re.search('[\d]+\.[\d]+', archivos[x]).group(0))
        else:
            currtime = float(re.search('^[\d]+', archivos[x]).group(0))
        img = cv2.imread(dirArchivo)
        height, width = img.shape[:2]
        match = re.search('SRT', nomArchivo)
        if match:
            texto = buscaSubt(subs, currtime)
            # dur=math.ceil(len(texto)/40)*durSRT
            #      print(str(currtime)+" "+str(dur), file=sys.stderr)
            #      print("SRT "+str(dur)+"/"+str(veloc))
            video = cv2.VideoWriter("dep/" + sys.argv[3] + "_" + str(x) + '.mp4', cv2.VideoWriter_fourcc(*'mp4v'),
                                    veloc, (width, height))
            durTTS = math.ceil(veloc * TTS(texto, "dep/" + sys.argv[3] + "_" + str(x), veloc, velocTTS))
            dur = durTTS + 1
            print("DUR " + str(dur) + "/" + str(veloc))

            for i in range(dur):
                #        img_array.append(img)
                #        time_array.append(float(re.search('[\d]+\.[\d]+', nomArchivo).group(0)))
                video.write(img)
            video.release()
            print("MP4 (" + str(dur) + "): dep/" + sys.argv[3] + "_" + str(x) + ".mp4")
            # input("dur: "+str(dur)+" durTTS: "+str(durTTS))
        else:
            dur = durSHOT
            print("DUR " + str(currtime) + " " + str(dur), file=sys.stderr)
            video = cv2.VideoWriter("dep/" + sys.argv[3] + "_" + str(x) + '.mp4', cv2.VideoWriter_fourcc(*'mp4v'),
                                    veloc, (width, height))
            for i in range(dur):
                #        img_array.append(img)
                #        time_array.append(float(re.search('[\d]+\.[\d]+', nomArchivo).group(0)))
                video.write(img)
            video.release()
            print("MP4 (" + str(dur) + "): dep/" + sys.argv[3] + "_" + str(x) + ".mp4")
            os.system(FFMPEG + " -f lavfi -i anullsrc=r=22050:cl=mono -t " + str(
                dur / veloc) + " -q:a 9 -acodec libmp3lame dep/" + sys.argv[3] + "_" + str(x) + ".mp3")
            print("MP3 (" + str(dur) + "/" + str(veloc) + "): dep/" + sys.argv[3] + "-" + str(x) + ".mp4")
        os.system(FFMPEG + " -i dep/" + sys.argv[3] + "_" + str(x) + ".mp4 -i dep/" + sys.argv[3] + "_" + str(
            x) + ".mp3 -c:v copy -map 0:v -map 1:a  -shortest -y dep/" + sys.argv[3] + "-" + str(x) + ".mp4")
        print("-MP4: dep/" + sys.argv[3] + "-" + str(x) + ".mp4")
        f.write("file '" + sys.argv[3] + "-" + str(x) + ".mp4" + "'" + '\r' + '\n')
        # if x==4:
        #  input("pulse2")

# print("Video writer")
# video = cv2.VideoWriter(sys.argv[3]+'-bis.mp4', cv2.VideoWriter_fourcc(*'mp4v'), veloc, (width, height))
# print("Video writing")
# for i in range(0, len(img_array)):
#  if i%100==0:
#    print('archivo '+str(i), file=sys.stderr)
#  video.write(img_array[i])
# video.release()

os.system(FFMPEG + " -f concat -i dep/videos.lis -c copy -y SUM_" + sys.argv[3] + '.mp4')


# Sound Diarization ----------------------------------------------------

def millisec(timeStr):
  spl = timeStr.split(":")
  s = (int)((int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2]))* 1000)
  return s

def DIARIZA(fich,name):
  from pydub import AudioSegment
  import re
  t1 = 0 * 1000 # works in milliseconds
  t2 = 20 * 60 * 1000
  newAudio = AudioSegment.from_wav(fich)
  a = newAudio[t1:t2]
  a.export("audio.wav", format="wav")
  from pyannote.audio import Pipeline
  pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1",use_auth_token="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")
  DEMO_FILE = {"uri": "blabal", "audio": fich}
  dz = pipeline(DEMO_FILE)
  print(*list(dz.itertracks(yield_label = True))[:10], sep="\n")
  with open("diarization"+name+".txt", "w") as text_file:
      text_file.write(str(dz))
  spacermilli = 10
  spacer = AudioSegment.silent(duration=spacermilli)
  dz = open("diarization"+name+".txt").read().splitlines()
  dzList = []
  for l in dz:
    start, end =  tuple(re.findall("[0-9]+:[0-9]+:[0-9]+\.[0-9]+",string=l))
    start = millisec(start) - spacermilli
    end = millisec(end)  - spacermilli
    lex = not re.findall("SPEAKER_01", string=l)
    dzList.append([start, end, lex])
  print(*dzList[:10], sep='\n')
#  sounds = spacer
#  segments = []

#  dz = open("diarization"+name+".txt").read().splitlines()
#  for l in dz:
#    start, end = tuple(re.findall("[0-9]+:[0-9]+:[0-9]+\.[0-9]+",string=l))
#    start = int(millisec(start)) #milliseconds
#    end = int(millisec(end))  #milliseconds

#    segments.append(len(sounds))
#    sounds = sounds.append(newAudio[start:end], crossfade=0)
#    sounds = sounds.append(spacer, crossfade=0)
#  sounds.export("dz.wav", format="wav") #Exports to a wav file in thecurrent path.

#  print(segments[:8])
  return

