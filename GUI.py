from tkinter import Tk
from tkinter import Button, Entry, Radiobutton, Frame, Label, Spinbox, Listbox
from tkinter import StringVar, messagebox

from functions import write_to_db
from functions import get_from_db
from functions import get_json_data
from functions import set_json_data

SETTINGS_PATH = "settings.json"
settings = get_json_data(SETTINGS_PATH)

DEFAULT_PADDING = {'x':10,'y':10}
OWNERS = settings['owners']

BACKGROUND_COLOR = settings["background_color"]
BUTTON_COLOR = settings["button_color"]

def show_warning(title,msg): messagebox.showwarning(title, msg, icon="warning")
def show_info(title, msg): messagebox.showinfo(title, msg, type="ok", icon="info")

class MainGUI:
    def __init__(self): 
        self.root = Tk()
        self._config()
        self._init_widgets()
        self._grid()

    def _config(self):
        self.root.title("Doink Manager")
        #self.root.geometry("200x50")
        self.root.resizable(False, False)

    def _init_widgets(self):
        # ROW 1
        self.row1 = Frame(self.root, bg=BACKGROUND_COLOR)
        self.user_selection_spinbox = Spinbox(self.row1, values=OWNERS, state="readonly")
        self.view_db_button = Button(self.row1, bg=BUTTON_COLOR,text="View data for user: ", command=self.view_db)
        self.add_doink_button = Button(self.row1, bg=BUTTON_COLOR, text="Add a doink", command=self.open_dialog)
        self.settings_button = Button(self.row1, bg=BUTTON_COLOR, text="Settings",command=self.view_settings)
        self.quit_button = Button(self.row1, bg=BUTTON_COLOR, text="Exit", command=self.root.destroy)

    def _grid(self):
        # ROW 0
        self.user_selection_spinbox.grid(column=1, row=0, padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING["y"])
        self.view_db_button.grid(column=0, row=0, padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING["y"])
        # ROW 1
        self.add_doink_button.grid(column=0, row=1, sticky="EW", padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING["y"], columnspan=2)
        # ROW 2
        self.settings_button.grid(column=0, row=2, sticky="EW", padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING["y"])
        self.quit_button.grid(column=1,row=2, sticky="EW", padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING["y"])
        self.row1.grid()
        
    def open_dialog(self):
        AddEntry_dialog = AddEntry()
        AddEntry_dialog.run()

    def view_db(self):
        '''Shows a window containing the amount of doinks that have been smoked by each user'''
        db_window = UserDataWindow(owner=self.user_selection_spinbox.get())
        db_window.run()

    def view_settings(self):
        settings_window = SettingsWindow()
        settings_window.run()

    def run(self): self.root.mainloop()

class AddEntry:
    def __init__(self): 
        self.root = Tk()
        self._config()
        self._init_widgets()
        self._grid()

    def _config(self):
        self.root.title("Add a sesh")
        #self.root.geometry("200x200")
        self.root.resizable(False, False)

    def _init_widgets(self):
        # ROW 0
        self.row0 = Frame(self.root)
        self.owner_selection_spinbox = Spinbox(self.row0, values=OWNERS, state="readonly")
        # ROW 1
        self.row1 = Frame(self.root)
        self.entry_type = StringVar(self.row1, value="doink")
        self.doink_radio_button = Radiobutton(self.row1, text="Doink", variable=self.entry_type, value="doink")
        self.bowl_radio_button = Radiobutton(self.row1, text="Bowl", variable=self.entry_type, value="bowl")
        # ROW 2
        self.row2 = Frame(self.root)
        self.cigs_label = Label(self.row2, text="Smokes:")
        self.cigs_entry = Entry(self.row2)
        # ROW 3
        self.row3 = Frame(self.root)
        self.grams_label = Label(self.row3, text="Grams:")
        self.grams_entry = Entry(self.row3)
        # ROW 4
        self.row4 = Frame(self.root)
        self.add_button = Button(self.row4, text="Add", command=self.add_entry)

    def _grid(self):
        # ROW 0
        self.owner_selection_spinbox.pack()
        # ROW 1
        self.doink_radio_button.pack(side="left")
        self.bowl_radio_button.pack(side="right")
        # ROW 2
        self.cigs_label.pack(side="left")
        self.cigs_entry.pack(side="right")
        # ROW 3
        self.grams_label.pack(side="left")
        self.grams_entry.pack(side="right")
        # ROW 4
        self.add_button.pack(fill="both")
        # FRAMES
        self.row0.pack()
        self.row1.pack()
        self.row2.pack()
        self.row3.pack()
        self.row4.pack()

    def add_entry(self):
        try: write_to_db(type=self.entry_type.get(), owner=self.owner_selection_spinbox.get(),smokes=self.cigs_entry.get(), grams=self.grams_entry.get())
        except Exception as e: show_warning("Error!","Couldn't add doink/bowl :(")
        else: show_info("%s added!"%self.entry_type.get(), "%s added for user %s"%(self.entry_type.get(), self.owner_selection_spinbox.get()))
        finally: self.root.destroy()

    def run(self): self.root.mainloop()

class AddUserDialog:
    def __init__(self): 
        self.root = Tk()
        self._config()
        self._init_widgets()
        self._grid()

    def _config(self):
        self.root.title("Add user")
        self.root.resizable(False, False)

    def _init_widgets(self):
        self.username_label = Label(self.root, text="User name:")
        self.username_entry = Entry(self.root)
        self.submit_button = Button(self.root, text="Confirm", command=self.submit)

    def _grid(self):
        self.username_label.grid(column=0, row=0)
        self.username_entry.grid(column=1, row=0)
        self.submit_button.grid(column=0, row=1, columnspan=2)

    def submit(self): return self.username_entry.get()
    def run(self): self.root.mainloop()

class SettingsWindow:
    def __init__(self):
        self.root = Tk()
        self.settings = self._get_settings()
        self._config()
        self._init_widgets()
        self._grid()

    def _config(self):
        self.root.title("Settings")
        self.root.resizable(False, False)

    def _init_widgets(self):
        # column 1
        self.column1 = Frame(self.root)
        self.bg_color_label = Label(self.column1, text="Background color:")
        self.bg_color_selection = StringVar(self.column1, value=self.settings['background_color'])
        self.bg_color_darkgrey = Radiobutton(self.column1, text="Grey",variable=self.bg_color_selection, value="darkgrey")
        self.bg_color_darkred = Radiobutton(self.column1, text="Red",variable=self.bg_color_selection,value="darkred")
        # column 1 2nd row
        self.btn_color_label = Label(self.column1, text="Button color:")
        self.btn_color_selection = StringVar(self.column1, value=self.settings['button_color'])
        self.btn_color_darkblue = Radiobutton(self.column1, text="Dark blue",variable=self.btn_color_selection, value="darkblue")
        self.btn_color_lightblue = Radiobutton(self.column1, text="Light blue",variable=self.btn_color_selection, value="lightblue")
        # column 2
        self.column2 = Frame(self.root)
        self.users_label = Label(self.column2, text="Users:")

        self.users_list = Listbox(self.column2)
        self.users_list.insert("end", *self.settings['owners'])

        self.delete_user_button = Button(self.column2, text="Delete", command=self.remove_user)
        self.add_user_button = Button(self.column2, text="Add", command=self.add_user)

        # Bottom
        self.apply_button = Button(self.root, text="Apply settings", command=self._set_settings)

    def _grid(self):
        # column 1
        self.bg_color_label.grid(sticky="W")
        self.bg_color_darkgrey.grid()
        self.bg_color_darkred.grid()

        self.btn_color_label.grid(sticky="W")
        self.btn_color_darkblue.grid()
        self.btn_color_lightblue.grid()
        # column 2
        self.users_label.grid(column=0, row=0, columnspan=2)
        self.users_list.grid(column=0, row=1, columnspan=2, padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING["y"])
        self.delete_user_button.grid(column=0, row=2, sticky="EW", padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING["y"])
        self.add_user_button.grid(column=1, row=2, sticky="EW", padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING["y"])
        # self.root
        self.column1.grid(column=0, row=0)
        self.column2.grid(column=1, row=0)
        self.apply_button.grid(column=0, row=1, columnspan=2, padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING["y"])
        
    def _get_settings(self): return get_json_data(SETTINGS_PATH)
    def _set_settings(self):
        self.settings['background_color'] = self.bg_color_selection.get()
        self.settings['button_color'] = self.btn_color_selection.get()

        users = []
        for i in range(self.users_list.size()): users.append(self.users_list.get(i))
        self.settings['owners'] = users

        set_json_data(SETTINGS_PATH, self.settings)
        self.root.destroy()

    def remove_user(self): self.users_list.delete(self.users_list.curselection())
    def add_user(self):
        users = self.settings['owners']
        #users.append(AddUserDialog())
        self.settings['owners'] = users
        
    def run(self): self.root.mainloop()

class UserDataWindow:
    def __init__(self, owner: str):
        self.root = Tk()
        self.owner = owner # Defines which users data to grab
        try: self.data = get_from_db(self.owner)
        except:
            show_warning("Oops!","No data found for user %s"%self.owner)
            self.root.destroy()
            del self
            return
        self._config()
        self._init_widgets()
        self._grid()

    def _config(self):
        self.root.title(self.owner)
        self.root.resizable(False, False)

    def _init_widgets(self):
        # COLUMN 1
        self.col1 = Frame(self.root)
        self.data_entry_frames = []

        for no,v in enumerate(self.data):
            bg_color: str
            # Shifts between dark and light grey for each data entry for easier viewing
            if no % 2 == 0: bg_color = "grey"
            else: bg_color = "darkgrey"

            frame = Frame(self.root, bg=bg_color)

            date_label = Label(frame, text=v['date'], bg=bg_color)

            data_text = f"{v['type']} - Smokes: {v['smokes']} - Grams: {v['grams']}"
            data_label = Label(frame, text=data_text, bg=bg_color)

            self.data_entry_frames.append((date_label,data_label,frame))

    def _grid(self):
        for i,v in enumerate(self.data_entry_frames):
            try:
                # date label
                v[0].grid(column=0,row=0, sticky="W", padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING["y"])
                # data label
                v[1].grid(column=0, row=1, sticky="W", padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING["y"])
                # frame containing both labels
                v[2].grid(column=0, row=i, sticky="EW")
            except: print("couldn't grid")

        self.col1.grid()

    def run(self): self.root.mainloop()