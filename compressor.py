import os
import subprocess

# Parameters for execution
exe = "C:\\Program Files\\7-Zip\\7z.exe"        # 7-Zip executable path
directory = 'test'                              # Directory which will be searched for files to compress
file_extensions = ['.sav', '.3dsav', '.f3sav']  # File extensions that should be compressed
delete = True                                   # Whether to delete files after


def compress(file):
    """
    Compresses the inputted file into a .7z
    :param file: a string path to the file
    """
    target = file[:file.rfind('.')] + '.7z'
    subprocess.call(f'"{exe}" a {"-sdel" if delete else ""} -tzip "{target}" "{file}"')


def compress_dir(directory):
    """
    Recursively compresses all of the specified files in the inputted directory
    :param directory: dir to be compressed
    """
    files = os.listdir(directory)
    files = [directory + '/' + file for file in files]
    files_compressable = []

    # Zipping individually
    for file in files:
        # Recurse if file is a directory
        if os.path.isdir(f"{directory}/{file}"):
            compress_dir(f"{directory}/{file}")
        # Check whether file should be compressed
        for extension in file_extensions:
            if extension in file:
                compress(file)
                files_compressable.append(file)


def main():
    """
    Compresses all files with the specified file extensions in the specified
       directory.
    """
    compress_dir(directory)


if __name__ == '__main__':
    main()
