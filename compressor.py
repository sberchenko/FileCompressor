import os
from zipfile import ZipFile, BadZipFile, LargeZipFile
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from functools import partial

# Parameters for execution
file_extensions = ['.sav', '.3dsav', '.f3sav']  # File extensions that should be compressed


class Window(QDialog):
    """
    Qt Window
    """

    def __init__(self):
        """
        Creates and displays the window
        """
        # Initialize window
        super(Window, self).__init__()
        self.setWindowFlags(self.windowFlags() | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint, )
        self.setWindowTitle("Timesheet Program")

        # GUI Variables
        font_size = 10
        major_spacing = 20
        minor_spacing = 10
        button_width = 150
        style_sheet = f"font-size: {font_size}pt;"

        # Create major layouts
        window_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Create right layout
        file_label = QLabel('File: None')
        file_label.setStyleSheet(style_sheet)

        def checkbox_changed():
            self.delete = delete_box.isChecked()

        delete_box = QCheckBox("Delete Files")
        delete_box.setStyleSheet(style_sheet)
        delete_box.stateChanged.connect(checkbox_changed)

        right_layout.addWidget(file_label)
        right_layout.addStretch(1)
        right_layout.setSpacing(int(minor_spacing*2.2))

        # Create file_buttons
        def clicked():
            file_name = QFileDialog.getExistingDirectory(self, "Select Directory", "/")
            if file_name != '': file_label.setText(f"File: {file_name}")

        input_button = QPushButton('Select Directory')
        input_button.setStyleSheet(style_sheet)
        input_button.setFixedWidth(button_width)
        input_button.clicked.connect(clicked)

        compress_button = QPushButton('Compress')
        compress_button.setStyleSheet(style_sheet)

        def compress_clicked():

            compress_button.setText("Compressing...")
            self.compress_dir(file_label.text()[6:])

            # Write log
            failed_files = {}
            success_files = {}
            for e in self.log:
                if self.log[e] != 'success':
                    failed_files[e] = self.log[e]
                else:
                    success_files[e] = self.log[e]

            with open("log.txt", 'w') as f:
                f.write(f"Successfully wrote {len(success_files)} files.\n")
                f.write(f"Failed to write {len(failed_files)} files.\n")
                f.write(f"\nFailed files:\n\n")
                for k, v in failed_files.items():
                    f.write(f"File: {k}\nError cause: {v}\n")
                f.write(f"\nSuccessful Files:\n\n")
                for k, v in success_files.items():
                    f.write(f"File: {k}\n")

            compress_button.setText("Compress")
            msg = QMessageBox()
            msg.setWindowTitle("Compression Completed")
            msg.setText(f"Compression complete.\nFailed to write {len(failed_files)} files.\n" +
                        f"Compression log can be found at {os.getcwd()}\\log.txt")
            msg.exec_()

        compress_button.clicked.connect(compress_clicked)

        left_layout.addWidget(input_button)
        left_layout.addWidget(delete_box)
        left_layout.addWidget(compress_button)
        left_layout.addStretch(1)
        left_layout.setSpacing(major_spacing)

        # Create window layout
        window_layout.addLayout(left_layout)
        window_layout.addLayout(right_layout)
        window_layout.addStretch(1)
        window_layout.setSpacing(major_spacing)

        self.setLayout(window_layout)
        self.showMinimized()
        self.delete = False
        self.log = {}

    def compress(self, file):
        """
        Compresses the inputted file into a .7z
        :param file: a string path to the file
        """
        target = file[:file.rfind('.')] + '.zip'
        try:
            with ZipFile(target, 'w') as zip: zip.write(file)
            if self.delete: os.remove(file)
            self.log[file] = 'success'
        except BadZipFile as e:
            self.log[file] = e
        except LargeZipFile as e:
            self.log[file] = e
        except:
            self.log[file] = "unexpected_error"

    def compress_dir(self, directory):
        """
        Recursively compresses all of the specified files in the inputted directory
        :param directory: dir to be compressed
        """
        files = os.listdir(directory)
        files = [os.path.join(directory, file) for file in files]

        # Iterate through files
        for file in files:
            # Recurse if file is a directory
            if os.path.isdir(file): self.compress_dir(file)
            # Check whether file should be compressed
            for extension in file_extensions:
                if extension in file:
                    self.compress(file)


def main():
    """
    Compresses all files with the specified file extensions in the specified
       directory.
    """
    app = QApplication()
    main = Window()
    app.exec_()
    main.raise_()
    main.activateWindow()


if __name__ == '__main__':
    main()
