from PySide2.QtWidgets import *
from PySide2.QtGui import *
from functools import partial
from Compressor_Thread import Compressor


class Window(QDialog):
    """
    Qt Window to display GUI
    """

    def __init__(self):
        """
        Creates and displays the window
        """
        super(Window, self).__init__()
        self.compressor = Compressor()  # Compressor thread to be run in the background during compression
        self.delete = False             # Whether to delete files
        self.add_extension = False      # Whether to add file extension to zip
        self.directory = ""             # The directory to be compressed

        self.progress_bar = QProgressBar()  # Progress bar to indicate compression progress
        self.file_label = QLabel('File: None')  # Label for which file is selected
        self.compress_button = QPushButton('Compress')  # Button to start compressing

        self.__initialize_gui()

        # Connect compressor's signals
        self.compressor.progress.connect(self.progress_bar.setValue)
        self.compressor.finished.connect(self.compression_finished)

    def __initialize_gui(self):
        # Initialize window
        self.setWindowFlags(self.windowFlags() | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint, )
        self.setWindowTitle("File Compressor")

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
        self.file_label.setStyleSheet(style_sheet)
        self.progress_bar.hide()  # Hide progress bar until compressing begins

        # Creating delete checkbox
        delete_box = QCheckBox("Delete Initial Files after Compression")
        delete_box.setStyleSheet(style_sheet)
        delete_box.stateChanged.connect(partial(self.checkbox_changed, "delete"))

        # Creating add-extension checkbox
        extension_box = QCheckBox("Add Initial File Extension to Compressed Name")
        extension_box.setStyleSheet(style_sheet)
        extension_box.stateChanged.connect(partial(self.checkbox_changed, "extension"))

        # Add widgets to right layout
        right_layout.addWidget(self.file_label)
        right_layout.addSpacing(int(minor_spacing * .6))
        right_layout.addWidget(extension_box)
        right_layout.addWidget(self.progress_bar)
        right_layout.addStretch(1)
        right_layout.setSpacing(int(minor_spacing * 2.2))

        # Create left layout

        # Create select-directory button
        input_button = QPushButton('Select Directory')
        input_button.setStyleSheet(style_sheet)
        input_button.setFixedWidth(button_width)
        input_button.clicked.connect(self.get_dir)

        # Create compress button
        self.compress_button.setStyleSheet(style_sheet)
        self.compress_button.clicked.connect(self.begin_compression)

        # Add widgets to left layout
        left_layout.addWidget(input_button)
        left_layout.addWidget(delete_box)
        left_layout.addWidget(self.compress_button)
        left_layout.addStretch(1)
        left_layout.setSpacing(major_spacing)

        # Create window layout
        window_layout.addLayout(left_layout)
        window_layout.addLayout(right_layout)
        window_layout.addStretch(1)
        window_layout.setSpacing(major_spacing)

        self.setLayout(window_layout)
        self.showMinimized()
        
    def compression_finished(self):
        # Write log
        log = self.compressor.get_log()
        failed_files = {}
        success_files = {}
        for e in log:
            if log[e] != 'success':
                failed_files[e] = log[e]
            else:
                success_files[e] = log[e]

        with open(f"{self.directory}/log.txt", 'w') as f:
            f.write(f"Successfully wrote {len(success_files)} files.\n")
            f.write(f"Failed to write {len(failed_files)} files.\n")

            f.write(f"\nFailed files:\n\n")
            for k, v in failed_files.items():
                f.write(f"File: {k}\nError cause: {v}\n")

            f.write(f"\nSuccessful Files:\n\n")
            for k, v in success_files.items():
                f.write(f"File: {k}\n")

        # Display resulting message box
        self.compress_button.setText("Compress")
        self.setEnabled(True)
        self.progress_bar.hide()
        self.progress_bar.setValue(0)

        msg = QMessageBox()
        msg.setWindowTitle("Compression Completed")
        msg.setText(f"Compression complete.\nSuccessfully wrote {len(success_files)} files.\n" +
                    f"Failed to write {len(failed_files)} files.\n" +
                    f"Compression log can be found at {self.directory}/log.txt")
        msg.exec_()

        self.compressor.log = {}  # Reset compressor's log for multiple execution

    def checkbox_changed(self, checkbox, state):
        """
        Event handler for all QCheckboxes
        :param state:  The state of the changed QCheckbox
        :param checkbox: A string used to indicate which checkbox has been changed
        """
        is_checked = state == Qt.Checked
        if checkbox == 'delete':
            self.delete = is_checked
        if checkbox == 'extension':
            self.add_extension = is_checked

    def get_dir(self):
        """
        Opens a dialog box to get the user's desired directory.
        Sets the file_label's text to indicate the selected directory
        """
        file_name = QFileDialog.getExistingDirectory(self, "Select Directory", "/")
        if file_name != '': self.file_label.setText(f"File: {file_name}")

    def begin_compression(self):
        """
        Compresses all of the files in the currently selected directory.
        If no directory is selected, indicates to the user that they must select a directory.
        """
        self.directory = self.file_label.text()[6:]

        # Ensure a directory has been selected
        if self.directory == "None":
            msg = QMessageBox()
            msg.setWindowTitle("Input Invalid")
            msg.setText("Select a directory before compressing.")
            msg.exec_()
            return

        # Set GUI elements to indicate compression is occuring
        self.compress_button.setText("Compressing...")
        self.setDisabled(True)
        self.progress_bar.show()

        # Update thread variables and start thread
        self.compressor.directory = self.directory
        self.compressor.delete = self.delete
        self.compressor.add_extension = self.add_extension
        self.compressor.start()


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
