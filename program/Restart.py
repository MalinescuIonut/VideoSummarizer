import os
import shutil

with open("configfile.txt", 'r', encoding='utf8', newline='\r\n') as file:
    data = []
    lines = file.read().splitlines()
    for line in lines:
        data.append(line.split("=")[1])
    input_path = data[0]
    main_path = data[1]
    movie_name = data[2]

os.chdir(input_path)
for filename in os.listdir(input_path):
    if filename != movie_name:
        file_path = os.path.join(input_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete')