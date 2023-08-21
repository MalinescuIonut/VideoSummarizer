import os
import subprocess
import sys
import time

import pysrt


def fragmentation(movie_path, movie_name, srt_file):
    # inputs: file containing the desired timestamps of the fragments, srt format
    os.chdir(movie_path)

    ##### make a copy of the original movie where all frames become keyframes
    allkframes = 'output_with_all_keyframes.mkv'
    command = f'ffmpeg -y -i {movie_name} -c:v libx264 -x264opts keyint=1 {allkframes}'
    with open('ffmpeg_command.bat', 'w') as bat_file:
        bat_file.write(command)
    subprocess.call(['ffmpeg_command.bat'], shell=True)

    with open("splitmovie.bat", 'w') as output:
        try:
            with open(srt_file, 'r') as input:
                subs = pysrt.open(srt_file)
                for sub in subs:
                    start_point = sub.start.hours * 3600 + sub.start.minutes * 60 + sub.start.seconds + float('0.' + str(sub.start.milliseconds))  # in seconds for ffmpeg
                    end_point = sub.end.hours * 3600 + sub.end.minutes * 60 + sub.end.seconds + float('0.' + str(sub.end.milliseconds))
                    output.write(f'ffmpeg -y -i {allkframes} -ss {start_point} -to {end_point} -c copy {sub.index}{sub.text}.mp4\n')

        except FileNotFoundError:
            print(f"File not found")

    batpath = os.path.join(movie_path, "splitmovie.bat")
    subprocess.call(['cmd.exe', '/c', batpath]) #need to run it through the Windows command interpreter (cmd.exe) because win32 cannot execute it directly
    #/c tells the program to open cmd.exe and close it after the command from splitmovie.bat is ran

    return


def main():
    start_time = time.time()

    movie_path = sys.argv[1]
    movie_name = sys.argv[2]
    srt_file = sys.argv[3]
    fragmentation(movie_path, movie_name, srt_file)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"{sys.argv[0]} execution time: {execution_time} seconds")
    os.remove("output_with_all_keyframes.mkv")


if __name__ == "__main__":
    main()
