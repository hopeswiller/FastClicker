from tkinter import *

# main window or root widget
root = Tk()

myLabel = Label(
    root,
    text="Hello World Testing tkinter!",
)

myLabel2 = Label(
    root,
    text="Its been fun so far!",
)

# myLabel.pack()
myLabel.grid(row=0, column=0)
myLabel2.grid(row=2, column=0)

root.mainloop()
