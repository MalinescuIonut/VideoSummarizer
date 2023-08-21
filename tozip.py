import os
import shutil
import subprocess
import sys
from zipfile import ZipFile


def main():
    movie_path = sys.argv[1]
    movie_name = sys.argv[2]
    method = sys.argv[3]

    os.chdir(movie_path)
    name = f'{movie_name}'[:-4] #eliminate .zip from the name
    root_dir = f'{movie_path}'[:-6] #length("input") == 6
    os.chdir(root_dir)
    shutil.make_archive(f'{name}_{method}', 'zip', 'input')

    if os.path.exists(os.path.join(movie_path, f'{name}_{method}.zip')):
        print("ZIP file successfully created")
    else:
        print("The ZIP file was not created")


if __name__ == "__main__":
    main()
