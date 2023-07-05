import re
import subprocess
import os

import librosa
import numpy as np
import soundfile as sf
from pydub import AudioSegment
from pydub.playback import play
import ffmpy


def name(file_path):
    # substract file_name from file_path:
    file_name = re.findall(r'(\w+\.mkv)', file_path)[0]
    return file_name

def speed(file_path, speed_factor):

    file_name = name(file_path)

    # creating a .mp4 copy of the file
    subprocess.run(['ffmpeg', '-i', file_name, '-codec', 'copy', 'copy.mp4'])

    # separate mp3 and mp4 - both must be accelerated
    subprocess.run(['ffmpeg', '-i', 'copy.mp4', 'audio.mp3'])
    subprocess.run(['ffmpeg', '-i', 'copy.mp4', '-c:v', 'copy', '-an', 'video.mp4'])

    # 1. Video part -> apply video filter -> speed set according to the speed_factor
    subprocess.run(['ffmpeg', '-i', 'video.mp4', '-filter:v', f'setpts={speed_factor}*PTS', 'temp.mp4'])

    # trim the obtained video -> its duration = old_duration * speed_factor
    old_duration = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1',
         'copy.mp4'], capture_output=True, text=True)
    old_duration = float(old_duration.stdout.strip())
    speed_f = float(speed_factor)
    new_duration = old_duration * speed_f
    subprocess.run(['ffmpeg', '-y', '-i', 'temp.mp4', '-to', str(new_duration), '-c', 'copy', 'final.mp4'])

    # 2. Audio part
    audio = AudioSegment.from_file("audio.mp3")
    subprocess.run(['ffmpeg', '-i', 'audio.mp3', '-af', f'atempo={1/speed_f}', 'final.mp3'])

    #3. Combine audio & video
    subprocess.run(['ffmpeg', '-i', 'final.mp4', '-i', 'final.mp3', '-c:v', 'copy', '-c:a', 'aac', 'finalRESULT.mkv'])

    os.remove('copy.mp4')
    os.remove('temp.mp4')
    os.remove('audio.mp3')
    os.remove('video.mp4')
    os.remove('final.mp4')
    os.remove('final.mp3')

    return



#configuration file usage
with open("configurationSpeed.txt", 'r', encoding='utf8', newline='\r\n') as input:
    data = []
    lines = input.read().splitlines()
    for line in lines:
        data.append(line.split("=")[1])
    file_path = data[0]
    choice = data[1]
    speed_factor = float(data[2])
    length = float(data[3])

if choice == "speed":
    if float(speed_factor) == 0.0:
        print("Invalid speed factor!")
    speed(file_path, speed_factor)
    #combine_audiovideo('final.mp4', 'final.mp3', 'finalRESULT.mp4')

elif choice == "length":
    if float(length) == 0.0:
        print("Invalid length!")
    length = float(length)
    length = length*60 + 1
    old_duration = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1',
         name(file_path)], capture_output=True, text=True)
    old_duration = float(old_duration.stdout.strip())
    speed_factor = length/old_duration
    speed(file_path, speed_factor)
    #combine_audiovideo('final.mp4', 'final.mp3', 'finalRESULT.mp4')

else:
    print("Error when selecting input option")
