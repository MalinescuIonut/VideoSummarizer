import os
import re
import pysrt


def add_text():
    subs = pysrt.open("subs.srt")
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

    all_text_len = 0
    index = 1
    with open("voice-else_subs.srt", 'w') as output:
        for sub in subs:
            text = sub.text
            all_text_len += len(text)
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
                output.write(str(index) + '\n' + content[1] + '\n' + text + '\n\n')
                index += 1
                last_end = current_end
            else:
                # we have a gap between last end and current start => separate it

                if current_start == [0, 0, 0]:
                    if current_end[0] <= last_end[0] and current_end[1] <= last_end[1] and current_end[2] <= \
                            last_end[2]:
                        print("end time < start time -> this output was eliminated and replaced")
                else:

                    seconds1 = "{:06.3f}".format(last_end[2]).replace('.', ',')
                    seconds2 = "{:06.3f}".format(current_start[2]).replace('.', ',')
                    new_content = f'{last_end[0]:02}:{last_end[1]:02}:{seconds1} --> {current_start[0]:02}:{current_start[1]:02}:{seconds2}'
                    output.write(str(index) + '\n' + new_content + '\n' + "else" + '\n\n')
                    index += 1
                    # after writing the gap info, we'll also write the current object
                    output.write(str(index) + '\n' + content[1] + '\n' + text + '\n\n')
                    index += 1
                    last_end = current_end


    # for the last fragment - final index
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

    print('\n\n', index-1, " subtitles")
    print(all_text_len, " characters")
    print(all_text_len/(index-1), " average nr. of characters/subtitle\n\n")

    return all_text_len/(index-1)


def speedup_subs(voice_rate, else_rate, merged_movie_name, avg):
    subs = pysrt.open("voice-else_subs.srt")
    idx = 1
    prev_end = []
    total_else = 0
    total_voice = 0
    counter_else = 0
    counter_voice = 0

    for sub in subs:
        line_duration = sub.end.hours * 3600 + sub.end.minutes * 60 + sub.end.seconds + \
                        float('0.' + str(sub.end.milliseconds)) - sub.start.hours * 3600 - \
                        sub.start.minutes * 60 - sub.start.seconds - float('0.' + str(sub.start.milliseconds))
        if sub.text == 'else':
            total_else += line_duration
            counter_else += 1
        else:
            total_voice += len(sub.text)
            counter_voice += 1

    avg_else_time = total_else/counter_else
    avg_voice_char = total_voice / counter_voice

    with open(f'{merged_movie_name}.srt', 'w') as output:
        for sub in subs:

            if sub.text == 'else':
                speed_rate = else_rate
            else:
                speed_rate = voice_rate
            line_duration = sub.end.hours * 3600 + sub.end.minutes * 60 + sub.end.seconds + \
                            float('0.' + str(sub.end.milliseconds)) - sub.start.hours * 3600 - \
                            sub.start.minutes * 60 - sub.start.seconds - float('0.' + str(sub.start.milliseconds))

            new_duration = float(speed_rate) * line_duration
            if sub.text != 'else' and new_duration < 0.5 and len(sub.text) >= 1.75 * avg_voice_char:
                print(f'!!!!!!!!! old duration: {new_duration}')
                new_duration = 0.5

            if sub.text == 'else' and new_duration <= 0.12 * avg_else_time:
                print(f'!!!!!!!!! old duration: {new_duration}')
                new_duration = 0.12 * avg_else_time

            if sub.index == 1:
                new_start = [sub.start.hours, sub.start.minutes, sub.start.seconds + float('0.' + str(sub.start.milliseconds))]
                if sub.text == 'else':
                    new_duration = line_duration
            else:
                new_start = prev_end

            start_end_distance = new_start[0] * 3600 + new_start[1] * 60 + new_start[2] + new_duration
            hour = int(start_end_distance / 3600)
            minutes = int((float(start_end_distance / 3600) - hour) * 60)
            seconds = ((float(start_end_distance / 3600) - hour) * 60 - minutes) * 60
            end_seconds = "{:06.3f}".format(seconds)
            end_seconds = end_seconds.replace('.', ',')

            new_end = [hour, minutes, seconds]
            prev_end = new_end
            start_seconds = "{:06.3f}".format(new_start[2])
            start_seconds = start_seconds.replace('.', ',')

            print(f'{sub.index}\n{new_start[0]:02}:{new_start[1]:02}:{start_seconds} --> {new_end[0]:02}:{new_end[1]:02}:{end_seconds}\n{sub.text}\n\n')

            if sub.text != 'else':
                output.write(f"{idx}\n")
                output.write(f"{new_start[0]:02}:{new_start[1]:02}:{start_seconds} --> {new_end[0]:02}:{new_end[1]:02}:{end_seconds}\n")
                output.write(f"{sub.text}\n\n")
                idx += 1

    print(avg_else_time)
    print(avg_voice_char)
    return


def main():
    with open("configfile.txt", 'r', encoding='utf8', newline='\r\n') as file:
        data = []
        lines = file.read().splitlines()
        for line in lines:
            data.append(line.split("=")[1])
        input_path = data[0]
        main_path = data[1]
        movie_name = data[2]
        voice_speed = data[3]
        else_speed = data[4]

    os.chdir(input_path)
    avg = add_text()
    speedup_subs(voice_speed, else_speed, "merged_video", avg)


if __name__ == "__main__":
    main()
