from tkinter import Tk
from tkinter import Button, Entry, Radiobutton, Frame, Label, Spinbox, Listbox, Checkbutton
from tkinter import StringVar, messagebox
from tkinter import IntVar

from functions import write_to_db
from functions import get_from_db
from functions import get_json_data
from functions import set_json_data

SETTINGS_PATH = "settings.json"
settings = get_json_data(SETTINGS_PATH)

DEFAULT_PADDING = {'x':10,'y':10}
#OWNERS = settings['owners']

BACKGROUND_COLOR = settings["background_color"]
BUTTON_COLOR = settings["button_color"]

def show_warning(title,msg): messagebox.showwarning(title, msg, icon="warning")
def show_info(title, msg): messagebox.showinfo(title, msg, type="ok", icon="info")

class MainGUI:
    def __init__(self): 
        self.root = Tk()
        self.owners = get_json_data(SETTINGS_PATH)['owners']
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
        self.user_selection_spinbox = Spinbox(self.row1, values=self.owners, state="readonly")
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
        self.owners = get_json_data(SETTINGS_PATH)['owners']
        self._config()
        self._init_widgets()
        self._grid()

    def _config(self):
        self.root.title("Add a sesh")
        #self.root.geometry("200x200")
        self.root.resizable(False, False)

    def _init_widgets(self):
        # ROW 0 user selection
        self.main_frame = Frame(self.root, bg=BACKGROUND_COLOR, padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING['y'])
        self.owner_label = Label(self.main_frame, text="User: ", bg=BACKGROUND_COLOR, padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING['y'])
        self.owner_selection_spinbox = Spinbox(self.main_frame, values=self.owners, state="readonly")
        # ROW 1 doink/bowl choice
        self.type_entry_frame = Frame(self.main_frame, bg=BACKGROUND_COLOR, padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING['y'])
        self.entry_type = StringVar(self.type_entry_frame, value="doink")
        self.doink_radio_button = Radiobutton(self.type_entry_frame, text="Doink", variable=self.entry_type, value="doink", bg=BACKGROUND_COLOR, padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING['y'])
        self.bowl_radio_button = Radiobutton(self.type_entry_frame, text="Bowl", variable=self.entry_type, value="bowl", bg=BACKGROUND_COLOR, padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING['y'])
        # ROW 2 ciggy entry
        self.smokes_entry_frame = Frame(self.main_frame, bg=BACKGROUND_COLOR, padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING['y'])
        self.cigs_label = Label(self.smokes_entry_frame, text="Smokes:", bg=BACKGROUND_COLOR, padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING['y'])
        self.cigs_entry = Entry(self.smokes_entry_frame, bg=BACKGROUND_COLOR)
        # ROW 3 gram entry 
        self.gram_entry_frame = Frame(self.main_frame, bg=BACKGROUND_COLOR, padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING['y'])
        self.grams_label = Label(self.gram_entry_frame, text="Grams:", bg=BACKGROUND_COLOR, padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING['y'])
        self.grams_entry = Entry(self.gram_entry_frame, bg=BACKGROUND_COLOR)
        # ROW 4 checkbuttons

        self.filter_check = IntVar(self.main_frame, value=0)
        self.paper_check = IntVar(self.main_frame, value=0)

        self.checkbuttons_frame = Frame(self.main_frame, bg=BACKGROUND_COLOR, padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING['y'])
        self.filter_label = Label(self.checkbuttons_frame, text="Filter: ", bg=BACKGROUND_COLOR, padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING['y'])
        self.filter_checkbutton = Checkbutton(self.checkbuttons_frame,variable=self.filter_check, onvalue=1,offvalue=0,bg=BACKGROUND_COLOR, padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING['y'])
        self.paper_label = Label(self.checkbuttons_frame, text="Paper: ", bg=BACKGROUND_COLOR, padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING['y'])
        self.paper_checkbutton = Checkbutton(self.checkbuttons_frame, variable=self.paper_check, onvalue=1,offvalue=0, bg=BACKGROUND_COLOR, padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING['y'])
        # ROW 5 add button
        self.submit_button_frame = Frame(self.main_frame, bg=BACKGROUND_COLOR, padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING['y'])
        self.add_button = Button(self.submit_button_frame, background=BACKGROUND_COLOR,text="Add", command=self.add_entry)

    def _grid(self):
        # ROW 0
        self.owner_label.grid(column=0,row=0, sticky="W")
        self.owner_selection_spinbox.grid(column= 0, row= 0, sticky="E")
        # ROW 1
        self.doink_radio_button.grid(column= 0, row= 0)
        self.bowl_radio_button.grid(column= 1, row= 0)
        # ROW 2
        self.cigs_label.grid(column= 0, row= 0, sticky="W")
        self.cigs_entry.grid(column= 1, row= 0, sticky="E")
        # ROW 3
        self.grams_label.grid(column= 0, row= 0, sticky="W")
        self.grams_entry.grid(column= 1, row= 0, sticky="E")
        # row 4
        self.filter_label.grid(column=0, row=0, sticky="W")
        self.filter_checkbutton.grid(column= 1, row= 0, sticky="E")

        self.paper_label.grid(column=0, row=1, sticky="W")
        self.paper_checkbutton.grid(column= 1, row= 1, sticky="E")
        # ROW 5
        self.add_button.grid(column= 0, row= 0)
        # FRAMES
        self.main_frame.grid(column= 0, row= 0, sticky="NSEW")
        self.type_entry_frame.grid(column= 0, row= 1)
        self.smokes_entry_frame.grid(column= 0, row= 2, sticky="EW")
        self.gram_entry_frame.grid(column= 0, row= 3, sticky="EW")
        self.checkbuttons_frame.grid(column= 0, row= 4, sticky="EW")
        self.submit_button_frame.grid(column= 0, row= 5)

    def add_entry(self):
        try: write_to_db(type=self.entry_type.get(), owner=self.owner_selection_spinbox.get(),smokes=self.cigs_entry.get(), grams=self.grams_entry.get(), filter=self.filter_check.get(), paper=self.paper_check.get())
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
        self.column1 = Frame(self.root, bg=BACKGROUND_COLOR)
        self.bg_color_label = Label(self.column1, text="Background color:", bg=BACKGROUND_COLOR)
        self.bg_color_selection = StringVar(self.column1, value=self.settings['background_color'])
        self.bg_color_darkgrey = Radiobutton(self.column1, text="Grey",variable=self.bg_color_selection, value="darkgrey", bg=BACKGROUND_COLOR)
        self.bg_color_darkred = Radiobutton(self.column1, text="Red",variable=self.bg_color_selection,value="darkred", bg=BACKGROUND_COLOR)
        # column 1 2nd row
        self.btn_color_label = Label(self.column1, text="Button color:", bg=BACKGROUND_COLOR)
        self.btn_color_selection = StringVar(self.column1, value=self.settings['button_color'])
        self.btn_color_darkblue = Radiobutton(self.column1, text="Dark blue",variable=self.btn_color_selection, value="darkblue", bg=BACKGROUND_COLOR)
        self.btn_color_lightblue = Radiobutton(self.column1, text="Light blue",variable=self.btn_color_selection, value="lightblue", bg=BACKGROUND_COLOR)
        # column 1 3rd row
        self.price_label = Label(self.column1, text="Price per gram: (%.2f)"%self.settings['cost_per_gram'], bg=BACKGROUND_COLOR)
        self.price_entry = Entry(self.column1, bg=BACKGROUND_COLOR)
        # column 1 4th row
        self.filter_price_label = Label(self.column1, text="Price per filter: (%.2f)"%self.settings['price_per_filter'], bg=BACKGROUND_COLOR)
        self.filter_price_entry = Entry(self.column1, bg=BACKGROUND_COLOR)
        # column 1 5th row
        self.paper_price_label = Label(self.column1, text="Price per paper: (%.2f)"%self.settings['price_per_paper'], bg=BACKGROUND_COLOR)
        self.paper_price_entry = Entry(self.column1, bg=BACKGROUND_COLOR)
        # column 2
        self.column2 = Frame(self.root, bg=BACKGROUND_COLOR)
        self.users_label = Label(self.column2, text="Users:", bg=BACKGROUND_COLOR)

        self.users_list = Listbox(self.column2)
        self.users_list.insert("end", *self.settings['owners'])

        self.delete_user_button = Button(self.column2, text="Delete", command=self.remove_user)
        self.add_user_button = Button(self.column2, text="Add", command=self.add_user)

        # Bottom
        self.bottom_frame = Frame(self.root, bg=BACKGROUND_COLOR)
        self.apply_button = Button(self.bottom_frame, text="Apply settings", command=self._set_settings)

    def _grid(self):
        # column 1
        self.bg_color_label.grid(sticky="W")
        self.bg_color_darkgrey.grid()
        self.bg_color_darkred.grid()

        self.btn_color_label.grid(sticky="W")
        self.btn_color_darkblue.grid()
        self.btn_color_lightblue.grid()

        self.price_label.grid(sticky="W")
        self.price_entry.grid(sticky="W")

        self.filter_price_label.grid(sticky="W")
        self.filter_price_entry.grid(sticky="W")

        self.paper_price_label.grid(sticky="W")
        self.paper_price_entry.grid(sticky="W")

        # column 2
        self.users_label.grid(column=0, row=0, columnspan=2)
        self.users_list.grid(column=0, row=1, columnspan=2, padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING["y"])
        self.delete_user_button.grid(column=0, row=2, sticky="EW", padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING["y"])
        self.add_user_button.grid(column=1, row=2, sticky="EW", padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING["y"])

        # submit button
        self.apply_button.grid(sticky="E", padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING["y"])

        # self.root
        self.column1.grid(column=0, row=0, sticky="NSEW")
        self.column2.grid(column=1, row=0, sticky="NSEW")

        self.bottom_frame.grid(column=0, row=1, columnspan=2, sticky="EW")
        
    def _get_settings(self): return get_json_data(SETTINGS_PATH)
    def _set_settings(self):
        self.settings['background_color'] = self.bg_color_selection.get()
        self.settings['button_color'] = self.btn_color_selection.get()
        # catches exception if entry is left unchanged/is containing an illegal value
        try: price = float(self.price_entry.get())
        except: pass
        else: self.settings['cost_per_gram'] = price

        try: ppf = float(self.filter_price_entry.get())
        except: pass
        else: self.settings['price_per_filter'] = ppf

        try: ppp = float(self.paper_price_entry.get())
        except: pass
        else: self.settings['price_per_paper'] = ppp

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
        self.price = float(get_json_data(SETTINGS_PATH)['cost_per_gram'])
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
            # Shifts between dark and light grey for each data entry for appearance
            if no % 2 == 0: bg_color = "grey"
            else: bg_color = "darkgrey"

            frame = Frame(self.root, bg=bg_color)

            date_label = Label(frame, text=v['date'], bg=bg_color)

            data_text = f"{v['type']} - Smokes: {v['smokes']} - Grams: {v['grams']}"
            data_label = Label(frame, text=data_text, bg=bg_color)

            ppf = get_json_data(SETTINGS_PATH)['price_per_filter']
            ppp = get_json_data(SETTINGS_PATH)['price_per_paper']

            total = float(v['grams']) * self.price + (ppf + ppp)

            cost_label = Label(frame, text=f"Total: {round(total, 2)},-", bg=bg_color)

            self.data_entry_frames.append((date_label,data_label,cost_label,frame))

    def _grid(self):
        for i,v in enumerate(self.data_entry_frames):
            try:
                # date label
                v[0].grid(column=0,row=0, sticky="W", padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING["y"])
                # data label
                v[1].grid(column=0, row=1, sticky="W", padx=DEFAULT_PADDING["x"])
                # cost label
                v[2].grid(column=0, row=2, sticky="W", padx=DEFAULT_PADDING["x"], pady=DEFAULT_PADDING["y"])
                # frame containing both labels
                if i<5: v[3].grid(column=0, row=i, sticky="EW")
                elif i>=5 and i<10: v[3].grid(column=1, row=i-5, sticky="EW")
                elif i>=10 and i<15: v[3].grid(column=2, row=i-10, sticky="EW")
                elif i>=15 and i<20: v[3].grid(column=2, row=i-15, sticky="EW")
                else: show_warning("I knew this would happen eventualy", "Sorry, can't show you all the entries no more, tell me to fix this")
            except: print("couldn't grid")

        self.col1.grid()

    def run(self): self.root.mainloop()