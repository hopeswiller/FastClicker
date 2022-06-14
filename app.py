import os, requests, time, math
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from src import autoclick, load_data
from pynput.mouse import Controller, Listener

root = Tk()
root.title("FastClicker")
root.iconbitmap("./icon.ico")

width = 480
height = 400
root.minsize(width, height)
root.maxsize(width, height)
x_Left = int(root.winfo_screenwidth() / 2 - width / 1.5)
y_Top = int(root.winfo_screenheight() / 2 - height / 1.5)
root.geometry(f"{width}x{height}+{x_Left}+{y_Top}")  # "widthxheight+Left+Top"
root.resizable(0, 0)

# ------------------------------------------------------------------------------
# Processes
click_thread = autoclick.AutoClicker()

# ------------------------------------------------------------------------------
# Methods


def openfile():
    filename = filedialog.askopenfilename(
        title="Select a file",
        initialdir="./",
        filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")),
    )
    if filename:
        try:
            path.insert(0, filename)
            global profile
            global headers
            profile, headers = load_data.get_click_profile(filename)
            click_thread.profile = profile
            click_thread.repetitions = int(repeatsEntry.get().strip())
        except FileNotFoundError:
            messagebox.showerror(
                "Error Message !!", "File Couldn't Be Opened...Try Again!"
            )
        except ValueError:
            messagebox.showerror(
                "Error Message !!", "File Couldn't Be Opened...Try Again!"
            )
        else:
            if not click_thread.is_alive():
                click_thread.start()
                status.config(text="> Click Thread Started...")

        display()


def remove_loaded_data():
    tree.delete(*tree.get_children())
    status.config(text="> Removed Loaded Data...")


def display():
    tree.delete(*tree.get_children())
    tree["column"] = list(headers.keys())
    tree["show"] = "headings"

    for col in tree["column"]:
        tree.column(col, anchor=CENTER, stretch=NO, width=70)
        tree.heading(col, text=col)

    # rows
    for row in profile:
        tree.insert("", "end", values=list(row.values()))

    vscroll.pack(side=RIGHT, fill=Y)
    tree.pack()


def reloadprofile():
    if len(path.get().strip()) > 0:
        tree.pack_forget()
        vscroll.pack_forget()
        root.update()
        display()
        status.config(text="Reloaded Clicking Data...")


def stop_click():
    if click_thread.running:
        click_thread.stop_click()
        print("Stopped Clicking...")
        templateBtn.config(state=ACTIVE, bg="maroon", fg="white")
        status.config(text="> Clicking Stopped...")


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
            templateBtn.config(state=DISABLED, bg="#cccccc", fg="#666666")
            status.config(text="> Clicking Started...")
    else:
        # info, warning,error,askquestion,askokcancel,askyesno
        messagebox.showwarning("Warning Message !!", "Please Load Clicking Data or Pick Locations")


def download():
    # change dir to downloads
    os.chdir(os.path.join(os.environ["USERPROFILE"], "Downloads"))

    # check if file already exists
    if os.path.exists("SampleTemplate.xlsx") == False:
        status.config(text="> Downloading Template File...")
        progressValue.grid(row=0, column=0)
        progressBar.grid(row=0, column=1)

        res = requests.get(
            "https://drive.google.com/uc?export=download&id=17jenL8-Do108aVZBKETNDMXpLGJE6N_I",
            stream=True,
        )
        total_size = int(res.headers["content-length"])
        with open("SampleTemplate.xlsx", "wb") as f:
            for data in res:
                f.write(data)
                progressBar["value"] += (
                    100 / 70
                )  # progress is 100 divided by the length / how long is your loop
                progressValue.config(text=f"{round(progressBar['value'])}%")
                root.update_idletasks()
                time.sleep(0.15)

            # for data in tqdm(iterable=res.iter_content(chunk_size = 1024), total=total_size/1024, unit="KB"):
            #     f.write(data)
        status.config(text="> Download Completed...")
        messagebox.showinfo(
            "Download Completed",
            "Your File Successfully Downloaded to Downloads Folder",
        )
    else:
        messagebox.showerror("Error", "File Already Exist in Downloading Path!")


def save_data():
    pass


def on_move(x, y):
    root.update_idletasks()
    status.config(text=f"> Mouse Moved to position {(x,y)}")
    root.update_idletasks()


pickProfile = []
def on_click(x, y, button, pressed):
    print(f"Mouse {'Pressed' if pressed else 'Released'} at {(x,y)}")

    location = {"x": x, "y": y, "btn": "L" if button.left else "R"}
    status.config(text=f"> Mouse Clicked at {(x,y)}")

    # call Listener.stop from anywhere,
    # raise StopException or return False from a callback to stop the listener.
    if not pressed:
        if location:
            tree["column"] = ("Activity", "X", "Y", "Button", "delay(ms)", "delay(s)")
            tree["show"] = "headings"

            for col in tree["column"]:
                tree.column(col, anchor=CENTER, stretch=NO, width=70)
                tree.heading(col, text=col)

            # # rows
            tree.insert(
                "",
                "end",
                values=(
                    "activity",
                    location["x"],
                    location["y"],
                    location["btn"],
                    "6000",
                    "6",
                ),
            )
            pickProfile.append(
                {
                    "Activity": "activity",
                    "X": location["x"],
                    "Y": location["y"],
                    "Button": location["btn"],
                    "delay(ms)": 6000,
                    "delay(s)": 6,
                }
            )

            vscroll.pack(side=RIGHT, fill=Y)
            tree.pack()

        click_thread.profile = pickProfile
        templateBtn.config(state=ACTIVE, bg="maroon", fg="white")
        # Stop listener
        return False


# [
#   {'Activity': 'refresh', 'X': 58, 'Y': 847, 'Button': 'L', 'delay(ms)': 6000, 'delay(s)': 6},
#   {'Activity': 'order', 'X': 58, 'Y': 847, 'Button': 'L', 'delay(ms)': 6000, 'delay(s)': 6}
# ]


def pickLocation():
    mouse = Controller()
    templateBtn.config(state=DISABLED, bg="#cccccc", fg="#666666")
    # with Listener(on_click=on_click) as listener:
    # listener.join()
    listener = Listener(on_move=on_move, on_click=on_click)
    listener.start()


def on_closing():
    if click_thread.is_alive():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            click_thread.exit()
            root.destroy()
    else:
        root.destroy()


# -------------------------------------------------------------------------------
# Menu
menubar = Menu(root)
root.config(menu=menubar)

# Create menu item
file = Menu(menubar, tearoff=False)
menubar.add_cascade(label="File", menu=file)
file.add_command(label="Download Template", command=download)
file.add_command(label="Save", command=save_data)
file.add_separator()
file.add_command(label="Exit", command=on_closing)

edit = Menu(menubar, tearoff=False)
menubar.add_cascade(label="Edit", menu=edit)
edit.add_command(label="Reload Data", command=reloadprofile)
edit.add_command(label="Remove Data", command=remove_loaded_data)


# -------------------------------------------------------------------------------
# Cursor Options
cursorFrame = LabelFrame(root, text="Cursor Options", padx=5, pady=5)
cursorFrame.pack(padx=18, pady=5)

pathLabel = Label(cursorFrame, text="File")
pathLabel.grid(row=0, column=1)

path = Entry(cursorFrame, width=37)
path.grid(row=0, column=2, padx=5)

loadBtn = Button(
    cursorFrame, bg="green", fg="white", text="Load Profile", command=openfile
)
loadBtn.grid(row=0, column=3, padx=4)

pickLocationBtn = Button(
    cursorFrame, text="Pick Location", bg="maroon", fg="white", command=pickLocation
)
pickLocationBtn.grid(row=0, column=4, padx=4)


# --------------------------------------------------------------------
# Data
dataFrame = LabelFrame(root, text="Profile", padx=2, pady=5)
dataFrame.pack(padx=10, pady=2)

# Create vertical scrollbar
vscroll = Scrollbar(dataFrame, orient="vertical")

# Create Treeview and configure with scrollbar
tree = ttk.Treeview(dataFrame, height=5, yscrollcommand=vscroll.set)
vscroll.config(command=tree.yview)


# --------------------------------------------------------------------
# Clicking Options
clickFrame = LabelFrame(root, text="Clicking Options", padx=4, pady=5)
clickFrame.pack(padx=15, pady=2)

repeatsLabel = Label(clickFrame, text="Number of Repeats")
repeatsLabel.grid(row=0, column=0, padx=3)

repeatstimeLabel = Label(clickFrame, text="Time Between Repeats(s)")
repeatstimeLabel.grid(row=1, column=0, padx=3)

repeatsEntry = Entry(clickFrame, width=15, justify="right")
repeatsEntry.insert(-1, 5)
repeatsEntry.grid(row=0, column=1, padx=5)

repeatsTimeEntry = Entry(clickFrame, width=15, justify="right")
repeatsTimeEntry.insert(-1, 10)
repeatsTimeEntry.grid(row=1, column=1, padx=5)

startClickBtn = Button(
    clickFrame, text="Start Clicking", bg="green", fg="white", command=start_click
)
startClickBtn.grid(row=0, column=2, padx=5)

stopClickBtn = Button(
    clickFrame, text="Stop Clicking", bg="maroon", fg="white", command=stop_click
)
stopClickBtn.grid(row=0, column=3, padx=5)


templateBtn = Button(
    clickFrame,
    text="Download Sample Template",
    bg="maroon",
    fg="white",
    command=download,
)
templateBtn.grid(row=1, column=2, padx=5, pady=5, columnspan=2)


# -------------------------------------------------------------------------------
# Status Bar

status = Label(
    root, text="> Developed by Hopeswiller", border=1, relief=SUNKEN, anchor=W, padx=5
)
status.pack(side=BOTTOM, fill=X)

frame = Frame(root)
frame.pack(side=BOTTOM, pady=7, padx=8)
progressValue = Label(frame, text="0%")
progressBar = ttk.Progressbar(
    frame, orient=HORIZONTAL, length=width - 50, mode="determinate"
)


# root.bell()
root.focus_force()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
