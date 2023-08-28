import os
import re
import shutil
import subprocess
import time
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


def main():

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
        ffmpeg_path = data[5]  # ex: C:\ffmpeg\bin\ffmpeg.exe

    ############### choose ina.srt reference <=> method
    reference = input(
        "Choose the desired reference for splitting the movie:\n inaSpeechSegmenter results (type ina) of subtitle file (type srt): ")
    if reference != 'srt' and reference != 'ina':
        raise Exception("Invalid input - reference choice")

    frame_detection(input_path, movie_name, main_path)
    srt_file = ""
    hc_sub = ""

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
        hc_sub = srt_file

    elif reference == 'ina':
        os.chdir(input_path)
        try:
            subprocess.run(['ffmpeg', '-i', movie_name, '-map', '0:s:0', 'subs.srt'])
            hc_sub = "subs.srt"
        except subprocess.CalledProcessError as e:
            print("An error occurred: ", e)

        os.chdir(main_path)
        print(
            'In this case, an analysis based on the inaSpeechSegmenter will be performed to detect the fragments with noise/music/silence and voice content')
        #subprocess.run(["python", 'inaAnalysis.py'])  # --> we'll obtain the inaSpeechAnalysis results in original format and srt format
        command = ["python", "inaAnalysis.py", input_path, movie_name]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            #print("Script output:", result.stdout)
        except subprocess.CalledProcessError as e:
            print("An error occurred: ", e)

        os.chdir(input_path)
        # in the srt format, the male/female lines are reduced to voice, and noise/music/silence to else
        srt_file = 'inaSpeech_subs.srt'
    print("\n------- Step 1: choosing reference and generating srt files --> COMPLETE ------\n")


    ############### hardcode the subs into the movie before cutting it
    ffmpeg_command = (
        f'"{ffmpeg_path}" -i "{movie_name}" -vcodec libx264 -acodec aac '
        f'-map "0:a:0" -map "0:v:0" -vf "subtitles={hc_sub}:force_style=FontSize=11" -y "{os.path.splitext(movie_name)[0]}_harcoded.mp4"'
    )
    with open("hardcode_subs.bat", 'w') as output:
        output.write(ffmpeg_command)
    batpath = os.path.join(os.getcwd(), "hardcode_subs.bat")
    subprocess.call(batpath)
    old_moviename = movie_name
    movie_name = f'{os.path.splitext(old_moviename)[0]}_harcoded.mp4'
    print(f"\n------- Step 1: the subtitles were hardcoded => new input = {movie_name} --> COMPLETE ------\n")


    ########format the srt file (original subs or ina srt output) into a simplified version
    os.chdir(main_path)
    #subprocess.run(["python", 'Format_srt.py'])
    command = ["python", "Format_srt.py", input_path, main_path, srt_file]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("Script output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("An error occurred: ", e)
    print("\n------- Step 2: formatting the srt file provided/generated into a simplified version --> COMPLETE ------\n")


    ####### movie fragmentation into voice/else fragments #########
    os.chdir(main_path)
    # cut the movie into fragments following the timemap provided in the reference srt file "srt_file"
    #subprocess.run(["python", 'Movie_cutter.py'])
    command = ["python", "Movie_cutter.py", input_path, movie_name, "compr_subs.srt"]
    try:
        subprocess.run(command, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred: ", e)
    print("\n------- Step 3: cutting the movie into voice/else mp4 fragments --> COMPLETE ------\n")


    ######## selective acceleration of movie fragments #######
    os.chdir(main_path)
    # accelerate the movie fragments with different speeds (one for voice content, one for gaps between lines)
    #subprocess.run(["python", 'Selective_acceleration.py'])
    command = ["python", "Selective_acceleration.py", main_path, input_path, "compr_subs.srt", str(voice_speed), str(else_speed)]
    try:
        subprocess.run(command, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred: ", e)
    print("\n------- Step 4: selective acceleration of voice/else mp4 files --> COMPLETE ------\n")


    ####### movie maker #######
    os.chdir(main_path)
    # merge the {index}.mp4 fragments into one final movie
    #subprocess.run(["python", 'Movie_maker.py'])
    command = ["python", "Movie_maker.py", main_path, input_path, "compr_subs.srt"]
    try:
        subprocess.run(command, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred: ", e)
    print("\n------- Step 5: putting together the accelerated mp4 files to create the summarized movie --> COMPLETE ------\n")


    ########speedup the summarized movie to fit the desired length#######
    os.chdir(input_path)
    sp_movie = 'merged_video.mp4'
    old_duration = subprocess.run(
       ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1',
        sp_movie], capture_output=True, text=True)
    old_duration = float(old_duration.stdout.strip())
    old_h = int(old_duration / 3600)
    old_min = int((float(old_duration / 3600) - old_h) * 60)
    old_s = ((float(old_duration / 3600) - old_h) * 60 - old_min) * 60
    print(f"Current duration: {old_h} hours, {old_min} minutes and {old_s} seconds")
    new_duration = 0
    speedup = input("If you are not pleased with the final length of the movie, insert here the desired duration in the following format: hh:mm:ss.ms (3 decimals for ms)\nOtherwise, press any key: ")
    if len(speedup) > 11:
        h = int(re.findall(r'(\d+\d+):', speedup)[0])
        mins = int(re.findall(r':(\d+\d+):', speedup)[0])
        s = float(re.findall(r':(\d+\d+.\d+\d+\d+)', speedup)[0])
        new_duration = h*60 + mins + s/60   #in minutes, required by the config file of the speedup.py program
        print("Desired duration [minutes]: ", new_duration)

        shutil.copyfile(os.path.join(input_path, sp_movie), os.path.join(main_path, sp_movie))
        os.chdir(main_path)
        new_content = f"PATH={os.path.join(main_path, sp_movie)}\nOPTION=length\nSPEED=1\nLENGTH={new_duration}\n"
        with open("configurationSpeed.txt", 'w') as file:
            file.write(new_content)
        subprocess.run(["python", "speedup.py"])

        try:
            if os.path.exists(os.path.join(main_path, 'finalRESULT.mkv')):
                os.rename('finalRESULT.mkv', f'compressedin_{new_duration}min.mp4')
                shutil.move(os.path.join(main_path, f'compressedin_{new_duration}min.mp4'), os.path.join(input_path, f'compressedin_{new_duration}min.mp4'))
        except FileNotFoundError:
            print(f"File not found")
        except Exception as e:
            print("Error reading file")

        print("\n------- Step 5.1 - optional\nspeed-up the summarized movie to fit in a certain length --> COMPLETE ------\n")


    ######## female/male screentime duration results########
    os.chdir(main_path)
    #subprocess.run(["python", 'VoiceElseDuration.py'])
    command = ["python", "VoiceElseDuration.py", input_path, movie_name, old_moviename]
    try:
        subprocess.run(command, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred: ", e)
    print("\n------- Step 6 - female/male/else inaSpeechSegmenter analysis on both the original and summarized movie --> COMPLETE ------\n")


    ########organize used files in folders############
    os.chdir(input_path)
    folder_normal = "fragments_normalcut"
    if not os.path.exists(folder_normal):
        os.makedirs(folder_normal)
    folder_speed = "fragments_spedup"
    if not os.path.exists(folder_speed):
        os.makedirs(folder_speed)
    folder_output = "output_results"
    if not os.path.exists(folder_output):
        os.makedirs(folder_output)
    folder_bat = "batfiles"
    if not os.path.exists(folder_bat):
        os.makedirs(folder_bat)

    normal_path = os.path.join(input_path, folder_normal)
    speed_path = os.path.join(input_path, folder_speed)
    output_path = os.path.join(input_path, folder_output)
    bat_path = os.path.join(input_path, folder_bat)

    index = determine_index("compr_subs.srt")
    print("Number of fragments to be generated: ", index)

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

    try:
        if os.path.exists(os.path.join(input_path, "merged_video.mp4")):
            shutil.move(os.path.join(input_path, "merged_video.mp4"), os.path.join(output_path, "summarized_video.mp4"))
        if os.path.exists(os.path.join(input_path, movie_name)):
            shutil.move(os.path.join(input_path, movie_name), os.path.join(output_path, movie_name))
        if os.path.exists(os.path.join(input_path, "inaSpeechSegmenter_voice_else_analysis")):
            shutil.move(os.path.join(input_path, "inaSpeechSegmenter_voice_else_analysis"), os.path.join(output_path, "inaSpeechSegmenter_voice_else_analysis"))
        if os.path.exists(os.path.join(input_path, "merged_video.srt")):
            shutil.move(os.path.join(input_path, "merged_video.srt"), os.path.join(output_path, "summarized_video.srt"))
        if os.path.exists(os.path.join(input_path, f'compressedin_{new_duration}min.mp4')):
            shutil.move(os.path.join(input_path, f'compressedin_{new_duration}min.mp4'), os.path.join(output_path, f'compressedin_{new_duration}min.mp4'))
        if os.path.exists(os.path.join(input_path, f'compressedin_{new_duration}min.srt')):
            shutil.move(os.path.join(input_path, f'compressedin_{new_duration}min.srt'), os.path.join(output_path, f'compressedin_{new_duration}min.srt'))

        try:
            if os.path.exists(os.path.join(input_path, old_moviename)):
                shutil.copy(os.path.join(input_path, old_moviename), os.path.join(output_path, old_moviename))
        except FileNotFoundError:
            print(f"File not found: {old_moviename}")

        os.chdir(input_path)
        for filename in os.listdir():
            if filename.endswith(".bat"):
                shutil.move(os.path.join(input_path, filename), os.path.join(bat_path, filename))

        os.chdir(main_path)
        os.remove("merged_video.mp4")
    except FileNotFoundError:
        print(f"File not found")
    print("\n------- Step 8 - the generated files were organized in their corresponding folders --> COMPLETE ------\n")


    ###### create zip with all generated files #########
    os.chdir(main_path)
    command = ["python", "tozip.py", input_path, old_moviename, reference]
    try:
        subprocess.run(command, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred: ", e)
    print("\n------- Step 9 - the input file was compressed in a zip file located in the root directory (containing both <input> and <program> --> COMPLETE ------\n")


    ######## delete all files included in the zip, but the original movie file ########
    os.chdir(main_path)
    restart = input(
        "Do you want to empty the input folder, except for the movie you provided as input? <yes> or any key: ")
    if restart == 'yes':
        #subprocess.run(["python", 'Restart.py'])
        command = ["python", "Restart.py", input_path, old_moviename]
        try:
            subprocess.run(command, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            print("An error occurred: ", e)
        print("\n------- Step 10* optional - the <input> folder is empty and ready for a new movie\nall the files generated and used for the previous movies can be found in their corresponding zip files\n--> COMPLETE ------")


if __name__ == "__main__":
    main()
