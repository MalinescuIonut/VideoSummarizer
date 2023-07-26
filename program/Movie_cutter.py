import os
import subprocess
import pysrt


def fragmentation(movie_path, movie_name, srt_file):
    # inputs: file containing the desired timestamps of the fragments, srt format
    os.chdir(movie_path)
    with open("splitmovie.bat", 'w') as output:
        try:
            with open(srt_file, 'r') as input:
                subs = pysrt.open(srt_file)
                for sub in subs:
                    start_point = sub.start.hours * 3600 + sub.start.minutes * 60 + sub.start.seconds + float('0.' + str(sub.start.milliseconds))  # in seconds for ffmpeg
                    end_point = sub.end.hours * 3600 + sub.end.minutes * 60 + sub.end.seconds + float('0.' + str(sub.end.milliseconds))
                    output.write(f'ffmpeg -i {movie_name} -ss {start_point} -to {end_point} -async 1 {sub.index}{sub.text}.mp4\n')

        except FileNotFoundError:
            print(f"File not found")

    batpath = os.path.join(movie_path, "splitmovie.bat")
    subprocess.call([f'{batpath}'])

    return

with open("configfile.txt", 'r', encoding='utf8', newline='\r\n') as input:
    data = []
    lines = input.read().splitlines()
    for line in lines:
        data.append(line.split("=")[1])
    movie_path = data[0]
    program_path = data[1]
    movie_name = data[2]
    srt_file = data[5]

fragmentation(movie_path, movie_name, srt_file)
