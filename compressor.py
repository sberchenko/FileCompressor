import os

directory = 'test'
file_extensions = ['.sav', '.3dsav', '.f3sav']


def compress(file):
    print(f"Compressing {file}")


def main():
    files = os.listdir(directory)
    for file in files:
        for extension in file_extensions:
            if extension in file:
                compress(file)


if __name__ == '__main__':
    main()