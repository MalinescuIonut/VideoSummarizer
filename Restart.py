import os
import shutil
import sys


def main():

    input_path = sys.argv[1]
    movie_name = sys.argv[2]

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


if __name__ == "__main__":
    main()
