import os
import re
import pysrt


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
                            print("end time < start time -> this output was eliminated and replaced")
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
                if current_end != 0:
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
    index = 0
    for sub in subs:
        content = str(sub)
        content = content.splitlines()
        index = content[0]

    return index


with open("configfile.txt", 'r', encoding='utf8', newline='\r\n') as file:
    data = []
    lines = file.read().splitlines()
    for line in lines:
        data.append(line.split("=")[1])
    input_path = data[0]
    main_path = data[1]
    movie_name = data[2]
    srt_file = data[5]

os.chdir(input_path)

# else-voice_subs.srt will contain the subtitles simplified to "voice" (for fragments with subs) and else (for fragments w/out subs, larger than 1s)
fill_srt(srt_file)
srt_file = "voice-else_subs.srt"

# compr_subs.srt will reduce the number of subtitles by merging together all consecutive voice subs
compress_srt(srt_file)
srt_file = "compr_subs.srt"

# determine the total nr of fragments to be generated
index = determine_index(srt_file)
print(index)

os.chdir(main_path)

