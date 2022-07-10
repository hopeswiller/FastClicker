# Ensuring consistent coordinates between listener and controller on Windows
# Recent versions of _Windows_ support running legacy applications scaled
# when the system scaling has been increased beyond 100%.

# This allows old applications to scale, albeit with a blurry look, and avoids tiny, unusable user interfaces.

# This scaling is unfortunately inconsistently applied to a mouse listener and a controller:
# the listener will receive physical coordinates, but the controller has to work with scaled coordinates.
# This can be worked around by telling Windows that your application is DPI aware.
# This is a process global setting, so _pynput_ cannot do it automatically.
# Do enable DPI awareness

import os
import ctypes
from tkinter import Tk
from tkinter import filedialog, messagebox, constants
from pynput import mouse, keyboard
from src import autoclick, load_data, widgets

PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

root = Tk()
widgets.set_window(root, width=612, height=510, resizable=False)

# -------------------------------------------------------------------------------
# Globals
global click_thread
click_thread = autoclick.AutoClicker()
global profile
profile = []
mouselistener = None
keylistener = None
is_clear = False
exit_event = autoclick.exit_event


# ------------------------------------------------------------------------------
# Methods
def pass_data(file):
    try:
        path.delete(0, constants.END)
        path.insert(0, file)
        global profile
        profile, headers = load_data.get_click_profile(file)
        click_thread.profile = profile
    except Exception:
        messagebox.showerror("Error Message !!", "File Couldn't Be Opened...Try Again!")
    else:
        display(headers, profile)


def openfile():
    filename = filedialog.askopenfilename(
        title="Select a file",
        initialdir="./",
        filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")),
    )
    if filename:
        pass_data(filename)
        status.config(text="> File Loaded Successfully...")


def display(headers, profile):
    tree.delete(*tree.get_children())
    tree["column"] = list(headers.keys())
    tree["show"] = "headings"

    for col in tree["column"]:
        tree.column(col, anchor=constants.CENTER, stretch=constants.NO, width=107)
        tree.heading(col, text=col)
    # rows
    for i, row in enumerate(profile):
        tree.insert("", "end", iid=i, values=list(row.values()))

    vscroll.pack(side=constants.RIGHT, fill=constants.Y)
    tree.pack()
    selectionFrame.pack()


def reloadprofile():
    # pickProfile = []
    if len(path.get().strip()) > 0:
        tree.pack_forget()
        vscroll.pack_forget()
        root.update()
        pass_data(path.get().strip())
        status.config(text="> Reloaded Clicking Data...")
    else:
        messagebox.showwarning("Warning Message!!", "Load Data Before Reload")


def fast_load():
    loc = os.path.join(
        os.environ["USERPROFILE"], "Documents", "FastClicker", "recentpaths.txt"
    )
    if os.path.exists(loc):
        with open(loc, "r") as f:
            data = f.read()
        pass_data(data.strip())
        status.config(text="> Saved Data Loaded Successfully...")


def stop_click():
    if click_thread.running:
        click_thread.stop_click()
        print("Stopped Clicking...")
        startClickBtn.config(state=constants.ACTIVE, bg="green", fg="white")
        status.config(text="> Stop Click Initiated...")


def start_click():
    # if data is loaded and not clicking
    if len(path.get()) > 0 or tree.get_children():
        if not click_thread.is_alive():
            click_thread.start()

        if not click_thread.running:
            print("Started Clicking...")
            status.config(text="> Start Click Initiated...")
            exit_event.clear()
            click_thread.status_msg = status
            click_thread.start_click()
            click_thread.app_counter = 0
            click_thread.time_between_repeats = int(repeatsTimeEntry.get().strip())
            click_thread.repetitions = int(repeatsEntry.get().strip())

            status.config(text="> Start Click Initiated...")
            startClickBtn.config(state=constants.DISABLED, bg="#cccccc", fg="#666666")
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
    root.withdraw()  # hide window
    global mouselistener
    global keylistener
    mouselistener = mouse.Listener(on_click=on_click)
    keylistener = keyboard.Listener(on_press=on_press)
    mouselistener.start()
    keylistener.start()


def on_press(key):
    if key == keyboard.Key.esc:
        root.deiconify()  # show window
        keylistener.stop()
        mouselistener.stop()
        status.config(text="> Mouse Listener Cancelled")


def on_click(x, y, button, pressed):
    root.deiconify()  # show window
    global is_clear
    global profile
    location = {"x": x, "y": y, "btn": "L" if button.left else "R"}
    status.config(text=f"> Mouse Clicked at {(x,y)}")
    headers = {"Activity": None, "X": None, "Y": None, "Button": None, "delay(s)": None}

    # raise StopException or return False from a callback to stop the listener.
    if not pressed:
        if is_clear:
            profile.clear()

        if location:
            profile.append(
                {
                    "Activity": f"activity{len(profile)+1}",
                    "X": location["x"],
                    "Y": location["y"],
                    "Button": location["btn"],
                    "delay(s)": 5,
                }
            )
            display(headers, profile)
            vscroll.pack(side=constants.RIGHT, fill=constants.Y)
            tree.pack()
            is_clear = False  # change value of global variable

        click_thread.profile = profile
        keylistener.stop()
        mouselistener.stop()
        root.deiconify()


def remove_loaded_data():
    global is_clear
    is_clear = True  # change value of global variable
    tree.delete(*tree.get_children())
    status.config(text="> Removed Loaded Data...")


def on_closing(thread):
    global click_thread
    click_thread = thread
    if click_thread.is_alive():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            click_thread.exit()
            mouselistener.stop() if mouselistener else None
            keylistener.stop() if keylistener else None
            root.destroy()
    else:
        root.destroy()


def select_record():
    try:
        if tree.get_children():
            activity_entry.delete(0, constants.END)
            x_entry.delete(0, constants.END)
            y_entry.delete(0, constants.END)
            delay_entry.delete(0, constants.END)

            row = tree.item(tree.focus(), "values")
            activity_entry.insert(0, row[0])
            x_entry.insert(0, row[1])
            y_entry.insert(0, row[2])
            checkValue.set("L") if str(row[3]).strip() == "L" else checkValue.set("R")
            delay_entry.insert(0, row[4])
    except IndexError:
        pass


def update_record():
    try:
        if tree.get_children() and x_entry.get() and y_entry.get():
            # grab selected record and update
            selected = tree.focus()
            tree.item(
                selected,
                text="",
                values=(
                    activity_entry.get(),
                    x_entry.get(),
                    y_entry.get(),
                    checkValue.get(),
                    delay_entry.get(),
                ),
            )
            global profile
            profile[int(selected)] = {
                "Activity": activity_entry.get(),
                "X": int(x_entry.get()),
                "Y": int(y_entry.get()),
                "Button": checkValue.get(),
                "delay(s)": int(delay_entry.get()),
            }
            activity_entry.delete(0, constants.END)
            x_entry.delete(0, constants.END)
            y_entry.delete(0, constants.END)
            checkValue.set("L")
            delay_entry.delete(0, constants.END)
    except ValueError:
        pass


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
    checkValue,
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
root.protocol("WM_DELETE_WINDOW", lambda: on_closing(click_thread))
root.attributes("-topmost", True)
root.mainloop()
