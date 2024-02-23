import asyncio

from PySide6.QtCore import QObject, QRunnable, Signal
from PySide6.QtWidgets import (QApplication, QFileDialog, QFrame, QGridLayout,
                               QMainWindow, QPushButton, QWidget)

import ExcelIcon
import MainWindow
import xl


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    """

    finished = Signal()
    error = Signal(str)
    result = Signal(object)
    progress = Signal(int)


class Worker(QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    """

    def __init__(self, callback_fn, *args, **kwargs):
        super().__init__()


class App_ExcelIcon(QFrame, ExcelIcon.Ui_Form):
    def __init__(self, file_path, row, col, index):
        super().__init__()
        self.setupUi(self)
        self.index = index
        self.file_name = file_path.split("/")[-1]
        self.label_fn.setText(self.file_name)
        self.label_x.hide()

    def enterEvent(self, event):
        self.label_icon.setEnabled(False)
        self.label_x.show()

    def leaveEvent(self, event):
        self.label_icon.setEnabled(True)
        self.label_x.hide()

    def mousePressEvent(self, event) -> None:
        window.delete_item(self, self.index)
        return super().mousePressEvent(event)


class App_MainWindow(QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.selected_files = set()
        self.grid_layout = QGridLayout(self.scrollAreaWidgetContents)
        self.btn_open_files.clicked.connect(self.open)
        self.btn_find_duplicates.clicked.connect(self.find_duplicates)
        self.require_duplicate_origin = False
        self.require_save = False
        self.switch_save_files.stateChanged.connect(
            lambda _: self.__setattr__("require_save", not self.require_save)
        )
        self.switch_find_duplicates.stateChanged.connect(
            lambda _: self.__setattr__(
                "require_duplicate_origin", not self.require_duplicate_origin
            )
        )

    def add_item(self, item_path, index):
        if item_path not in self.selected_files:
            self.selected_files.add(item_path)
            self.place_item_in_grid(item_path, index)

    def place_item_in_grid(self, item_path, index):
        file_path = item_path
        row = index // 4
        col = index % 4
        index = index
        w = App_ExcelIcon(file_path, row, col, index)
        self.grid_layout.addWidget(w, row, col)

    def open(self):
        file_names = QFileDialog(self).getOpenFileNames(self)
        for fn in file_names[0]:
            self.add_item(fn, index=len(self.selected_files))

    def delete_item(self, widget, index):
        # delete the widget
        w = self.grid_layout.takeAt(index)
        w.widget().deleteLater()
        # fix the widgets that come after the delted one indices
        for i in range(index, self.grid_layout.count()):
            self.grid_layout.itemAt(i).widget().index = i  # type:ignore
        # rearrange grid based on new idices
        self.rearrange_grid(index)

    def rearrange_grid(self, index) -> None:
        # make a list of all the widget that come after the deleted one
        after_widgets = set()
        # take at said widgets but don't delete them, since we want to add again
        for _ in range(index, self.grid_layout.count()):
            w = self.grid_layout.takeAt(index)
            after_widgets.add(w.widget())

        # add collected widgets with updated position, starting at index
        for i, w in enumerate(after_widgets, index):
            self.grid_layout.addWidget(w, i // 4, i % 4)

    async def find_duplicates(self):
        # TODO:
        values = xl.get_files_values(self.selected_files)
        await xl.edit_files_values(
            valuesDict=values,
            files=self.selected_files,
            make_copy=self.require_save,
            show_dup_origin=self.require_duplicate_origin,
            test=False,
        )


app = QApplication([])
window = App_MainWindow()
window.show()
app.exec()
