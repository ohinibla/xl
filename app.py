from PySide6.QtWidgets import (QApplication, QFileDialog, QFrame, QMainWindow,
                               QWidget)

import ExcelIcon
import MainWindow


class App_ExcelIcon(QFrame, ExcelIcon.Ui_frame_icon):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)


class App_MainWindow(QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.btn_open_files.clicked.connect(self.open)
        self.btn_find_duplicates.clicked.connect(self.find_duplicates)
        self.xs = App_ExcelIcon(self.scroll_file_list)

    def open(self):
        file_names = QFileDialog(self).getOpenFileNames(self)
        # TODO:
        # open_files_xl(file_names)
        pass

    def find_duplicates(self):
        # TODO:
        # find_duplicates_xl()
        pass


app = QApplication([])
window = App_MainWindow()
window.show()
app.exec()
