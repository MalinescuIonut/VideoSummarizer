import os
import re
import shutil
import subprocess
import pysrt
import fileinput

def frame_Detection(folder_path, movie_name):
    os.chdir(folder_path)

    # before speeding up:
    with open("framedetection.bat", 'w') as output:
        output.write(
            f'ffprobe -loglevel error -select_streams v:0 -show_entries packet=pts_time,flags -of csv=print_section=0 {movie_name}\n')

    batpath = os.path.join(folder_path, "framedetection.bat")
    f = open("frames.txt", 'w')
    subprocess.call([f'{batpath}'], stdout=f)

    with open("frames.txt", 'r') as input:
        with open("kframes.txt", 'w') as output:
            for line in input:
                if "K__" in line.strip("\n"):
                    output.write(line)
    return

#simplify this function using pysrt
def fill_srt(file_name):
    subs = pysrt.open(file_name)

    try:
        file = open("kframes.txt", "r")
    except FileNotFoundError:
        print(f"File not found")
    line = file.readline()
    firstkframe = float(line.split(",")[0])
    last_hour = int(firstkframe / 3600)
    last_minutes = int((float(firstkframe / 3600) - last_hour) * 60)
    last_seconds = ((float(firstkframe / 3600) - last_hour) * 60 - last_minutes) * 60
    last_end = [int(last_hour), int(last_minutes), float(last_seconds)]  # h/min/s


    index = 1
    with open("voice-else_subs.srt", 'w') as output:
        for sub in subs:
            content = str(sub)
            content = content.splitlines()

            start_h = int(re.findall(r'(\d+\d+):', content[1])[0])
            start_min = int(re.findall(r':(\d+\d+):', content[1])[0])
            start_s = re.findall(r':(\d+\d+,\d+\d+\d+)', content[1])[0]
            start_s = float(start_s.replace(',', '.'))

            end_h = int(re.findall(r'(\d+\d+):', content[1])[2])
            end_min = int(re.findall(r':(\d+\d+):', content[1])[1])
            end_s = re.findall(r':(\d+\d+,\d+\d+\d+)', content[1])[1]
            end_s = float(end_s.replace(',', '.'))

            current_start = [start_h, start_min, start_s]
            current_end = [end_h, end_min, end_s]

            if current_start == last_end:
                output.write(str(index) + '\n' + content[1] + '\n' + "voice" + '\n\n')
                index += 1
                last_end = current_end
            else:
                # we have a gap between last end and current start => if the gap is longer than 1s => separate it
                gap_duration = (start_h * 3600 + start_min * 60 + start_s) - (last_end[0] * 3600 + last_end[1] * 60 +
                                                                              last_end[2])
                if gap_duration > 1:
                    seconds1 = "{:06.3f}".format(last_end[2]).replace('.', ',')
                    seconds2 = "{:06.3f}".format(current_start[2]).replace('.', ',')
                    new_content = f'{last_end[0]:02}:{last_end[1]:02}:{seconds1} --> {current_start[0]:02}:{current_start[1]:02}:{seconds2}'
                    output.write(str(index) + '\n' + new_content + '\n' + "else" + '\n\n')
                    index += 1
                    # after writing the gap info, we'll also write the current object
                    output.write(str(index) + '\n' + content[1] + '\n' + "voice" + '\n\n')
                    index += 1
                    last_end = current_end

                else:
                    # special case for first subtitle
                    if current_start == [0, 0, 0]:
                        if current_end[0] <= last_end[0] and current_end[1] <= last_end[1] and current_end[2] <= last_end[2]:
                            print("STOP")
                    else:
                        seconds1 = "{:06.3f}".format(last_end[2]).replace('.', ',')
                        seconds2 = "{:06.3f}".format(current_end[2]).replace('.', ',')
                        new_content = f'{last_end[0]:02}:{last_end[1]:02}:{seconds1} --> {current_end[0]:02}:{current_end[1]:02}:{seconds2}'
                        output.write(str(index) + '\n' + new_content + '\n' + "voice" + '\n\n')
                        index += 1
                        last_end = current_end

    #for the last fragment - final index
    with open('kframes.txt', 'r') as f:
        last_line = f.readlines()[-1]
    lastkeyframe = float(last_line.split(",")[0])
    final_hour = int(lastkeyframe / 3600)
    final_minutes = int((float(lastkeyframe / 3600) - final_hour) * 60)
    final_seconds = ((float(lastkeyframe / 3600) - final_hour) * 60 - final_minutes) * 60
    final_time = [int(final_hour), int(final_minutes), float(final_seconds)]  # h/min/s
    if last_end != final_time:
        with open("voice-else_subs.srt", 'a') as output:
            seconds1 = "{:06.3f}".format(last_end[2]).replace('.', ',')
            seconds2 = "{:06.3f}".format(final_time[2]).replace('.', ',')
            new_content = f'{last_end[0]:02}:{last_end[1]:02}:{seconds1} --> {final_time[0]:02}:{final_time[1]:02}:{seconds2}'
            output.write(str(index) + '\n' + new_content + '\n' + "else" + '\n\n')
    index += 1

    return


def compress_srt(file_name):
    subs = pysrt.open(file_name)
    current_start = 0
    current_end = 0
    current_text = ""
    current_index = 0

    with open("compr_subs.srt", "w") as output_file:
        for sub in subs:
            if sub.text == current_text:
                current_end = sub.end
            else:
                output_file.write(f"{current_index}\n")
                output_file.write(f"{current_start} --> {current_end}\n")
                output_file.write(f"{current_text}\n\n")
                current_start = sub.start
                current_end = sub.end
                current_text = sub.text
                current_index += 1

        if current_start != 0:
            output_file.write(f"{current_index}\n")
            output_file.write(f"{current_start} --> {current_end}\n")
            output_file.write(f"{current_text}\n\n")

    return


def determine_index(srt_file):
    subs = pysrt.open(srt_file)
    for sub in subs:
        content = str(sub)
        content = content.splitlines()
        index = content[0]

    return index


def fragmentation(folder_path, movie_name, reference):
    # inputs: file containing the desired timestamps of the fragments, srt format

    with open("splitmovie.bat", 'w') as output:
        try:
            with open(reference, 'r') as input:
                subs = pysrt.open(reference)
                for sub in subs:
                    start_point = sub.start.hours * 3600 + sub.start.minutes * 60 + sub.start.seconds + float('0.' + str(sub.start.milliseconds))  # in seconds for ffmpeg
                    end_point = sub.end.hours * 3600 + sub.end.minutes * 60 + sub.end.seconds + float('0.' + str(sub.end.milliseconds))
                    output.write(f'ffmpeg -i {movie_name} -ss {start_point} -to {end_point} -async 1 {sub.index}{sub.text}.mp4\n')

        except FileNotFoundError:
            print(f"File not found")

    batpath = os.path.join(current_path, "splitmovie.bat")
    subprocess.call([f'{batpath}'])

    return


def selective_acc(root_path, current_dir, index, voice_speed, else_speed):
    # after the .mp4 files are created, the ones named {index}voice will have acc_rate1 and the {index}else -> acc_rate2
    current_file = ""
    current_speed = 0
    for i in range(1, int(index) + 1):
        if os.path.exists(os.path.join(current_dir, f'{i}else.mp4')):
            current_file = f'{i}else.mp4'
            current_speed = else_speed
        elif os.path.exists(os.path.join(current_dir, f'{i}voice.mp4')):
            current_file = f'{i}voice.mp4'
            current_speed = voice_speed

        if current_file != "" and current_speed != 0:
            speedup_file(root_path, current_dir, current_file, current_speed, f'{i}.mp4')

        #try:
        #    os.remove(f'{i}else.mp4')
        #    os.remove(f'{i}voice.mp4')
        #except FileNotFoundError:
        #    print(f"File not found")
    return


def speedup_file(root_path, current_path, file_name, speed_rate, output_name):
    shutil.copyfile(os.path.join(current_path, file_name), os.path.join(root_path, file_name))
    new_content = f"PATH={os.path.join(root_path, file_name)}\nOPTION=speed\nSPEED={speed_rate}\nLENGTH=3\n"
    os.chdir(root_path)
    with open("configurationSpeed.txt", 'w') as file:
        file.write(new_content)
    subprocess.run(["python", "speedup.py"])

    try:
        if os.path.exists(os.path.join(root_path, 'finalRESULT.mkv')):
            os.rename('finalRESULT.mkv', output_name)
            shutil.move(os.path.join(root_path, output_name), os.path.join(current_path, output_name))
    except FileNotFoundError:
        print(f"File not found")
    except Exception as e:
        print("Error reading file")

    try:
        if os.path.exists(os.path.join(root_path, file_name)):
            os.remove(file_name)  # from root path
    except FileNotFoundError:
        print(f"File not found")

    os.chdir(current_path)

    return


def movie_maker(index, current_path):
    os.chdir(current_path)
    video_list = [f"{i}.mp4" for i in range(1, int(index) + 1)]
    temp_file_list = []
    concat_txt = os.path.join(current_path, 'concat.txt')

    with open(concat_txt, 'w') as output:
        for video in video_list:
            temp_file = os.path.join(current_path,
                                     f"temp{video[:-4]}.ts")  # [:-4] - to remove the last four characters from "video"
            subprocess.run(
                ['ffmpeg', '-i', video, '-c', 'copy', '-bsf:v', 'h264_mp4toannexb', '-f', 'mpegts', temp_file])
            # -bsf:v h264_mp4toannexb -> converts the video stream to the Annex B byte stream format required for MPEG-TS containers
            # -f mpegts -> set the output format to MPEG-TS (Transport Stream) = a container format used for streaming media
            temp_file_list.append(temp_file)
            output.write(f"file '{temp_file}'\n")

    output_file = os.path.join(current_path, 'merged_video.mp4')
    subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_txt, '-c', 'copy', '-c:a', 'copy', '-bsf:a',
                    'aac_adtstoasc', output_file])
    # '-bsf:a', 'aac_adtstoasc' -> bitstream filter, converts the audio stream to the ASC (Audio Specific Configuration) format required for MPEG-TS containers

    # Remove the temporary files
    try:
        for temp_file in temp_file_list:
            os.remove(temp_file)
    except FileNotFoundError:
        print(f"File not found")

    #for i in range(1, int(index) + 1):
    #    try:
    #        os.remove(f'{i}.mp4')
    #    except FileNotFoundError:
    #        print(f"File not found")

    return


######  main #######

with open("configfile.txt", 'r', encoding='utf8', newline='\r\n') as file:
    data = []
    lines = file.read().splitlines()
    for line in lines:
        data.append(line.split("=")[1])
    root_path = data[0]  # here is stored speed.py and its config file
    current_path = data[1]  # points to the place where newcut.py, its config file, and a copy of cut.mkv are stored
    movie_name = data[2]
    voice_speed = float(data[3])
    else_speed = float(data[4])

reference = input(
    "Choose the desired reference for splitting the movie:\n inaSpeechSegmenter results (type ina) of subtitle file (type srt): ")
if reference != 'srt' and reference != 'ina':
    raise Exception("Invalid input - reference choice")

frame_Detection(current_path, movie_name)
srt_file = ""

if reference == 'srt':
    srt_file = input(
        "Provide the .srt track and enter its name or provide a video with one track - the program will automatically substract it\nEnter the name of the srt file or - : ")
    if len(re.findall(r'(\w+).srt', srt_file)) == 0 and srt_file != '-':
        raise Exception("Invalid input - srt choice")
    if srt_file == '-':
        # in this case, we'll find the sub track with ffmpeg
        subprocess.run(['ffmpeg', '-i', movie_name, '-map', '0:s:0', 'subs.srt'])
        srt_file = 'subs.srt'

elif reference == 'ina':
    print('In this case, an analysis based on the inaSpeechSegmenter will be performed to detect the fragments with noise/music/silence and voice content')
    subprocess.run(["python", "inaAnalysis.py"])    #--> we'll obtain the inaSpeechAnalysis results in original format and srt format
    #in the srt format, the male/female lines are reduced to voice, and noise/music/silence to else
    srt_file = 'inaSpeech_subs.srt'

# else-voice_subs.srt will contain the subtitles simplified to "voice" (for fragments with subs) and else (for fragments w/out subs, larger than 1s)
fill_srt(srt_file)
srt_file = "voice-else_subs.srt"

#compr_subs.srt will reduce the number of subtitles by merging together all consecutive voice subs
compress_srt(srt_file)
srt_file = "compr_subs.srt"

#determine the total nr of fragments to be generated
index = determine_index(srt_file)
print(index)

#cut the movie into fragments following the timemap provided in the reference srt file "srt_file"
fragmentation(current_path, movie_name, srt_file)

selective_acc(root_path, current_path, index, voice_speed, else_speed)
movie_maker(index, current_path)
