import asyncio
import os
import sys
from pathlib import Path
from typing import Callable

import customtkinter as ctk
import tk_async_execute as tae
from PIL import Image, ImageTk

import xl

ctk.set_appearance_mode("dark")


# NOTE: For packaging assets in pyinstaller with --one-file option, Just add this search function:
# Then use this function to find the asset, eg: resource("my_file")
def resource(relative_path):
    base_path = getattr(
        sys,
        "_MEIPASS",
        os.path.dirname(os.path.abspath(__file__)),
    )
    return os.path.join(base_path, relative_path)


class Utility:
    """
    A class for containing several used variables

    Methods:
        - __init__(self) -> class must be instantiated or tkinter complains about using font class without root(?)

    Subclasses:
        - COLOR
        - PATH

    """

    def __init__(self) -> None:
        self.font = ctk.CTkFont(family="Helvetica", size=14, weight="bold")
        self.bigger_font = ctk.CTkFont(
            family="Helvetica", size=18, weight="bold")

    # colors
    class COLOR:
        BLUE = "#007BFF"
        RED = "#DC3545"
        FRAME_BG = "#333333"
        FRAME_FG = "#2B2B2B"
        FRAME_HIGHLIGHT = "#404040"
        FRAME_HIGHLIGHT_HOVER = "#595959"

    class Path:
        CWD = Path(".")
        EXCEL_ICON_PATH = resource(os.path.join("icons", "xls-file.png"))
        CLOSE_ICON_PATH = resource(os.path.join("icons", "red2.png"))


# ------ Main Window class ----------------------------------------------
class App(ctk.CTk):
    """
    Main Customtkinter class containing all the child windows classes
    and program logic callbacks
    Main window geometry is:

    ( * * )
    ( * * )

    Methods:
        - __init__(self)
        - open_files(self)
        - find_duplicates(self)
        - get_selected_files(self)
        - find_duplicates_callback
        - delete_item(self, item: str)
        - progress_handler(self)
    """

    def __init__(self) -> None:
        super().__init__()

        # ------ Variables -----------------
        self.selected_files: set = set()
        self.is_saved = ctk.BooleanVar(value=False)
        self.show_dup_origin = ctk.BooleanVar(value=False)

        # ------ General settings ----------
        self.title("Excel Duplicates")
        self.geometry("1000x500")
        self.resizable(False, False)

        # ------ Grid ----------------------
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1, minsize=450)
        self.grid_rowconfigure(1, weight=1, minsize=50)

        # ------ Frames --------------------
        self.mainbar_frame = MainbarFrame(
            self,
            open_file_callback=self.open_files,
            delete_file_callback=self.delete_item,
        )
        self.mainbar_frame.grid(
            row=0,
            column=1,
            padx=(0, 30),
            sticky="news",
        )

        self.sidebar_frame = SidebarFrame(
            self,
            find_duplicates_callback=self.find_duplicates_callback_func,
            is_saved=self.is_saved,
            show_dup_origin=self.show_dup_origin,
        )
        self.sidebar_frame.grid(
            row=0,
            column=0,
            padx=20,
            sticky="news",
        )

        self.progressbar = Progress(
            self,
            determinate_speed=1,
            mode="determinate",
            height=25,
            corner_radius=0,
            progress_color=Utility.COLOR.FRAME_FG,
        )
        self.progressbar.set(0)

    # ------ Callbacks ------------------
    def open_files(self) -> None:
        """
        Open files with a file open modal and add their paths to selected_files
        and add their icon the list_frame window
        """
        self.progressbar.grid_forget()
        file_names = ctk.filedialog.askopenfilenames(
            filetypes=(
                ("Excel files", "*.xlsx"),
                ("Excel files", "*.xls"),
                ("Excel files", "*.xlsm"),
                ("Excel files", "*.xltx"),
                ("Excel files", "*.xltm"),
            )
        )
        for fn in file_names:
            if fn not in self.selected_files:
                self.selected_files.add(fn)

                self.mainbar_frame.list_frame.add_item(
                    fn,
                    index=len(self.selected_files),
                )

    def get_selected_files(self) -> set:
        return self.selected_files

    async def find_duplicates(self) -> None:
        """
        Main functionality of the program, get duplicates and save appropriately with selected files
        """
        self.progressbar.set(0)
        _s = self.get_selected_files()
        if _s:
            try:
                self.progressbar.update_text_and_show(
                    text="Loading",
                    color="white",
                )
                all_values = xl.get_files_values(_s)
                await xl.edit_files_values(
                    valuesDict=all_values,
                    files=_s,
                    make_copy=self.is_saved.get(),
                    show_dup_origin=self.show_dup_origin.get(),
                    test=False,
                )
                await self.progress_handler()
                self.progressbar.update_text_and_show(
                    text="Done", color="#94D095")
                self.progressbar.configure(progress_color="#293C17")

            # TODO: change these
            except Exception as e:
                self.progressbar.update_text_and_show(
                    text=f"ERROR: {e}",
                    color=Utility.COLOR.RED,
                )
        else:
            self.progressbar.update_text_and_show(
                text="ERROR: No files selected",
                color=Utility.COLOR.RED,
            )

    def find_duplicates_callback_func(self) -> None:
        """
        Callback function for tkinter-async package
        """
        tae.async_execute(self.find_duplicates(), visible=False)

    def delete_item(self, item: str) -> None:
        self.selected_files.remove(item)

    # ------ Utilities -----
    async def progress_handler(self) -> None:
        """
        Asynchronously progress the progressbar value.
        """
        for i, fn in enumerate(self.selected_files, start=1):
            self.progressbar.set(i * (1 / len(self.selected_files)))
            self.progressbar.update_text_and_show(
                text=fn.split("/")[-1],
                color="white",
            )
            await asyncio.sleep(0)


# ------ Sub Windows ----------------------------------------------------
class MainbarFrame(ctk.CTkFrame):
    """
    Mainbar frame of the application that contains buttons and switches.

    Mainbar window geometry is:

    ( * )
    ( * )

    Attributes:
        - open_file_callback: callable
        - delete_file_callback: callable

    Methods:
        - __init__(self, open_file_callback: callable, delete_file_callback: callable)
    """

    def __init__(
        self,
        *args,
        open_file_callback: Callable,
        delete_file_callback: Callable,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)

        self.open_frame = OpenFileFrame(self, open_file=open_file_callback)
        self.open_frame.grid(
            column=0,
            row=0,
            padx=30,
            pady=(20, 0),
            sticky="new",
        )

        self.list_frame = FileListFrame(self, delete_item=delete_file_callback)
        self.list_frame.grid(
            column=0,
            row=1,
            padx=30,
            pady=20,
            sticky="news",
        )


class OpenFileFrame(ctk.CTkFrame):
    """
    fileopening frame of the application that contains a simple button and a placeholder entry

    openfile window geometry is:

    ( * * )

    Attributes:
        - open_file: callable -> (to be passed to button from upperclass)

    Methods:
        - __init__(self, open_files: callable)
    """

    def __init__(self, *args, open_file: Callable, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.configure(fg_color="transparent")

        self.entry = ctk.CTkEntry(
            self,
            state="disabled",
            border_width=0,
            fg_color="gray88",
            corner_radius=0,
        )
        self.entry.grid(
            row=0,
            column=0,
            sticky="ew",
        )

        self.open_button = ctk.CTkButton(
            self,
            text="open",
            width=70,
            command=open_file,
            border_width=0,
            fg_color=Utility.COLOR.BLUE,
            corner_radius=0,
            font=Utility().font,
        )
        self.open_button.grid(row=0, column=1, sticky="w")


class FileListFrame(ctk.CTkScrollableFrame):
    """
    filelist frame of the application that contains a simple button
    and a placeholder entry this frame handles placing, deleting,
    rearranging and deleting the icons of the selected files with
    a helper function of recoloring scrollbar of the scrollable frame
    when there are not many selected files

    file list frame geometry is:

    ( * * * * )
    ( . . . . )
    ( . . . . )
    ( . . . . )

    Attributes:
        - delete_item: callable

    Methods:
        - __init__(self, open_files: callable) -> None
        - place_item(self, item: str, index: int) -> None
        - add_item(self, item_path: str, index: int) -> None
        - rearrange_items(self, index: int) -> None
        - delete_item(self, item_path: str, index: int) -> None
        - recolor_scrollbar(self) -> None
    """

    def __init__(self, *args, delete_item: Callable, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        # self.grid_rowconfigure(0, weight=1)

        self.configure(scrollbar_button_color=Utility.COLOR.FRAME_BG)
        self.configure(scrollbar_button_hover_color=Utility.COLOR.FRAME_BG)

        self.delete_item_main = delete_item
        self.items = set()
        self.items_widgets = dict()

    def place_item(self, item: str, index: int) -> None:
        last_item_num = len(self.items) - 1
        clean_name = item.split("/")[-1][0:8]
        icon = ExcelIconFrame(
            self,
            item_name=clean_name,
            item_path=item,
            delete_upclass=self.delete_item,
            index=index,
        )
        icon.grid(
            row=last_item_num // 4,
            column=last_item_num % 4,
            padx=10,
            pady=10,
        )
        self.items_widgets[index] = icon

    def add_item(self, item_path: str, index: int) -> None:
        if item_path not in self.items:
            self.items.add(item_path)
            self.place_item(item_path, index)
        self.recolor_scrollbar()

    def rearrange_items(self, index: int) -> None:
        """
        Rearrange icons in the grid when an icon gets removed.
        """
        new = dict()
        for i, w in self.items_widgets.items():
            if i > index:
                w.index -= 1
                new[i - 1] = w
            else:
                new[i] = w

        self.items_widgets = new
        for i, w in self.items_widgets.items():
            if i >= index:
                w.grid(
                    row=(w.index - 1) // 4,
                    column=(w.index - 1) % 4,
                    padx=10,
                    pady=10,
                )

    def delete_item(self, item_path: str, index: int) -> None:
        self.items.remove(item_path)
        del self.items_widgets[index]
        self.delete_item_main(item_path)
        self.recolor_scrollbar()
        self.rearrange_items(index)

    # TODO: rewrite better
    def recolor_scrollbar(self) -> None:
        """
        recolor scrollbar so the scrollbar is hidden when not needed
        """
        if len(self.items) > 16:
            self.configure(
                scrollbar_button_color=Utility.COLOR.FRAME_HIGHLIGHT,
            )
            self.configure(
                scrollbar_button_hover_color=Utility.COLOR.FRAME_HIGHLIGHT_HOVER
            )
        else:
            self.configure(scrollbar_button_color=Utility.COLOR.FRAME_BG)
            self.configure(scrollbar_button_hover_color=Utility.COLOR.FRAME_BG)


class ExcelIconFrame(ctk.CTkFrame):
    """
    A frame for a canvas for icon of the excel file and a label for their filename

    excel icon frame geometry is (pack):

    ( * )
    ( * )

    Attributes:
        - item_name: str
        - item_path: str
        - delete_upclass: callable
        - index: int

    Methods:
        - __init__(self) -> None
        - _delete(self) -> None
    """

    def __init__(
        self,
        *args,
        item_name: str,
        item_path: str,
        delete_upclass: Callable,
        index: int,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.configure(fg_color="transparent")

        self.item_name = item_name
        self.item_path = item_path
        self.delete_upclass = delete_upclass
        self.index = index

        self.icon_canvas = ExcelIcon(
            self,
            width=100,
            height=100,
            bd=0,
            highlightthickness=0,
            relief="ridge",
            delete_event_handler=self._delete,
        )

        self.name_label = ctk.CTkLabel(
            self,
            text=self.item_name,
            font=Utility().font,
        )

        self.icon_canvas.pack()
        self.name_label.pack()

    def _delete(self) -> None:
        """
        Function that propagate deleting fucionality to upper classes since the main logic
        is handled in the main window
        """
        self.delete_upclass(item_path=self.item_path, index=self.index)
        self.destroy()


class ExcelIcon(ctk.CTkCanvas):
    """
    A canvas for making excel icon with a red X icon for exit
    and appropriate methods for handling mouse events.

    excel icon frame geometry is (pack):

    ( * )
    ( * )
    ( * )

    Attributes:
        - delete_event_handler: callable

    Methods:
        - __init__(self) -> None
        - enter(self, evnet) -> None
        - leave(self, evnet) -> None
        - _delete(self, evnet) -> None
        - enter_with_cursor(self, evnet) -> None
        - leave_with_cursor(self, evnet) -> None
    """

    def __init__(self, *args, delete_event_handler: Callable, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.configure(bg=Utility.COLOR.FRAME_BG)
        self.configure(bd=0)
        self.delete_event_handler = delete_event_handler

        self._icon = Image.open(Utility.Path.EXCEL_ICON_PATH).resize(
            (100, 100),
        )
        self._icon = ImageTk.PhotoImage(self._icon)
        self.icon = self.create_image(0, 0, image=self._icon, anchor="nw")

        self._redx = Image.open(Utility.Path.CLOSE_ICON_PATH).resize((30, 30))
        self._redx = ImageTk.PhotoImage(self._redx)
        self.redx = self.create_image(
            100, 0, image=self._redx, anchor="ne", state=ctk.HIDDEN
        )

        self.tag_bind(self.icon, "<Enter>", self.enter)
        self.tag_bind(self.icon, "<Leave>", self.leave)

        # WARNING: events have to be repeated on redx also, because mouse entering redx also registers as leaving the icon.
        self.tag_bind(self.redx, "<Enter>", self.enter_with_cursor)
        self.tag_bind(self.redx, "<Leave>", self.leave_with_cursor)
        self.tag_bind(self.redx, "<Button-1>", self._delete)

    def enter(self, event) -> None:
        self.itemconfig(self.redx, state=ctk.NORMAL)

    def leave(self, event) -> None:
        self.itemconfig(self.redx, state=ctk.HIDDEN)

    def _delete(self, event) -> None:
        self.delete_event_handler()

    # BUG: change the cursor to hand only when on redx shape (causes freeze)
    def enter_with_cursor(self, event) -> None:
        self.itemconfig(self.redx, state=ctk.NORMAL)
        self.configure(cursor="hand2")

    def leave_with_cursor(self, event) -> None:
        self.itemconfig(self.redx, state=ctk.HIDDEN)
        self.configure(cursor="")


class SidebarFrame(ctk.CTkFrame):
    """
    Sidebar frame of the application containing buttons and switches
    however main logic of the application is handled in the main frame class so
    the methods actually direct the events input from the user to upper classes

    excel icon frame geometry is (pack):

    ( * )
    ( . )
    ( . )
    ( . )

    Attributes:
        - delete_event_handler: callable
        - show_dup_origin: callable
        - find_duplicates_callback: callable
        - is_saved: bool

    Methods:
        - __init__(
                   self,
                   show_dup_origin: bool,
                   find_duplicates_callback: callable,
                   is_saved: callable,
                   )
    """

    def __init__(
        self,
        *args,
        show_dup_origin: ctk.BooleanVar,
        find_duplicates_callback: Callable,
        is_saved: ctk.BooleanVar,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.is_saved = is_saved

        self.bg_frame = ctk.CTkFrame(self)

        self.duplicate_button = ctk.CTkButton(
            self,
            text="find duplicates",
            command=find_duplicates_callback,
            fg_color=Utility.COLOR.BLUE,
            corner_radius=0,
            font=Utility().font,
        )

        self.save_files_switch = ReversedSwitch(
            self.bg_frame, text="save files", variable=is_saved
        )

        self.show_duplicate_origin_label = ctk.CTkLabel(
            self.bg_frame, text="show duplicate origin"
        )

        self.show_duplicate_origin = ReversedSwitch(
            self.bg_frame,
            text="show duplicates origin",
            variable=show_dup_origin,
        )

        self.exit_button = ctk.CTkButton(
            self,
            text="Exit",
            fg_color=Utility.COLOR.RED,
            command=self.quit,
            corner_radius=0,
            font=Utility().font,
        )

        self.duplicate_button.pack(padx=20, pady=(20, 50), fill="x")
        self.save_files_switch.pack(
            anchor="w",
            padx=(20, 20),
            pady=10,
            fill="x",
        )
        self.show_duplicate_origin.pack(
            anchor="w",
            padx=(20, 20),
            pady=10,
            fill="x",
        )
        self.bg_frame.pack(fill="x", padx=20)
        self.exit_button.pack(
            padx=20,
            fill="x",
            pady=20,
            side="bottom",
        )


class ReversedSwitch(ctk.CTkSwitch):
    """
    Switch with rounded corners, border, label, command, variable support.
    the main difference is that the label and the canvas is reversed
    """

    def __init__(
        self,
        *args,
        switch_height: int = 30,
        switch_width: int = 50,
        **kwargs,
    ) -> None:
        super().__init__(
            *args,
            switch_height=switch_height,
            switch_width=switch_width,
            **kwargs,
        )

        self._canvas.grid(row=0, column=2, sticky="e")
        self._text_label.grid(row=0, column=0)  # type: ignore
        self._text_label.configure(font=Utility().font)  # type: ignore
        self.configure(font=Utility().font)

        self.grid_columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)


class Progress(ctk.CTkProgressBar):
    """
    Progressbar with rounded corners, border, variable support,
    indeterminate mode, vertical orientation.
    with added methods to update the text and show or hide the
    progressbar when needed
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def update_text_and_show(self, text: str, color: str) -> None:
        self._canvas.delete("text")
        self.text = self._canvas.create_text(
            self.master.winfo_width() / 2,
            18,
            text=text,
            justify="center",
            fill=color,
            font=Utility().bigger_font,
            tags="text",
        )
        self.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="we",
            padx=(20, 30),
        )


if __name__ == "__main__":
    # as to documentation of the tkinter async package
    app = App()
    tae.start()
    app.mainloop()
    tae.stop()
