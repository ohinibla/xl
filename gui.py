import asyncio
from pathlib import Path

import customtkinter as ctk
import tk_async_execute as tae
from PIL import Image, ImageTk

import xl

ctk.set_appearance_mode("dark")

# PATHS
CWD = Path(".")
EXCEL_ICON_PATH = CWD / "icons" / "sheet.png"
CLOSE_ICON_PATH = CWD / "icons" / "red2.png"


COLORS = {
    "BLUE": "#007BFF",
    "RED": "#DC3545",
    "FRAME_BG": "#333333",
    "FRAME_FG": "#2B2B2B",
    "FRAME_HIGHLIGHT": "#404040",
    "FRAME_HIGHLIGHT_HOVER": "#595959",
}


# ------ Main Window class ----------------------------------------------
class App(ctk.CTk):
    def __init__(self):
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
        self.mainbar_frame.grid(row=0, column=1, padx=(
            0, 30), pady=10, sticky="news")

        self.sidebar_frame = SidebarFrame(
            self,
            find_duplicates_callback=self.find_duplicates_callback_func,
            is_saved=self.is_saved,
            show_dup_origin=self.show_dup_origin,
        )
        self.sidebar_frame.grid(
            row=0, column=0, padx=20, pady=10, sticky="news")

        self.progressbar = Progress(
            self,
            determinate_speed=1,
            mode="determinate",
            height=25,
            corner_radius=0,
        )
        self.progressbar.set(0)

    # ------ Callbacks ------------------
    def open_files(self):
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

                self.mainbar_frame.list_frame.add_item(fn)

    def get_selected_files(self):
        return self.selected_files

    async def find_duplicates(self):
        self.progressbar.set(0)
        _s = self.get_selected_files()
        if _s:
            try:
                self.progressbar.update_text(text="Loading", color="white")
                self.progressbar.grid(
                    row=1, column=0, columnspan=2, sticky="we", padx=(20, 30)
                )
                all_values = xl.get_files_values(_s)
                await xl.edit_files_values(
                    valuesDict=all_values,
                    files=_s,
                    make_copy=self.is_saved.get(),
                    show_dup_origin=self.show_dup_origin.get(),
                )
                await self.progress_handler()
                self.progressbar.update_text(text="Done", color="#94D095")
                self.progressbar.configure(progress_color="#293C17")

            except Exception as e:
                pass
        else:
            pass

    def find_duplicates_callback_func(self):
        tae.async_execute(self.find_duplicates(), visible=False)

    def delete_item(self, item):
        self.selected_files.remove(item)

    # ------ Utilities -----
    async def progress_handler(self):
        for i, fn in enumerate(self.selected_files, start=1):
            self.progressbar.set(i * (1 / len(self.selected_files)))
            self.progressbar.update_text(text=fn.split("/")[-1], color="white")
            await asyncio.sleep(0)


# ------ Sub Windows ----------------------------------------------------
class MainbarFrame(ctk.CTkFrame):
    def __init__(self, *args, open_file_callback, delete_file_callback, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)

        self.open_frame = OpenFileFrame(self, open_file=open_file_callback)
        self.open_frame.grid(column=0, row=0, padx=30,
                             pady=(20, 0), sticky="nwe")

        self.list_frame = FileListFrame(self, delete_item=delete_file_callback)
        self.list_frame.grid(column=0, row=1, padx=30, pady=20, sticky="news")


class OpenFileFrame(ctk.CTkFrame):
    def __init__(self, *args, open_file, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.configure(fg_color="transparent")

        self.entry = ctk.CTkEntry(
            self, state="disabled", border_width=0, fg_color="gray88", corner_radius=0
        )
        self.entry.grid(row=0, column=0, sticky="ew")

        self.open_button = ctk.CTkButton(
            self,
            text="open",
            width=70,
            command=open_file,
            border_width=0,
            fg_color=COLORS["BLUE"],
            corner_radius=0,
        )
        self.open_button.grid(row=0, column=1, sticky="w")


class FileListFrame(ctk.CTkScrollableFrame):
    def __init__(self, *args, delete_item, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.configure(scrollbar_button_color=COLORS["FRAME_BG"])
        self.configure(scrollbar_button_hover_color=COLORS["FRAME_BG"])

        self.delete_item_main = delete_item
        self.items = set()

    def place_item(self, item):
        last_item_num = len(self.items) - 1
        clean_name = item.split("/")[-1][0:8]
        icon = ExcelIconFrame(
            self, item_name=clean_name, item_path=item, delete_upclass=self.delete_item
        )
        icon.grid(
            row=last_item_num // 4,
            column=last_item_num % 4,
            padx=10,
            pady=10,
        )

    # TODO: rewrite better
    def recolor_scrollbar(self):
        if len(self.items) > 16:
            self.configure(scrollbar_button_color=COLORS["FRAME_HIGHLIGHT"])
            self.configure(
                scrollbar_button_hover_color=COLORS["FRAME_HIGHLIGHT_HOVER"])
        else:
            self.configure(scrollbar_button_color=COLORS["FRAME_BG"])
            self.configure(scrollbar_button_hover_color=COLORS["FRAME_BG"])

    def add_item(self, item_path: str) -> None:
        if item_path not in self.items:
            self.items.add(item_path)
            self.place_item(item_path)
        self.recolor_scrollbar()

    # TODO: Rearrange items after deletion
    def rearrange_items(self):
        pass

    def delete_item(self, item_path):
        self.items.remove(item_path)
        self.delete_item_main(item_path)
        self.recolor_scrollbar()


class ReversedSwitch(ctk.CTkSwitch):
    def __init__(self, *args, switch_height=30, switch_width=50, **kwargs):
        super().__init__(
            *args,
            switch_height=switch_height,
            switch_width=switch_width,
            **kwargs,
        )

        self._canvas.grid(row=0, column=2, sticky="e")
        self._text_label.grid(row=0, column=0)
        self.grid_columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)


class SidebarFrame(ctk.CTkFrame):
    def __init__(
        self, *args, show_dup_origin, find_duplicates_callback, is_saved, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.is_saved = is_saved

        self.bg_frame = ctk.CTkFrame(self)

        self.duplicate_button = ctk.CTkButton(
            self,
            text="find duplicates",
            command=find_duplicates_callback,
            fg_color=COLORS["BLUE"],
            corner_radius=0,
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
            fg_color=COLORS["RED"],
            command=self.quit,
            corner_radius=0,
        )

        self.duplicate_button.pack(padx=20, pady=(20, 50), fill="x")
        self.save_files_switch.pack(
            anchor="w", padx=(20, 20), pady=10, fill="x")
        self.show_duplicate_origin.pack(
            anchor="w", padx=(20, 20), pady=10, fill="x")
        self.bg_frame.pack(fill="x", padx=20)
        self.exit_button.pack(padx=20, fill="x", pady=20, side="bottom")


class ExcelIconFrame(ctk.CTkFrame):
    def __init__(self, *args, item_name, item_path, delete_upclass, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(fg_color="transparent")

        self.item_name = item_name
        self.item_path = item_path
        self.delete_upclass = delete_upclass

        self.icon_canvas = ExcelIcon(
            self,
            width=100,
            height=100,
            bd=0,
            highlightthickness=0,
            relief="ridge",
            delete_event_handler=self._delete,
        )

        self.name_label = ctk.CTkLabel(self, text=self.item_name)

        self.icon_canvas.pack()
        self.name_label.pack()

    def _delete(self):
        self.delete_upclass(item_path=self.item_path)
        self.destroy()


class ExcelIcon(ctk.CTkCanvas):
    def __init__(self, *args, delete_event_handler, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.configure(bg=COLORS["FRAME_BG"])
        self.configure(bd=0)
        self.delete_event_handler = delete_event_handler

        self._icon = Image.open(EXCEL_ICON_PATH).resize((100, 100))
        self._icon = ImageTk.PhotoImage(self._icon)
        self.icon = self.create_image(0, 0, image=self._icon, anchor="nw")

        self._redx = Image.open(CLOSE_ICON_PATH).resize((30, 30))
        self._redx = ImageTk.PhotoImage(self._redx)
        self.redx = self.create_image(
            100, 0, image=self._redx, anchor="ne", state=ctk.HIDDEN
        )

        self.tag_bind(self.icon, "<Enter>", self.enter)
        self.tag_bind(self.icon, "<Leave>", self.leave)

        self.tag_bind(self.redx, "<Enter>", self.enter)
        self.tag_bind(self.redx, "<Leave>", self.leave)
        self.tag_bind(self.redx, "<Button-1>", self._delete)

    def enter(self, event):
        self.itemconfig(self.redx, state=ctk.NORMAL)

    def leave(self, event):
        self.itemconfig(self.redx, state=ctk.HIDDEN)

    def _delete(self, event):
        self.delete_event_handler()


class Progress(ctk.CTkProgressBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.text = self._canvas.create_text(
        #     500,
        #     12,
        #     text="",
        #     fill="white",
        #     font=("Helvetica 10 normal"),
        #     tags="text",
        # )

    def update_text(self, text, color):
        self._canvas.delete("text")
        self.text = self._canvas.create_text(
            500,
            12,
            text=text,
            fill=color,
            font=("Helvetica 10 normal"),
            tags="text",
        )


app = App()
tae.start()
app.mainloop()
tae.stop()
