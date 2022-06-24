from tkinter import *
from tkinter import ttk
from datetime import datetime
from xml.etree.ElementTree import tostring


root = Tk()
root.title("Time Clock")
def update_time():
    current_time = (datetime.now().strftime("%H:%M:%S"))
    ttk.Label(mainframe, text=current_time).grid(column=2, row=1, sticky=W)
    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)
    root.after(1000, update_time)

def login():
    return

def time_entry():
    return


mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Label(mainframe, text="Current Time: ").grid(column=1, row=1, sticky=E)
ttk.Label(mainframe, text="Employee ID: ").grid(column=1, row=2, sticky=W)

id_number = StringVar()
ttk.Entry(mainframe, textvariable=id_number).grid(column=2, row=2, sticky=E)

ttk.Button(mainframe,text="Manager Login", command=login).grid(column=3, row=3, sticky=(W, E))

ttk.Button(mainframe,text="Punch Clock", command=time_entry).grid(column=1, row=3, sticky=(W, E))
update_time()

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

root.after(1000, update_time)
root.mainloop()