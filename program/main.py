import os
import re
import shutil
import subprocess

import pysrt


def determine_index(srt_file):
    subs = pysrt.open(srt_file)
    index = 0
    for sub in subs:
        content = str(sub)
        content = content.splitlines()
        index = content[0]

    return index


def frame_detection(folder_path, movie_name, final_path):
    os.chdir(folder_path)

    with open("framedetection.bat", 'w') as output:
        output.write(
            f'ffprobe -loglevel error -select_streams v:0 -show_entries packet=pts_time,flags -of csv=print_section=0 {movie_name}\n')

    batpath = os.path.join(folder_path, "framedetection.bat")
    f = open("frames.txt", 'w')
    subprocess.call([f'{batpath}'], stdout=f)

    with open("frames.txt", 'r') as input:
        with open("kframes.txt", 'w') as output:
            for line in input:
                if "K" in line.strip("\n"):
                    output.write(line)

    os.chdir(final_path)
    return


######  main #######

with open("configfile.txt", 'r', encoding='utf8', newline='\r\n') as file:
    initial_content = file.read()
content_lines = initial_content.splitlines()
content_lines = "\n".join(content_lines)

with open("configfile.txt", 'r', encoding='utf8', newline='\r\n') as file:
    data = []
    lines = file.read().splitlines()
    for line in lines:
        data.append(line.split("=")[1])
    input_path = data[0]
    main_path = data[1]
    movie_name = data[2]
    voice_speed = float(data[3])
    else_speed = float(data[4])

reference = input(
    "Choose the desired reference for splitting the movie:\n inaSpeechSegmenter results (type ina) of subtitle file (type srt): ")
if reference != 'srt' and reference != 'ina':
    raise Exception("Invalid input - reference choice")

frame_detection(input_path, movie_name, main_path)
srt_file = ""

if reference == 'srt':
    srt_file = input(
        "Provide the .srt track and enter its name or provide a video with one track - the program will automatically substract it\nEnter the name of the srt file or - : ")
    if len(re.findall(r'(\w+).srt', srt_file)) == 0 and srt_file != '-':
        raise Exception("Invalid input - srt choice")
    if srt_file == '-':
        # in this case, we'll find the sub track with ffmpeg
        os.chdir(input_path)
        subprocess.run(['ffmpeg', '-i', movie_name, '-map', '0:s:0', 'subs.srt'])
        srt_file = 'subs.srt'

elif reference == 'ina':
    os.chdir(main_path)
    print(
        'In this case, an analysis based on the inaSpeechSegmenter will be performed to detect the fragments with noise/music/silence and voice content')
    subprocess.run(["python",
                    'inaAnalysis.py'])  # --> we'll obtain the inaSpeechAnalysis results in original format and srt format
    os.chdir(input_path)
    # in the srt format, the male/female lines are reduced to voice, and noise/music/silence to else
    srt_file = 'inaSpeech_subs.srt'

os.chdir(main_path)
with open("configfile.txt", 'a') as file:
    file.write(f'\nsrt_file={srt_file}')

subprocess.run(["python", 'Format_srt.py'])

with open("configfile.txt", 'w') as file:
    file.write(content_lines)

with open("configfile.txt", 'a') as app:
    app.write(f'\nsrt_file=compr_subs.srt')

os.chdir(main_path)
# cut the movie into fragments following the timemap provided in the reference srt file "srt_file"
#subprocess.run(["python", 'Movie_cutter.py'])

os.chdir(main_path)
# accelerate the movie fragments with different speeds (one for voice content, one for gaps between lines)
#subprocess.run(["python", 'Selective_acceleration.py'])

os.chdir(main_path)
# merge the {index}.mp4 fragments into one final movie
#subprocess.run(["python", 'Movie_maker.py'])

os.chdir(main_path)
with open("configfile.txt", 'w') as file:
    file.write(content_lines)

speedup = input("If you are not pleased with the final length of the movie, insert here the desired duration in the following format: hh:mm:ss.ms (3 decimals for ms)\nOtherwise, press any key: ")
if len(speedup) > 11:
    h = int(re.findall(r'(\d+\d+):', speedup)[0])
    mins = int(re.findall(r':(\d+\d+):', speedup)[0])
    s = float(re.findall(r':(\d+\d+.\d+\d+\d+)', speedup)[0])
    new_duration = h*60 + mins + s/60   #in minutes, required by the config file of the speedup.py program
    print("Desired duration [minutes]: ", new_duration)

    # if you want to generate the new version in the "input" folder, uncomment the following lines:
    #os.chdir(input_path)
    #sp_movie = 'merged_video.mp4'

    sp_movie = 'SummarizedMovie.mp4'
    #old_duration = subprocess.run(
    #    ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1',
    #     sp_movie], capture_output=True, text=True)
    #old_duration = float(old_duration.stdout.strip())
    #print("Current duration:", old_duration)

    #shutil.copyfile(os.path.join(input_path, file_name), os.path.join(main_path, file_name))
    new_content = f"PATH={os.path.join(main_path, sp_movie)}\nOPTION=length\nSPEED=1\nLENGTH={new_duration}\n"
    with open("configurationSpeed.txt", 'w') as file:
        file.write(new_content)
    subprocess.run(["python", "speedup.py"])

    try:
        os.rename('finalRESULT.mkv', f'compressedin_{new_duration}min.mp4')
        #shutil.move(os.path.join(main_path, f'compressedin_{new_duration}min.mp4'), os.path.join(input_path, f'compressedin_{new_duration}min.mp4'))
    except FileNotFoundError:
        print(f"File not found")
    except Exception as e:
        print("Error reading file")

    #try:
    #    if os.path.exists(os.path.join(main_path, f'compressedin_{new_duration}min.mp4')):
    #        os.remove(f'compressedin_{new_duration}min.mp4')  # from root path
    #except FileNotFoundError:
    #    print(f"File not found")

os.chdir(input_path)
#make folders for simple fragments and spedup fragments
folder_normal = "fr_normalcut"  # Format folder name with leading zeros
if not os.path.exists(folder_normal):
    os.makedirs(folder_normal)
folder_speed = "fr_spedup"  # Format folder name with leading zeros
if not os.path.exists(folder_speed):
    os.makedirs(folder_speed)

normal_path = os.path.join(input_path, folder_normal)
speed_path = os.path.join(input_path, folder_speed)

index = determine_index("compr_subs.srt")
print(index)
try:
    for i in range(1, int(index) + 1):
        if os.path.exists(os.path.join(input_path, f'{i}else.mp4')):
            shutil.move(os.path.join(input_path, f'{i}else.mp4'), os.path.join(normal_path, f'{i}else.mp4'))
        elif os.path.exists(os.path.join(input_path, f'{i}voice.mp4')):
            shutil.move(os.path.join(input_path, f'{i}voice.mp4'), os.path.join(normal_path, f'{i}voice.mp4'))
except FileNotFoundError:
    print(f"File not found")

try:
    for i in range(1, int(index) + 1):
        if os.path.exists(os.path.join(input_path, f'{i}.mp4')):
            shutil.move(os.path.join(input_path, f'{i}.mp4'), os.path.join(speed_path, f'{i}.mp4'))
except FileNotFoundError:
    print(f"File not found")

os.chdir(main_path)
restart = input("Do you want to delete the mp4 fragments and srt files generated by the process? <yes> or <no> answers: ")
if restart == 'yes':
    subprocess.run(["python", 'Restart.py'])

os.chdir(main_path)
