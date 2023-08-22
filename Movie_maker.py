import os
import shutil
import subprocess
import sys

import pysrt


def determine_index(srt_file):
    subs = pysrt.open(srt_file)
    index = 0
    for sub in subs:
        content = str(sub)
        content = content.splitlines()
        index = content[0]

    return index


def movie_maker(index, current_path):

    video_list = [f"{i}.mp4" for i in range(1, int(index) + 1)]
    temp_file_list = []
    concat_txt = os.path.join(current_path, 'concat.txt')

    with open(concat_txt, 'w') as output:
        for video in video_list:
            temp_file = os.path.join(current_path,
                                     f"temp{video[:-4]}.ts")  # [:-4] - to remove the last four characters from "video"
            terminalText = subprocess.run(
                ['ffmpeg', '-y', '-i', video, '-c', 'copy', '-bsf:v',
                 'h264_mp4toannexb', '-f', 'mpegts', temp_file], capture_output=True, text=True)

            # -bsf:v h264_mp4toannexb -> converts the video stream to the Annex B byte stream format required for MPEG-TS containers
            # -f mpegts -> set the output format to MPEG-TS (Transport Stream) = a container format used for streaming media

            if not os.path.isfile(temp_file):
                print("error executing " + str(['ffmpeg', '-i', video, '-c', 'copy', '-bsf:v', 'h264_mp4toannexb', '-f', 'mpegts', temp_file]))
                print(terminalText.stderr)
            else:
                temp_file_list.append(temp_file)
                output.write(f"file '{temp_file}'\n")

    output_file = os.path.join(current_path, 'merged_video.mp4')
    subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', concat_txt, '-c:a', 'copy', '-bsf:a',
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


def main():

    main_path = sys.argv[1]
    input_path = sys.argv[2]
    srt_file = sys.argv[3]

    os.chdir(input_path)
    index = determine_index(srt_file)
    movie_maker(index, input_path)


if __name__ == "__main__":
    main()
