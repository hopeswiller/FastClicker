import os,requests,time,math
from tkinter import *
from tkinter import ttk,filedialog, messagebox
from src import autoclick, load_data


root = Tk()
root.title("FastClicker")
root.iconbitmap("icon.ico")

width = 482
height = 410
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
            path.delete(0, END)
            path.insert(0, filename)
            profile,headers = load_data.get_click_profile(filename)
            click_thread.profile = profile
            click_thread.repetitions = int(repeatsEntry.get().strip())
        except FileNotFoundError:
            messagebox.showerror("Error Message !!", "File Couldn't Be Opened...Try Again!")
        except ValueError:
            messagebox.showerror("Error Message !!", "File Couldn't Be Opened...Try Again!")
        else:
            display(headers,profile)
            reloadBtn.config(state=ACTIVE)
            if not click_thread.is_alive():
                click_thread.start()
                status.config(text = "> Click Thread Started...")



def remove_loaded_data():
    tree.delete(*tree.get_children())
    status.config(text = "> Removed Loaded Data...")

def display(headers, profile):
    tree.delete(*tree.get_children())
    tree["column"] = list(headers.keys())
    tree["show"] = "headings"

    for col in tree["column"]:
        tree.column(col, anchor=CENTER, stretch=NO, width=83)
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
        profile,headers = load_data.get_click_profile(path.get().strip())
        click_thread.profile = profile
        click_thread.repetitions = int(repeatsEntry.get().strip())
        display(headers, profile)
        status.config(text = "> Reloaded Clicking Data...")



def stop_click():
    startClickBtn.config(state=ACTIVE,bg="green",fg="white")
    if click_thread.running:
        click_thread.stop_click()
        print("Stopped Clicking...")
        # templateBtn.config(state=ACTIVE,bg="maroon",fg="white")
        status.config(text = "> Stop Click Initiated...")


def start_click():
    # if data is loaded and not clicking
    if len(path.get()) > 0 and tree.get_children():
        if not click_thread.running:
            print("Started Clicking...")
            click_thread.app_running = True
            click_thread.start_click()
            click_thread.app_counter = 0
            click_thread.time_between_repeats = int(repeatsTimeEntry.get().strip())
            click_thread.repetitions = int(repeatsEntry.get().strip())
            # templateBtn.config(state=DISABLED,bg="#cccccc",fg="#666666")
            status.config(text = "> Start Click Initiated...")
            startClickBtn.config(state=DISABLED,bg="#cccccc",fg="#666666")
    else:
        # info, warning,error,askquestion,askokcancel,askyesno
        messagebox.showwarning("Warning Message !!", "Please Load Clicking Data")



# def download():
#     # change dir to downloads
#     os.chdir(os.path.join(os.environ['USERPROFILE'],'Downloads'))

#     # check if file already exists
#     if (os.path.exists("SampleTemplate.xlsx") == False):
#         status.config(text="> Downloading Template File...")
#         progressValue.grid(row=0,column=0)
#         progressBar.grid(row=0,column=1)

#         res = requests.get(
#             "https://drive.google.com/uc?export=download&id=17jenL8-Do108aVZBKETNDMXpLGJE6N_I",
#             stream = True
#         )
#         total_size = int(res.headers['content-length'])
#         with open("SampleTemplate.xlsx", 'wb') as f:
#             for data in res:
#                 f.write(data)
#                 progressBar['value'] += (100/70)  # progress is 100 divided by the length / how long is your loop
#                 progressValue.config(text=f"{round(progressBar['value'])}%")
#                 root.update_idletasks()
#                 time.sleep(0.15)

#             # for data in tqdm(iterable=res.iter_content(chunk_size = 1024), total=total_size/1024, unit="KB"):
#             #     f.write(data)
#         status.config(text="> Download Completed...")
#         messagebox.showinfo("Download Completed","Your File Successfully Downloaded to Downloads Folder")
#     else:
#         messagebox.showerror("Error","File Already Exist in Downloading Path!")


def save_data():
    if len(path.get()) > 0:
        # change dir to downloads
        location = os.path.join(os.environ['USERPROFILE'],'Documents','FastClicker')
        os.mkdir(location) if not os.path.exists(location) else None
        os.chdir(location)

        if os.path.exists("recentpaths.txt"):
            os.remove("recentpaths.txt")

        with open('recentpaths.txt', 'w') as f:
            f.truncate()
            f.write(path.get().strip())
        status.config(text="> Data Saved...")



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
file = Menu(menubar,tearoff=False)
menubar.add_cascade(label="File",menu=file)
# file.add_command(label="Download Template",command=download)
# file.add_command(label="Donate",command=download)
file.add_command(label="Save Data",command=save_data)
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

reloadBtn = Button(cursorFrame, text="Reload", command=reloadprofile)
reloadBtn.grid(row=0,column=4,padx=5)




# --------------------------------------------------------------------
# Data 
dataFrame = LabelFrame(root, text="Profile", padx=2, pady=5)
dataFrame.pack(padx=10,pady=2)

# Create vertical scrollbar
vscroll = Scrollbar(dataFrame,orient ="vertical")

# Create Treeview and configure with scrollbar
tree = ttk.Treeview(dataFrame,height=5,yscrollcommand=vscroll.set)
vscroll.config(command=tree.yview)



# --------------------------------------------------------------------
# Clicking Options
clickFrame = LabelFrame(root, text="Clicking Options", padx=4, pady=5)
clickFrame.pack(padx=15,pady=2)

repeatsLabel = Label(clickFrame, text="Number of Repeats")
repeatsLabel.grid(row=0,column=0,padx=3)

repeatstimeLabel = Label(clickFrame, text="Time Between Repeats(s)")
repeatstimeLabel.grid(row=1,column=0,padx=3)

repeatsEntry = Entry(clickFrame, width=15,justify="right")
repeatsEntry.insert(-1, 100)
repeatsEntry.grid(row=0,column=1,padx=5)

repeatsTimeEntry = Entry(clickFrame, width=15,justify="right")
repeatsTimeEntry.insert(-1, 10)
repeatsTimeEntry.grid(row=1,column=1,padx=5)

startClickBtn = Button(clickFrame,text="Start Clicking",bg="green",fg="white", command=start_click)
startClickBtn.grid(row=0,column=2,padx=5)

stopClickBtn = Button(clickFrame, text="Stop Clicking",bg="maroon",fg="white",command=stop_click)
stopClickBtn.grid(row=0,column=3,padx=5)


# templateBtn = Button(clickFrame, text="Download Sample Template",bg="maroon",fg="white",command=download)
# templateBtn.grid(row=1,column=2,padx=5,pady=5,columnspan=2)


# -------------------------------------------------------------------------------
# Status Bar

status = Label(root, text="> Developed by hopeswiller<davidba941@gmail.com>",border=1, relief=SUNKEN,anchor=W,padx=5)
status.pack(side=BOTTOM, fill=X)

frame = Frame(root)
frame.pack(side=BOTTOM,pady=7,padx=8)
progressValue = Label(frame,text="0%")
progressBar = ttk.Progressbar(frame,orient=HORIZONTAL,length=width-50, mode="determinate")


# root.bell()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.focus_force()
root.grab_set()


loc = os.path.join(os.environ['USERPROFILE'],'Documents','FastClicker','recentpaths.txt')
if os.path.exists(loc):
    with open(loc, 'r') as f:
        data = f.read()
    path.insert(0, data)

root.mainloop()