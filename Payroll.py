from tkinter import *
from tkinter import ttk
from datetime import datetime

class mainwondow:
    def __init__(self, root):
        
        root.title("Time Clock")
        
        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        ttk.Label(self.mainframe, text="Current Time: ").grid(column=1, row=1, sticky=E)
        ttk.Label(self.mainframe, text="Employee ID: ").grid(column=1, row=2, sticky=W)

        self.id_number = StringVar()
        ttk.Entry(self.mainframe, textvariable=self.id_number).grid(column=2, row=2, sticky=E)

        ttk.Button(self.mainframe,text="Manager Login", command=self.login).grid(column=3, row=3, sticky=(W, E))

        ttk.Button(self.mainframe,text="Punch Clock", command=self.time_entry).grid(column=1, row=3, sticky=(W, E))
        self.update_time()

        for child in self.mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
            
    def update_time(self, *args):
        current_time = (datetime.now().strftime("%H:%M:%S"))
        ttk.Label(self.mainframe, text=current_time).grid(column=2, row=1, sticky=W)
        for child in self.mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
        root.after(1000, self.update_time)

    def login():
        return

    def time_entry():
        return

    

root = Tk()
mainwondow(root)
root.mainloop()