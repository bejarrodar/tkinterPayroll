from logging import root
import threading
from tkinter import *
from tkinter import ttk
from datetime import datetime
import tkinter
from sqlconnect import *
import time

class MainWindow:
    def __init__(self, root):
        
        root.title("Time Clock")
        
        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        ttk.Label(self.mainframe, text="Current Time: ").grid(column=1, row=1, sticky=E)
        ttk.Label(self.mainframe, text="Employee ID: ").grid(column=1, row=2, sticky=W)
        
        self.found = ""
        self.id_number = StringVar()
        id_entry = ttk.Entry(self.mainframe, textvariable=self.id_number)
        id_entry.grid(column=2, row=2, sticky=E)

        ttk.Button(self.mainframe,text="Manager Login", command= self.login_btn).grid(column=3, row=3, sticky=(W, E))
        self.punch_label = ttk.Label(self.mainframe, text=self.found)
        self.punch_label.grid(column=2, row=3, sticky=W)
        ttk.Button(self.mainframe,text="Punch Clock", command= self.enter_time).grid(column=1, row=3, sticky=(W, E))
        
        self.update_labels()

        for child in self.mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
            
        id_entry.focus()
        root.bind("<Return>", self.enter_time)
            
    def update_labels(self):
        current_time = (datetime.now().strftime("%H:%M:%S"))
        ttk.Label(self.mainframe, text=current_time).grid(column=2, row=1, sticky=W)
        for child in self.mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
        ###self.punch_label.state(["disabled"])
        root.after(1000, self.update_labels)        

    def enter_time(self, *args):
        if self.id_number.get() != "":
            value = time_entry(self.id_number.get(), connect_sql)
            if value == True:
                self.found = (self.id_number.get() + " punched at " + datetime.now().strftime("%H:%M"))
                self.id_number.set("")
                s = threading.Thread(target=self.punch_success)
                s.start()
            else:
                self.found = ("Employee " + self.id_number.get() + " not found")
                self.id_number.set("")
                f = threading.Thread(target=self.punch_failed)
                f.start()
                
            print(self.found)
        else:
            print("Empty id passed")
            
    def punch_success(self):
        top= Toplevel(root)
        top.geometry("250x250")
        top.title("Punch Succeded")
        success_popup = ttk.Label(top, text= self.found, font=('Mistral 12 bold'))
        success_popup.place(x=10,y=80)
        time.sleep(3)
        top.destroy()
        
    def punch_failed(self):
        top= Toplevel(root)
        top.geometry("250x250")
        top.title("Punch Failed")
        fail_popup = ttk.Label(top, text= self.found, font=('Mistral 12 bold'))
        fail_popup.place(x=10,y=80)
        time.sleep(3)
        top.destroy()
    
    def login_btn(self):
        self.id_number.set("")
        l = threading.Thread(target=self.login)
        l.start()

    
    def login(self):

        self.branch= Toplevel(root)
        self.branch.geometry("550x550")
        self.branch.title("Manager Login")
       
        managerframe = ttk.Frame(self.branch, padding="3 3 12 12")
        managerframe.grid(column=0, row=0, sticky=(N, W, E, S))
        managerframe.place(x=10,y=10)
        
        ttk.Label(managerframe, text="Manager ID: ").grid(column=3, row=3, sticky=(E))
        
        self.login_id = StringVar()
        manager_id = ttk.Entry(managerframe,textvariable=self.login_id)
        manager_id.grid(column=4, row=3, sticky=(W, E))
        
        ttk.Label(managerframe, text= "Manager Password: ").grid(column=3, row=5, sticky=(E))
        
        self.login_password = StringVar()
        manager_password = ttk.Entry(managerframe, textvariable=self.login_password)
        manager_password.grid(column=4, row=5, sticky=(W, E))
        
        ttk.Button(managerframe, text= "Login", command= self.manager_login).grid(column=2, row=7, sticky=(W, E))
        ttk.Button(managerframe, text= "Exit", command= self.manager_exit).grid(column=6, row=7, sticky=(W, E))
        
        for child in managerframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
  
    def manager_login(self):
        if login_manager(self.login_id.get(),self.login_password.get(),connect_sql) == True:
            print("login succeeded")
        else:
            print("login failed")

    def manager_exit(self):
        self.branch.destroy()
        
    
    

create_employee_table = """
CREATE TABLE IF NOT EXISTS employees (
  id INTEGER PRIMARY KEY,
  fName TEXT NOT NULL,
  lName TEXT NOT NULL,
  pay INTEGER
);
"""

create_punch_table = """
CREATE TABLE IF NOT EXISTS punches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employeeID INTEGER NOT NULL,
    punchMonth INTEGER NOT NULL,
    punchDay INTEGER NOT NULL,
    punchHour INTEGER NOT NULL,
    punchMinute INTEGER NOT NULL,
    FOREIGN KEY (employeeID) REFERENCES employees (id)
);
"""

create_manager_table = """
CREATE TABLE IF NOT EXISTS managers (
    id INTEGER PRIMARY KEY,
    fName TEXT NOT NULL,
    lName TEXT NOT NULL,
    password TEXT NOT NULL
);
"""

create_test_employees = """
INSERT INTO
  employees (id, fName, lName, pay)
VALUES
  (123456, 'Mickey', 'Mouse', 9.50),
  (654321, 'Jane', 'Smith', 10.50),
  (123654, 'Tarzan', 'Gorilla', 9.25),
  (321456, 'Bob', 'Builder', 12.30),
  (456123, 'Jack', 'Beanstalk', 9.00);
"""
create_test_manager = """
INSERT INTO
    managers (id, fName, lName, password)
VALUES
    (1,'Dead','Pool','GunsAreG00d!');
"""



sql_location = "payroll.sqlite" 
connect_sql = create_connection(sql_location)
print("Creating employee table")
execute_query(connect_sql, create_employee_table)
print("filling test employee table")
execute_query(connect_sql, create_test_employees)
print("Creating manager table")
execute_query(connect_sql, create_manager_table)
print("Creating punch table")
execute_query(connect_sql, create_punch_table)
print("Creating test Manager")
execute_query(connect_sql, create_test_manager)


root = Tk()
MainWindow(root)
root.mainloop()