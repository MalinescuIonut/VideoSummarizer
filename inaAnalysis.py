from pyannote.audio import Pipeline
import os
import sys
from inaSpeechSegmenter import Segmenter
import pysrt


def extract_statistics(movie_path, file_name):
    os.chdir(movie_path)
    input_path = os.path.join(movie_path, file_name)
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


def main():

    movie_path = sys.argv[1]
    movie_name = sys.argv[2]
    extract_statistics(movie_path, movie_name)


if __name__ == "__main__":
    main()
