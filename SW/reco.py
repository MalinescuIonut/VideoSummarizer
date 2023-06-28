# importing libraries 
import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence

# create a speech recognition object
r = sr.Recognizer()

# a function that splits the audio name into chunks
# and applies speech recognition
def get_large_audio_transcription_withoutSilence(path):
    """
    Splitting the large audio name into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio name using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio name
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_namename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_namename, format="wav")
        # recognize the chunk
        with sr.Audioname(chunk_namename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened, language="es-ES")
#                text = r.recognize_bing(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_namename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text

import os
import sys
import re
import datetime
import glob
import io

def convertMillis(millis):
    milli=float(millis)
    miliseconds=milli%1000
    seconds=(milli/1000)%60
    minutes=(milli/(1000*60))%60
    hours=(milli/(1000*60*60))%24
    return miliseconds,seconds, minutes, hours

from pathlib import Path

# a function that applies speech recognition to a folder with wave names
def get_large_audio_transcription(path):
    """
    apply speech recognition on each of these names
    """
    # recognize the name
    print("PATH: "+path)
    cont=0
    files = glob.glob(path+"/*.wav")   
    files.sort(key=os.path.getmtime)
    print(files)
    for name in files:
#    for name in os.listdir(path):
#        current = os.path.join(path, name)
        current=name
        print(current)

        x = re.split("\-", current, 3)
        print(x)
        with sr.AudioFile(current) as source:
            audio_listened = r.record(source)
        # try converting it to text
            try:
                text = r.recognize_google( audio_listened, language="es-ES")
#               text = r.recognize_bing(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                with open('subtitulos.srt', 'a') as f1:
                    miliseconds1,seconds1,minutes1, hours1=convertMillis(float(x[1])*1000)
                    miliseconds2,seconds2,minutes2, hours2=convertMillis(float(x[2])*1000)    
                    x1 = io.StringIO()
                    x1.write("%02d:%02d:%02d.%03d" % (hours1, minutes1, seconds1, miliseconds1))
                    x2 = io.StringIO()
                    x2.write("%02d:%02d:%02d.%03d" % (hours2, minutes2, seconds2, int(miliseconds2)))
                    
                    f1.write(str(cont)+os.linesep+x1.getvalue()+" --> "+x2.getvalue()+os.linesep+text+os.linesep+os.linesep)
                    cont=cont+1
    # return the text
    return

from pydub import AudioSegment
#name="TheVastOfNight2020Patterson"
#name="CabezaDePerro2006Amodeo"
#name="ManyanaSeraOtroDia1967Camino"
name=sys.argv[1]

#print("loading: "+name)
#sound = AudioSegment.from_mp3(name+".mp3")
#print("name loaded: "+name)
#sound.export(name+".wav", format="wav")
#print("name exported: "+name)
#input("Pulse")

get_large_audio_transcription("summarized"+name+"\\speech\\")
#get_large_audio_transcription(name+".wav")
input("Pulse")

