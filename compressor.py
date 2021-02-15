import os
import subprocess

# Parameters for execution
exe = "C:\\Program Files\\7-Zip\\7z.exe"        # 7-Zip executable path
directory = 'test'                              # Directory which will be searched for files to compress
file_extensions = ['.sav', '.3dsav', '.f3sav']  # File extensions that should be compressed


def compress(file):
    """
    Compresses the inputted file into a .7z
    :param file: a string path to the file
    """
    target = file[:file.rfind('.')] + '.7z'
    subprocess.call(exe + " a -t7z " + target + " " + file)


def compress_all(files, target):
    """
    Compresses all of the inputted files into a single .7z
    :param files: an array of string paths to the files
    :param target: path to save directory
    """
    file_str = ""
    for file in files: file_str += file + " "
    subprocess.call(exe + " a -t7z " + target + " " + file_str)



def main():
    """
    Compresses all files with the specified file extensions in the specified
       directory.
    """
    files = os.listdir(directory)
    files = [directory + '/' + file for file in files]
    files_compressable = []

    # Zipping individually
    for file in files:
        # Assert file hasn't been zipped already
        if open(file, 'rb').read(2) != b'7z':
            for extension in file_extensions:
                if extension in file:
                    compress(file)
                    files_compressable.append(file)

    # Zipping collectively
    compress_all(files_compressable, directory + '/testAll.7z')


if __name__ == '__main__':
    main()
