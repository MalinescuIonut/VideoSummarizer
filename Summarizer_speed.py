import re
from os.path import getsize

from pydub import AudioSegment
from pyannote.audio import Pipeline
import subprocess
import os
import shutil
from inaSpeechSegmenter import Segmenter
from pymediainfo import MediaInfo


def extract_statistics(origin_path, file_name):
    os.chdir(origin_path)
    input_path = os.path.join(origin_path, file_name)
    seg = Segmenter()
    total_segmentation = seg(input_path)
    labels = []  # list defined for storing the labels

    with open("inaSpeech_results.txt", "w") as file:
        for input_det in total_segmentation:
            label, start_time, end_time = input_det
            line = f"{label}: {start_time} --> {end_time} => {end_time - start_time}"
            labels.append(label)
            file.write(line + '\n')

    return


def noise_silence_music():
    # keep only noise/music/silence scenes over 10s

    with open("inaSpeech_results.txt", 'r') as input:
        with open("noise_silence_music.txt", 'w') as output:
            for line in input:
                if 'noise' in line.strip("\n"):
                    output.write(line)
                elif 'music' in line.strip("\n"):
                    output.write(line)
                elif 'noEnergy' in line.strip("\n"):
                    output.write(line)

    return


def fragmentation(path, file_name):
    os.chdir(path)
    index = 0
    temp = 0

    with open("output.bat", 'w') as output:
        with open("noise_silence_music.txt", 'r') as input:
            for line in input:
                start_time = re.findall(r': (\d+\.\d+)', line)[0]
                stop_time = re.findall(r'--> (\d+\.\d+)', line)[0]
                duration = re.findall(r'=> (\d+\.\d+)', line)[0]

                # in the next part, I'll check if the current and the previous fragments are consecutive or not
                # if there is a time difference between the previous end_time (stored in temp) and the current start_time
                # => we have a voice (female/male) fragment between temp and start time => special name to signal them = {index}_voice
                # otherwise, if the files are consecutive, we have 2 music/noise/silence files and we'll give them a generic name = {index}

                if (start_time == temp):  # if the segments described in the lines of the txt are consecutive
                    output.write(
                        f'ffmpeg -i {file_name} -ss {start_time} -t {duration} -async 1 {index}.mp4\n')
                    #ffmpeg -i movie.mp4 -ss 00:00:03 -t 00:00:08 -async 1 cut.mp4
                    # output.write('pause\n')

                else:
                    # we should create 2 files: one corresponding to the timestamps from the current line and one for the time gap, indicating voice input
                    duration_voice = float(start_time) - float(temp)
                    output.write(
                        f'ffmpeg -i {file_name} -ss {temp} -t {duration_voice} -async 1 {index}_voice.mp4\n')
                    # output.write('pause\n')
                    index += 1
                    output.write(
                        f'ffmpeg -i {file_name} -ss {start_time} -t {duration} -async 1 {index}.mp4\n')
                    # output.write('pause\n')

                index += 1
                temp = stop_time

    batpath = os.path.join(path, "output.bat")
    subprocess.call([f'{batpath}'])

    return index

def selective_acc(origin_path, folder_path, index):

    # copy configurationSum.txt and speedup.py to path
    #shutil.copyfile(os.path.join(origin_path, "configurationSpeed.txt"), os.path.join(path, "configurationSpeed.txt"))
    #shutil.copyfile(os.path.join(origin_path, "speedup.py"), os.path.join(path, "speedup.py"))

    # after the .mp4 files are created, only the ones named {index} will be accelerated
    for i in range(index):
        if os.path.exists(os.path.join(folder_path, f'{i}.mp4')):
            shutil.copyfile(os.path.join(folder_path, f'{i}.mp4'), os.path.join(origin_path, f'{i}.mp4'))
            new_content = f"PATH={os.path.join(folder_path, f'{i}.mp4')}\nOPTION=speed\nSPEED=0.5\nLENGTH=3\n"
            #print(new_content)
            os.chdir(origin_path)
            with open("configurationSpeed.txt", 'w') as file:
                file.write(new_content)
            with open("speedup.py") as run:
                exec(run.read())
            os.rename('finalRESULT.mkv', f'{i}_acc.mkv')
            shutil.move(os.path.join(origin_path, f'{i}_acc.mkv'), os.path.join(folder_path, f'{i}_acc.mkv'))
            os.remove(f'{i}.mp4')
            os.chdir(folder_path)
            os.remove(f'{i}.mp4')
            os.rename(f'{i}_acc.mkv', f'{i}.mp4')
        if os.path.exists(os.path.join(folder_path, f'{i}_voice.mp4')):
            os.rename(f'{i}_voice.mp4', f'{i}.mp4')

    return


def movie_maker(index, folder_path):
    os.chdir(folder_path)
    video_list = [f"{i}.mp4" for i in range(index)]
    temp_file_list = []
    concat_txt = os.path.join(folder_path, 'concat.txt')

    with open(concat_txt, 'w') as output:
        for video in video_list:
            temp_file = os.path.join(folder_path, f"temp{video[:-4]}.ts")   #[:-4] - to remove the last four characters from "video"
            subprocess.run(['ffmpeg', '-i', video, '-c', 'copy', '-bsf:v', 'h264_mp4toannexb', '-f', 'mpegts', temp_file])
            #-bsf:v h264_mp4toannexb -> converts the video stream to the Annex B byte stream format required for MPEG-TS containers
            #-f mpegts -> set the output format to MPEG-TS (Transport Stream) = a container format used for streaming media
            temp_file_list.append(temp_file)
            output.write(f"file '{temp_file}'\n")

    output_file = os.path.join(folder_path, 'merged_video.mp4')
    subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_txt, '-c', 'copy', '-c:a', 'copy', '-bsf:a', 'aac_adtstoasc', output_file])
    #'-bsf:a', 'aac_adtstoasc' -> bitstream filter, converts the audio stream to the ASC (Audio Specific Configuration) format required for MPEG-TS containers

    # Remove the temporary files
    for temp_file in temp_file_list:
        os.remove(temp_file)

    return


# configuration file
with open("configurationSum.txt", 'r', encoding='utf8', newline='\r\n') as input:
    data = []
    lines = input.read().splitlines()
    for line in lines:
        data.append(line.split("=")[1])
    file_path = data[0]
    file_name = data[1]

print(file_path, '\n\n\n')

# create new folder for the movie fragments
movie_name = re.findall(r'\w+', file_name)[0]
folder_name = f'{movie_name}_moviecuts'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
folder_path = os.path.join(file_path, folder_name)
os.makedirs(folder_path, exist_ok=True)
shutil.copyfile(file_name, os.path.join(folder_path, file_name))

origin = file_path

with open("configurationSpeed.txt", 'r', encoding='utf8', newline='\r\n') as file:
    lines = file.read().splitlines()
updated_content = f"PATH={os.path.join(folder_path, file_name)}\nOPTION=speed\nSPEED=0.75\nLENGTH=3\n"
with open("configurationSpeed.txt", 'w', encoding='utf8', newline='\r\n') as file:
    file.write(updated_content)

with open("speedup.py") as f:
    exec(f.read())
shutil.move('finalRESULT.mkv', os.path.join(folder_path, 'finalRESULT.mkv'))
spedup_movie = 'finalRESULT.mkv'

os.chdir(folder_path)
os.remove(f'{file_name}')

extract_statistics(folder_path, spedup_movie)
noise_silence_music()
index = fragmentation(folder_path, spedup_movie)
selective_acc(origin, folder_path, index)
movie_maker(index, folder_path)
