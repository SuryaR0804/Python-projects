import os, shutil
from sys import argv   
from pathlib import Path


def get_dir(filename):  #rerturns what directory
    extension=filename.suffix[1:]       #get extension
    directory_name=dirs.get(extension, "Miscellaneous") #default value "Miscellaneous" as a directory name for files that are not in our dictionary.
    return directory_name

#Extensions and their directories
dirs={   
    #Images
    "jpeg":"Images",
    "png":"Images",
    "jpg":"Images",
    "tiff":"Images",
    "gif":"Images",

    #Videos
    "mp4":"Videos",
    "mkv":"Videos",
    "mov":"Videos",
    "webm":"Videos",
    "flv":"Videos",

    #Music
    "mp3":"Music",
    "ogg":"Music",
    "wav":"Music",
    "flac":"Music",

    #Program Files
    "py":"Program Files",
    "js":"Program Files",
    "cpp":"Program Files",
    "html":"Program Files",
    "css":"Program Files",
    "c":"Program Files",
    "sh":"Program Files",

    #Documents
    "pdf":"Documents",
    "doc":"Documents",
    "docx":"Documents",
    "txt":"Documents",
    "ppt":"Documents",
    "ods":"Documents",
    "csv":"Documents"
}


#to check if the command-line arguments are exactly 2 
#(name of the script file and the path)
if len(argv)!=2:
    print('='*35)
    print('[ERROR] Invalid no. of arguments were given')
    print(f'[Usage] python {Path(__file__).name} <dir_path>')
    exit(1)

#for taking a path from the user in our script file
path=Path(argv[1])


#Creating destination directory and moving files
for filename in path.iterdir():
    path_to_file=filename.absolute()

    if path_to_file.is_file():
        destination= path / get_dir(filename)

        if not destination.exists():
            destination.mkdir()

        shutil.move(str(path_to_file), str(destination))

print("Files organized successfully!")

