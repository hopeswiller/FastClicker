import os
from tkinter import *
from tkinter import ttk,filedialog, messagebox
from src import autoclick, load_data


root = Tk()
root.title("AutoClicker")

width = 480
height = 370
root.minsize(width, height)
root.maxsize(width, height)
x_Left = int(root.winfo_screenwidth() / 2 - width / 1.5)
y_Top = int(root.winfo_screenheight() / 2 - height / 1.5)
root.geometry(f"{width}x{height}+{x_Left}+{y_Top}")  # "widthxheight+Left+Top"
root.resizable(0,0)


# ------------------------------------------------------------------------------
# Processes
click_thread = autoclick.AutoClicker()

# ------------------------------------------------------------------------------
# Methods

def openfile():
    filename = filedialog.askopenfilename(
        title="Select a file",
        initialdir="./",
        filetypes=(("Excel files", "*.xlsx"),("All files", "*.*"))
    )
    if filename:
        try:
            path.insert(0, filename)
            global profile
            global headers
            profile,headers = load_data.get_click_profile(filename)
            click_thread.profile = profile
            click_thread.repetitions = int(repeatsEntry.get().strip())
        except FileNotFoundError:
            messagebox.showerror("Error Message !!", "File Couldn't Be Opened...Try Again!")
        except ValueError:
            messagebox.showerror("Error Message !!", "File Couldn't Be Opened...Try Again!")
        else:
            if not click_thread.is_alive():
                click_thread.start()
                status.config(text = "> Click Thread Started...")

        display()
        reloadBtn.config(state=ACTIVE)


def remove_loaded_data():
    tree.delete(*tree.get_children())
    status.config(text = "> Removed Loaded Data...")

def display():
    remove_loaded_data()
    tree["column"] = list(headers.keys())
    tree["show"] = "headings"

    for col in tree["column"]:
        tree.column(col, anchor=CENTER, stretch=NO, width=70)
        tree.heading(col,text=col)

    # rows
    for row in profile:
        tree.insert("", "end", values=list(row.values()))

    vscroll.pack(side=RIGHT,fill=Y)
    tree.pack()
    


def reloadprofile():
    if len(path.get().strip()) > 0:
        tree.pack_forget()
        vscroll.pack_forget()
        root.update()
        display()
        status.config(text = "Reloaded Clicking Data...")



def stop_click():
    if click_thread.running:
        click_thread.stop_click()
        print("Stopped Clicking...")
        status.config(text = "> Clicking Stopped...")


def start_click():
    # if data is loaded and not clicking
    if len(path.get()) > 0 and tree.get_children():
        if not click_thread.running:
            print("Started Clicking...")
            click_thread.app_running = True
            click_thread.start_click()
            click_thread.app_counter = 0
            click_thread.time_between_repeats = int(repeatsTimeEntry.get().strip())
            status.config(text = "> Clicking Started...")
    else:
        # info, warning,error,askquestion,askokcancel,askyesno
        messagebox.showwarning("Warning Message !!", "Please Load Clicking Data")


def download():
    os.chdir(path)


def save_data():
    pass


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        click_thread.exit()
        root.destroy()

# -------------------------------------------------------------------------------
# Menu
menubar = Menu(root)
root.config(menu=menubar)

# Create menu item
file = Menu(menubar,tearoff=False)
menubar.add_cascade(label="File",menu=file)
file.add_command(label="Download Template",command=download)
file.add_command(label="Save",command=save_data)
file.add_separator()
file.add_command(label="Exit",command=on_closing)

edit = Menu(menubar,tearoff=False)
menubar.add_cascade(label="Edit",menu=edit)
edit.add_command(label="Remove Data", command=remove_loaded_data)





# -------------------------------------------------------------------------------
# Cursor Options
cursorFrame = LabelFrame(root, text="Cursor Options", padx=5, pady=5)
cursorFrame.pack(padx=20,pady=5)

pathLabel = Label(cursorFrame,text="File Path")
pathLabel.grid(row=0,column=1)

path = Entry(cursorFrame, width=37)
path.grid(row=0,column=2,padx=5)

loadBtn = Button(cursorFrame, bg="green",fg="white",text="Load Profile",command=openfile)
loadBtn.grid(row=0,column=3,padx=5)

reloadBtn = Button(cursorFrame, text="Reload",command=reloadprofile,state=DISABLED)
reloadBtn.grid(row=0,column=4,padx=5)




# --------------------------------------------------------------------
# Data 
dataFrame = LabelFrame(root, text="Profile", padx=2, pady=5)
dataFrame.pack(padx=10,pady=2)

# Create an instance of Style widget
style=ttk.Style()
style.theme_use('clam')

# Create vertical scrollbar
vscroll = Scrollbar(dataFrame,orient ="vertical")

# Create Treeview and configure with scrollbar
tree = ttk.Treeview(dataFrame,height=5,yscrollcommand=vscroll.set)
vscroll.config(command=tree.yview)



# --------------------------------------------------------------------
# Clicking Options
clickFrame = LabelFrame(root, text="Clicking Options", padx=4, pady=5)
clickFrame.pack(padx=15,pady=3)

repeatsLabel = Label(clickFrame, text="Number of Repeats")
repeatsLabel.grid(row=0,column=0,padx=3)

repeatstimeLabel = Label(clickFrame, text="Time Between Repeats(s)")
repeatstimeLabel.grid(row=1,column=0,padx=3)

repeatsEntry = Entry(clickFrame, width=15,justify="right")
repeatsEntry.insert(-1, 5)
repeatsEntry.grid(row=0,column=1,padx=5)

repeatsTimeEntry = Entry(clickFrame, width=15,justify="right")
repeatsTimeEntry.insert(-1, 10)
repeatsTimeEntry.grid(row=1,column=1,padx=5)

startClickBtn = Button(clickFrame,text="Start Clicking",bg="green",fg="white", command=start_click)
startClickBtn.grid(row=0,column=2,padx=5)

stopClickBtn = Button(clickFrame, text="Stop Clicking",bg="maroon",fg="white",command=stop_click)
stopClickBtn.grid(row=0,column=3,padx=5)


templateBtn = Button(clickFrame, text="Download Sample Template",bg="maroon",fg="white",command=download)
templateBtn.grid(row=1,column=2,padx=5,pady=5,columnspan=2)


# -------------------------------------------------------------------------------
# Status Bar
status = Label(root, text="> Developed by Hopeswiller",border=1, relief=SUNKEN,anchor=W,padx=5)
status.pack(side=BOTTOM, fill=X)



while True and click_thread.running:
    status.config(text=click_thread.status_msg)


# root.bell()
root.focus_force()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()