import re
from pyannote.audio import Pipeline
import os
import subprocess
from inaSpeechSegmenter import Segmenter
import pysrt


def extract_statistics(origin_path, file_name):
    os.chdir(origin_path)
    input_path = os.path.join(origin_path, file_name)
    seg = Segmenter()
    total_segmentation = seg(input_path)

    with open("inaSpeech_results.txt", "w") as file:
        for input_det in total_segmentation:
            label, start_time, end_time = input_det
            line = f"{label}: {start_time} --> {end_time}"
            file.write(line + '\n')

    index = 0
    with open("inaSpeech_subs.srt", "w") as file:
        for input_det in total_segmentation:
            label, start_time, end_time = input_det
            if 'male' in label.strip():
                text = label

                hour = int(start_time / 3600)
                minutes = int((float(start_time / 3600) - hour) * 60)
                seconds = ((float(start_time / 3600) - hour) * 60 - minutes) * 60
                seconds = "{:06.3f}".format(seconds)
                start = f'{hour:02}:{minutes:02}:{seconds}'.replace('.', ',')

                hour = int(end_time / 3600)
                minutes = int((float(end_time / 3600) - hour) * 60)
                seconds = ((float(end_time / 3600) - hour) * 60 - minutes) * 60
                seconds = "{:06.3f}".format(seconds)
                end = f'{hour:02}:{minutes:02}:{seconds}'.replace('.', ',')

                index += 1
                line = f"{index}\n{start} --> {end}\n{text}\n"
                file.write(line + '\n')

    return

with open("configfile.txt", 'r', encoding='utf8', newline='\r\n') as input:
    data = []
    lines = input.read().splitlines()
    for line in lines:
        data.append(line.split("=")[1])
    file_path = data[1]
    file_name = data[2]

extract_statistics(file_path, file_name)