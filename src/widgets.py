import sys
from tkinter import (
    Menu,
    Button,
    LabelFrame,
    Label,
    Entry,
    Checkbutton,
    StringVar,
    Scrollbar,
    SUNKEN,
    BOTTOM,
    W,
    X,
)
from tkinter import ttk


def set_window(root, width, height, resizable=True):
    """
    Set Window Frame with width, height and resizable
    """
    root.title("FastClicker")

    # running interactively or local
    if (sys.stdin and sys.stdin.isatty()) or "pytest" in sys.modules:
        root.iconbitmap("assets/icon.ico")
    else:
        root.iconbitmap("icon.ico")

    root.minsize(width, height)
    root.maxsize(width, height)
    x_Left = int(root.winfo_screenwidth() / 2 - width / 1.5)
    y_Top = int(root.winfo_screenheight() / 2 - height / 1.5)
    root.geometry(f"{width}x{height}+{x_Left}+{y_Top}")  # "widthxheight+Left+Top"
    root.resizable(0, 0) if not resizable else None


def get_menu_bar(root):
    """
    Create Menu Bar and its items
    """
    menubar = Menu(root)
    file = Menu(menubar, tearoff=False)
    edit = Menu(menubar, tearoff=False)

    # add items to menu bar
    menubar.add_cascade(label="File", menu=file)
    menubar.add_cascade(label="Edit", menu=edit)

    root.config(menu=menubar)
    return file, edit


def get_cursor_options_items(root):
    cursorFrame = LabelFrame(root, text="Cursor Options", padx=5, pady=7)
    cursorFrame.pack(padx=18, pady=6)
    pathLabel = Label(cursorFrame, text="File")
    path = Entry(cursorFrame, width=39)
    loadBtn = Button(cursorFrame, bg="green", fg="white", text="Load File")
    reloadBtn = Button(cursorFrame, text="Reload", bg="azure3")
    pickBtn = Button(cursorFrame, text="Pick Pos", bg="azure3")

    pathLabel.grid(row=0, column=1)
    path.grid(row=0, column=2, padx=4)
    loadBtn.grid(row=0, column=3, padx=2)
    reloadBtn.grid(row=0, column=4, padx=2)
    pickBtn.grid(row=0, column=5, padx=2)

    return (cursorFrame, path, loadBtn, reloadBtn, pickBtn)


def get_profile_frame_items(root):
    checkValue = StringVar()
    dataFrame = LabelFrame(root, text="Profile", padx=2, pady=5)
    dataFrame.pack(padx=18, pady=2)

    selectionFrame = LabelFrame(dataFrame, padx=2, pady=5, width=13)
    selectionFrame.pack(padx=4, pady=6)

    Label(selectionFrame, text="Act:").grid(row=0, column=0)
    Label(selectionFrame, text="X:").grid(row=0, column=2)
    Label(selectionFrame, text="Y:").grid(row=0, column=4)
    Label(selectionFrame, text="Delay(s):").grid(row=0, column=6)
    selectbtn = Button(selectionFrame, text="Select", bg="maroon", fg="white")
    updatebtn = Button(selectionFrame, text="Update", bg="green", fg="white")

    activity_entry = Entry(selectionFrame, width=7)
    activity_entry.grid(row=0, column=1, padx=1)

    x_entry = Entry(selectionFrame, width=5)
    x_entry.grid(row=0, column=3, padx=1)
    x_entry.insert(-1, 0)

    y_entry = Entry(selectionFrame, width=5)
    y_entry.grid(row=0, column=5, padx=1)
    y_entry.insert(-1, 0)

    delay_entry = Entry(selectionFrame, width=5)
    delay_entry.grid(row=0, column=7, padx=1)
    delay_entry.insert(-1, 6)

    btn_check = Checkbutton(
        selectionFrame,
        text="Right Click",
        variable=checkValue,
        onvalue="R",
        offvalue="L",
    )
    btn_check.deselect()
    btn_check.grid(row=0, column=9)

    selectbtn.grid(row=0, column=10, padx=1)
    updatebtn.grid(row=0, column=11, padx=3)
    # Create vertical scrollbar
    vscroll = Scrollbar(dataFrame, orient="vertical")

    # Create Treeview and configure with scrollbar
    tree = ttk.Treeview(dataFrame, height=5, yscrollcommand=vscroll.set)
    vscroll.config(command=tree.yview)

    return (
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
    )


def get_clicking_options_items(root):
    clickFrame = LabelFrame(root, text="Clicking Options", padx=8, pady=8)
    clickFrame.pack(padx=18, pady=4)

    repeatsLabel = Label(clickFrame, text="Number of Repeats: ")
    repeatsLabel.grid(row=0, column=0, padx=3)

    repeatsEntry = Entry(clickFrame, width=15, justify="right")
    repeatsEntry.insert(-1, 9999)
    repeatsEntry.grid(row=0, column=1, padx=8)

    repeatstimeLabel = Label(clickFrame, text="Time Between Repeats(s): ")
    repeatstimeLabel.grid(row=1, column=0, padx=3)

    repeatsTimeEntry = Entry(clickFrame, width=15, justify="right")
    repeatsTimeEntry.insert(-1, 5)
    repeatsTimeEntry.grid(row=1, column=1, padx=8)

    startClickBtn = Button(clickFrame, text="Start Clicking", bg="green", fg="white")
    startClickBtn.grid(row=0, column=2, padx=7)

    stopClickBtn = Button(clickFrame, text="Stop Clicking", bg="maroon", fg="white")
    stopClickBtn.grid(row=0, column=3, padx=7)

    return (
        clickFrame,
        repeatsEntry,
        repeatsTimeEntry,
        startClickBtn,
        stopClickBtn,
    )


def get_status_bar(root):
    status = Label(
        root,
        text="> Developed by hopeswiller<davidba941@gmail.com>",
        border=1,
        relief=SUNKEN,
        bg="maroon",
        fg="white",
        anchor=W,
        padx=5,
    )
    status.pack(side=BOTTOM, fill=X)
    return status
