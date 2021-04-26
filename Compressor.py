from zipfile import ZipFile, BadZipFile, LargeZipFile, ZIP_DEFLATED
from PySide2.QtCore import Signal, QThread
import os

file_extensions = ['.sav', '.3dsav', '.f3sav']  # File extensions that should be compressed


class Compressor(QThread):

    progress = Signal(int)   # Progress signal; emits [0, 100] %
    finished = Signal(bool)  # Emits when finished

    def __init__(self, *args, **kwargs):
        QThread.__init__(self, *args, **kwargs)
        self.directory = None         # Directory to be compressed
        self.delete = False           # Whether to delete initial files
        self.add_extension = False    # Whether to add file extensions

        self.log = {}        # Log of compression
        self.processed = 0   # Number of files processed
        self.file_count = 0  # Total number of files to process

    def run(self):
        self.compress_dir(self.directory)
        self.finished.emit(True)

    def compress(self, file):
        # Add file extension if desired
        if self.add_extension: target = file + '.zip'
        else: target = file[:file.rfind('.')] + '.zip'
        try:
            # Try to write file contents to zip
            with ZipFile(target, 'w', ZIP_DEFLATED) as zip:
                zip.write(file, file[file.rfind('/') + 1:])
            if self.delete: os.remove(file)
            self.log[file] = 'success'
        # Log error if error occurs
        except BadZipFile as e:
            self.log[file] = f"BadZipFile Error: {e}"
        except LargeZipFile as e:
            self.log[file] = f"LargeZipFile Error: {e}"
        except:
            self.log[file] = "unexpected_error"

    def compress_dir(self, directory):
        # Get files & their count
        files = os.listdir(directory)
        files = [os.path.join(directory, file) for file in files]
        self.file_count += len(files)

        # Iterate through files
        for file in files:
            # Recurse if file is a directory
            if os.path.isdir(file):
                self.compress_dir(file)

            # Check whether file should be compressed
            file_extension = os.path.splitext(file)[1]
            if file_extension in file_extensions:
                self.compress(file)

            self.processed += 1
            self.progress.emit(int(100 * self.processed / self.file_count))

    def get_log(self):
        return self.log

