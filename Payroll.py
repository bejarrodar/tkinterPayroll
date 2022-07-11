#====================================================================Imports===========================================================
from logging import root
import threading
from tkinter import *
from tkinter import ttk
from datetime import datetime
from sqlconnect import *
import time
from manageEmployees import *
from punchControl import *
from manageManagers import *
from viewReports import *
import hashlib

class MainWindow:
    def __init__(self, root):
        
        #======================================================Time Punch Screen========================================================
        
        root.title("Time Clock")
        
        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        ttk.Label(self.mainframe, text="Current Time: ").grid(column=1, row=1, sticky=E)
        ttk.Label(self.mainframe, text="Employee ID: ").grid(column=1, row=2, sticky=W)
        
        self.found = ""
        self.id_number = StringVar()
        self.id_entry = ttk.Entry(self.mainframe, textvariable=self.id_number)
        self.id_entry.grid(column=2, row=2, sticky=E)

        ttk.Button(self.mainframe,text="Manager Login", command= self.login_btn).grid(column=3, row=3, sticky=(W, E))
        self.punch_label = ttk.Label(self.mainframe, text=self.found)
        self.punch_label.grid(column=2, row=3, sticky=W)
        ttk.Button(self.mainframe,text="Punch Clock", command= self.enter_time).grid(column=1, row=3, sticky=(W, E))
        
        self.update_labels()

        for child in self.mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
            
        self.id_entry.focus()
        self.id_entry.bind("<Return>", self.enter_time)
            
    def update_labels(self):            #updates time on punch screen
        current_time = (datetime.now().strftime("%H:%M:%S"))
        ttk.Label(self.mainframe, text=current_time).grid(column=2, row=1, sticky=W)
        for child in self.mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
        root.after(1000, self.update_labels)        

    def enter_time(self, *args):        #Attempts to enter punch to DB
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
            
    def punch_success(self):        #brings up self closing success screen
        top= Toplevel(root)
        top.geometry("250x250")
        top.title("Punch Succeded")
        success_popup = ttk.Label(top, text= self.found, font=('Mistral 12 bold'))
        success_popup.place(x=10,y=80)
        time.sleep(3)
        top.destroy()
        
    def punch_failed(self):          #brings up self closing failure screen
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

    #===================================Login Screen==============================================
    
    def login(self):

        self.branch= Toplevel(root)
        self.branch.geometry("750x750")
        self.branch.title("Manager Control")
       
        self.managerframe = ttk.Frame(self.branch, padding="3 3 12 12")
        self.managerframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.managerframe.place(x=10,y=10)
        
        ttk.Label(self.managerframe, text="Manager ID: ").grid(column=3, row=3, sticky=(E))
        
        self.login_id = StringVar()
        manager_id = ttk.Entry(self.managerframe,textvariable=self.login_id)
        manager_id.grid(column=4, row=3, sticky=(W, E))
        
        ttk.Label(self.managerframe, text= "Manager Password: ").grid(column=3, row=5, sticky=(E))
        
        self.login_password = StringVar()
        manager_password = ttk.Entry(self.managerframe, textvariable=self.login_password, show="*")
        manager_password.grid(column=4, row=5, sticky=(W, E))
        
        ttk.Button(self.managerframe, text= "Login", command= self.manager_login).grid(column=2, row=7, sticky=(W, E))
        ttk.Button(self.managerframe, text= "Exit", command= self.manager_exit).grid(column=6, row=7, sticky=(W, E))
        
        manager_id.focus()
        manager_password.bind("<Return>", self.manager_login)
        
        for child in self.managerframe.winfo_children(): 
            child.grid_configure(padx=10, pady=10)
  
    def manager_login(self,event = None):       #Attempts Login
        p = self.login_password.get()
        password = hashlib.sha256()
        password.update(p.encode())
        if login_manager(self.login_id.get(),password.hexdigest(),connect_sql) == True:
            self.login_password.set("")
            print("login succeeded")
            self.manager_control()
        else:
            print("login failed")

    def manager_exit(self):     #Exits Manager Window
        self.branch.destroy()
        self.id_entry.focus()
        root.bind("<Return>", self.enter_time)
        
    #====================================================Manager Control Screen==================================================
        
    def manager_control(self):
        for child in self.managerframe.winfo_children(): 
            child.destroy()
        self.managerframe = ttk.Frame(self.branch, padding="3 3 12 12")
        self.managerframe.grid(column=0, row=0, sticky=(N, W, E, S))
        
        manager = query_manager(self.login_id.get(), connect_sql)
        print(manager)
        self.welcome_message = "Welcome " + manager[0][0]
        ttk.Label(self.managerframe, text=self.welcome_message).grid(column=1,row=1,sticky=(W))
        
        ttk.Button(self.managerframe, text= "Change punch", command= self.punch_control).grid(column=2, row=2, sticky=(W, E))
        ttk.Button(self.managerframe, text= "Manage Employees", command= self.manage_employee).grid(column=4, row=2, sticky=(W, E))
        ttk.Button(self.managerframe, text= "View Reports", command= self.view_reports).grid(column=2, row=4, sticky=(W, E))
        ttk.Button(self.managerframe, text= "Manage Managers", command= self.manage_manager).grid(column=4, row=4, sticky=(W, E))
        ttk.Button(self.managerframe, text= "Logout", command= self.logout).grid(column=5, row=5, sticky=(W, E))
        
        for child in self.managerframe.winfo_children(): 
            child.grid_configure(padx=10, pady=10)
        
    #=============================Punch Control Screen====================================================
        
    def punch_control(self):
        for child in self.managerframe.winfo_children(): 
            child.destroy()
        ttk.Label(self.managerframe, text=self.welcome_message).grid(column=1,row=1,sticky=(W))
        punch_control(self.managerframe,connect_sql)
    
    #==========================Manage Employee Screen=====================================================

    def manage_employee(self):
        for child in self.managerframe.winfo_children(): 
            child.destroy()
        ttk.Label(self.managerframe, text=self.welcome_message).grid(column=1,row=1,sticky=(W))
        show_manage_employee(self.managerframe, connect_sql)

    #==========================View Reports Screen===============================================================

    def view_reports(self):
        for child in self.managerframe.winfo_children(): 
            child.destroy()
        ttk.Label(self.managerframe, text=self.welcome_message).grid(column=1,row=1,sticky=(W))
        
        show_reports(self.managerframe,connect_sql)

    #===========================Manage Managers Screen=====================================================

    def manage_manager(self):
        for child in self.managerframe.winfo_children(): 
            child.destroy()
        ttk.Label(self.managerframe, text=self.welcome_message).grid(column=1,row=1,sticky=(W))
        
        manager_control()
        
    
    def logout(self):       #closes manager control window and resets id and password
        self.login_id.set("")
        self.login_password.set("")
        self.branch.destroy()
        self.id_entry.focus()
        
#========================Creates DB Tables======================================        
    
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

#=======================Filling Test DB=============================================

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
    (1,'Dead','Pool','{}');
"""
test_password = "GunsAreG00d!"
test_hash = hashlib.sha256()
test_hash.update(test_password.encode())
test_manager = create_test_manager.format(test_hash.hexdigest())
print(test_manager)

#================================Starting Loop============================================================

sql_location = "payroll.sqlite" 
connect_sql = create_connection(sql_location)
execute_query(connect_sql, create_employee_table)
execute_query(connect_sql, test_manager)
execute_query(connect_sql, create_test_employees)
execute_query(connect_sql, create_manager_table)
execute_query(connect_sql, create_punch_table)

root = Tk()
MainWindow(root)
root.mainloop()