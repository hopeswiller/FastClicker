import os
from tkinter import *
from tkinter import filedialog, messagebox
from pynput.mouse import Controller, Listener
from src import autoclick, load_data, widgets


root = Tk()
widgets.set_window(root, width=480, height=410, resizable=True)


# ------------------------------------------------------------------------------
# Processes
click_thread = autoclick.AutoClicker()

# ------------------------------------------------------------------------------
# Methods
def pass_data(file):
    try:
        path.delete(0, END)
        path.insert(0, file)
        global profile
        global headers
        profile, headers = load_data.get_click_profile(file)
        click_thread.profile = profile
        click_thread.repetitions = int(repeatsEntry.get().strip())
    except FileNotFoundError:
        messagebox.showerror("Error Message !!", "File Couldn't Be Opened...Try Again!")
    except ValueError:
        messagebox.showerror("Error Message !!", "File Couldn't Be Opened...Try Again!")
    else:
        display(headers, profile)
        if not click_thread.is_alive():
            click_thread.start()



def openfile():
    filename = filedialog.askopenfilename(
        title="Select a file",
        initialdir="./",
        filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")),
    )
    if filename:
        pass_data(filename)
        status.config(text="> Click Thread Started...")


def display(headers, profile):
    tree.delete(*tree.get_children())
    tree["column"] = list(headers.keys())
    tree["show"] = "headings"

    for col in tree["column"]:
        tree.column(col, anchor=CENTER, stretch=NO, width=83)
        tree.heading(col, text=col)

    # rows
    for row in profile:
        tree.insert("", "end", values=list(row.values()))

    vscroll.pack(side=RIGHT, fill=Y)
    tree.pack()
    selectionFrame.pack()


def reloadprofile():
    pickProfile = []
    if len(path.get().strip()) > 0:
        tree.pack_forget()
        vscroll.pack_forget()
        root.update()
        pass_data(path.get().strip())
        status.config(text="> Reloaded Clicking Data...")
    else:
        messagebox.showwarning("Warning Message !!", "Load Data Before Reload")


def fast_load():
    loc = os.path.join(
        os.environ["USERPROFILE"], "Documents", "FastClicker", "recentpaths.txt"
    )
    if os.path.exists(loc):
        with open(loc, "r") as f:
            data = f.read()
        # path.insert(0, data)
        pass_data(data.strip())
        status.config(text="> Click Thread Started...")


def stop_click():
    if click_thread.running:
        click_thread.stop_click()
        print("Stopped Clicking...")
        startClickBtn.config(state=ACTIVE, bg="green", fg="white")
        status.config(text="> Stop Click Initiated...")


def start_click():
    # if data is loaded and not clicking
    if len(path.get()) > 0 or tree.get_children():
        if not click_thread.is_alive():
            click_thread.start()

        if not click_thread.running:
            print("Started Clicking...")
            click_thread.app_running = True
            click_thread.start_click()
            click_thread.app_counter = 0
            click_thread.time_between_repeats = int(repeatsTimeEntry.get().strip())
            click_thread.repetitions = int(repeatsEntry.get().strip())
            status.config(text="> Start Click Initiated...")
            startClickBtn.config(state=DISABLED, bg="#cccccc", fg="#666666")

            # status.config(text=click_thread.status_msg)
    else:
        # info, warning,error,askquestion,askokcancel,askyesno
        messagebox.showwarning("Warning Message!!", "Please Load Clicking Data")


def save_data():
    if len(path.get()) > 0:
        location = os.path.join(os.environ["USERPROFILE"], "Documents", "FastClicker")
        os.mkdir(location) if not os.path.exists(location) else None
        os.chdir(location)

        if os.path.exists("recentpaths.txt"):
            os.remove("recentpaths.txt")

        with open("recentpaths.txt", "w") as f:
            f.truncate()
            f.write(path.get().strip())
        status.config(text="> Data Saved...")


def pickLocation():
    mouse = Controller()
    # with Listener(on_click=on_click) as listener:
    # listener.join()
    root.withdraw() # hide window
    listener = Listener(on_move=on_move, on_click=on_click)
    listener.start()

def on_move(x, y):
    root.update_idletasks()
    status.config(text=f"> Mouse Moved to position {(x,y)}")
    root.update_idletasks()

# [
#   {'Activity': 'refresh', 'X': 58, 'Y': 847, 'Button': 'L', 'delay(ms)': 6000, 'delay(s)': 6},
#   {'Activity': 'order', 'X': 58, 'Y': 847, 'Button': 'L', 'delay(ms)': 6000, 'delay(s)': 6}
# ]
is_clear = False

pickProfile = []
def on_click(x, y, button, pressed):
    root.deiconify() # show window
    global is_clear
    location = {"x": x, "y": y, "btn": "L" if button.left else "R"}
    status.config(text=f"> Mouse Clicked at {(x,y)}")
    headers = {'Activity': None, 'X': None, 'Y': None, 'Button': None, 'delay(s)': None}

    # call Listener.stop from anywhere,
    # raise StopException or return False from a callback to stop the listener.
    if not pressed:
        if is_clear:
            pickProfile.clear()

        if location:
            pickProfile.append(
                {
                    "Activity": "activity",
                    "X": location["x"],
                    "Y": location["y"],
                    "Button": location["btn"],
                    "delay(s)": 5,
                }
            )
            display(headers,pickProfile)
            vscroll.pack(side=RIGHT, fill=Y)
            tree.pack()
            is_clear = False   # change value of global variable

        click_thread.profile = pickProfile
        # Stop listener
        return False

def remove_loaded_data():
    global is_clear
    is_clear = True   # change value of global variable
    tree.delete(*tree.get_children())
    status.config(text="> Removed Loaded Data...")


def on_closing():
    if click_thread.is_alive():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            click_thread.exit()
            root.destroy()
    else:
        root.destroy()


def select_record():
    if tree.get_children():
        activity_entry.delete(0, END)
        x_entry.delete(0, END)
        y_entry.delete(0, END)
        delay_entry.delete(0, END)

        values = tree.item(tree.focus(), "values")
        activity_entry.insert(0, values[0])
        x_entry.insert(0, values[1])
        y_entry.insert(0, values[2])
        delay_entry.insert(0, values[4])


def update_record():
    if tree.get_children():
        # grab selected record and update
        selected = tree.focus()
        values = tree.item(
            selected,
            text="",
            values=(
                activity_entry.get(),
                x_entry.get(),
                y_entry.get(),
                "L",
                delay_entry.get(),
            ),
        )
        activity_entry.delete(0, END)
        x_entry.delete(0, END)
        y_entry.delete(0, END)
        delay_entry.delete(0, END)


# -------------------------------------------------------------------------------
# Menu
file, edit = widgets.get_menu_bar(root)
# add subitems to menu items
file.add_command(label="Save Path", command=save_data)
file.add_separator()
file.add_command(label="Exit", command=on_closing)
edit.add_command(label="Remove Data", command=remove_loaded_data)


# -------------------------------------------------------------------------------
# Cursor Options
(
    cursorFrame,
    path,
    loadBtn,
    reloadBtn,
    pickBtn,
) = widgets.get_cursor_options_items(root)
loadBtn.config(command=openfile)
reloadBtn.config(command=reloadprofile)
pickBtn.config(command=pickLocation)


# --------------------------------------------------------------------
# Data Frame
(
    vscroll,
    tree,
    selectionFrame,
    selectbtn,
    updatebtn,
    activity_entry,
    x_entry,
    y_entry,
    delay_entry,
) = widgets.get_profile_frame_items(root)
selectbtn.configure(command=select_record)
updatebtn.configure(command=update_record)

# --------------------------------------------------------------------
# Clicking Options
(
    clickFrame,
    repeatsEntry,
    repeatsTimeEntry,
    startClickBtn,
    stopClickBtn,
) = widgets.get_clicking_options_items(root)

startClickBtn.config(command=start_click)
stopClickBtn.config(command=stop_click)


# -------------------------------------------------------------------------------
# Status Bar
status = widgets.get_status_bar(root)

fast_load()
root.bell()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.focus_force()
root.grab_set()
root.mainloop()
