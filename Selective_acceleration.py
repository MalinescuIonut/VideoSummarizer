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


def selective_acc(speedup_path, input_path, index, voice_speed, else_speed):
    # after the .mp4 files are created, the ones named {index}voice will have acc_rate = voice_speed and {index}else -> else_speed
    current_file = ""
    current_speed = -1

    for i in range(1, int(index) + 1):
        os.chdir(input_path)
        if os.path.exists(os.path.join(input_path, f'{i}else.mp4')):
            current_file = f'{i}else.mp4'
            current_speed = else_speed
        elif os.path.exists(os.path.join(input_path, f'{i}voice.mp4')):
            current_file = f'{i}voice.mp4'
            current_speed = voice_speed
        else:
            raise Exception("\n--------Non-existent file--------\n")

        if current_file != "" and current_speed != -1:
            speedup_file(speedup_path, input_path, current_file, current_speed, f'{i}.mp4')

        # try:
        #    os.remove(f'{i}else.mp4')
        #    os.remove(f'{i}voice.mp4')
        # except FileNotFoundError:
        #    print(f"File not found")
    return


def speedup_file(speedup_path, current_path, file_name, speed_rate, output_name):
    shutil.copyfile(os.path.join(current_path, file_name), os.path.join(speedup_path, file_name))
    new_content = f"PATH={os.path.join(speedup_path, file_name)}\nOPTION=speed\nSPEED={speed_rate}\nLENGTH=3\n"
    os.chdir(speedup_path)
    with open("configurationSpeed.txt", 'w') as file:
        file.write(new_content)
    subprocess.run(["python", "speedup.py"])

    try:
        if os.path.exists(os.path.join(speedup_path, 'finalRESULT.mkv')):
            os.rename('finalRESULT.mkv', output_name)
            shutil.move(os.path.join(speedup_path, output_name), os.path.join(current_path, output_name))
        else:
            print(f"File not found: finalRESULT.mkv")
            shutil.copy(os.path.join(speedup_path, file_name), os.path.join(current_path, output_name))
    except FileNotFoundError:
        print(f"File not found: finalRESULT.mkv")
        shutil.copy(os.path.join(speedup_path, file_name), os.path.join(current_path, output_name))
    except Exception as e:
        print(f"Error reading file: finalRESULT.mkv")
        shutil.copy(os.path.join(speedup_path, file_name), os.path.join(current_path, output_name))

    try:
        if os.path.exists(os.path.join(speedup_path, file_name)):
            os.remove(file_name)  # from root path
    except FileNotFoundError:
        print(f"File not found")

    return


def main():

    main_path = sys.argv[1]
    input_path = sys.argv[2]
    srt_file = sys.argv[3]
    voice_speed = sys.argv[4]
    else_speed = sys.argv[5]

    os.chdir(input_path)
    index = determine_index(srt_file)
    selective_acc(main_path, input_path, index, voice_speed, else_speed)


if __name__ == "__main__":
    main()