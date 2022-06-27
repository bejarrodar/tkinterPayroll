from logging import root
from operator import indexOf
import threading
from tkinter import *
from tkinter import ttk
from datetime import datetime
from pyparsing import col
from sqlconnect import *
import time

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
        root.bind("<Return>", self.enter_time)
            
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
        root.bind("<Return>", self.manager_login)
        
        for child in self.managerframe.winfo_children(): 
            child.grid_configure(padx=10, pady=10)
  
    def manager_login(self):        #Attempts Login
        if login_manager(self.login_id.get(),self.login_password.get(),connect_sql) == True:
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
        self.managerframe.destroy()
        self.managerframe2 = ttk.Frame(self.branch, padding="3 3 12 12")
        self.managerframe2.grid(column=0, row=0, sticky=(N, W, E, S))
        
        manager = query_manager(self.login_id.get(), connect_sql)
        print(manager)
        self.welcome_message = "Welcome " + manager[0][0]
        ttk.Label(self.managerframe2, text=self.welcome_message).grid(column=1,row=1,sticky=(W))
        
        ttk.Button(self.managerframe2, text= "Change punch", command= self.punch_control).grid(column=2, row=2, sticky=(W, E))
        ttk.Button(self.managerframe2, text= "Manage Employees", command= self.manage_employee).grid(column=4, row=2, sticky=(W, E))
        ttk.Button(self.managerframe2, text= "View Reports", command= self.view_reports).grid(column=2, row=4, sticky=(W, E))
        ttk.Button(self.managerframe2, text= "Manage Managers", command= self.manage_manager).grid(column=4, row=4, sticky=(W, E))
        ttk.Button(self.managerframe2, text= "Logout", command= self.logout).grid(column=5, row=5, sticky=(W, E))
        
        for child in self.managerframe2.winfo_children(): 
            child.grid_configure(padx=10, pady=10)
        
    #=============================Punch Control Screen====================================================
        
    def punch_control(self):
        self.managerframe2.destroy()
        self.managerframe3 = ttk.Frame(self.branch, padding="3 3 12 12")
        self.managerframe3.grid(column=0, row=0, sticky=(N, W, E, S))
        
        ttk.Label(self.managerframe3, text=self.welcome_message).grid(column=1,row=1,sticky=(W))
        
        #ttk.Label(self.managerframe3, text = "Employee ID: ")
        self.employee_id = StringVar()
        employeebox = ttk.Combobox(self.managerframe3, textvariable= self.employee_id, state= "readonly")
        employeebox.grid(column=2, row=2, sticky=(E,W))
        employee_list = self.employee_list_gen()
        employeebox["value"] = employee_list
        #print(employee_list)
        self.punch_list = []
        employeebox.bind("<<ComboboxSelected>>", self.populate_employee)
        
        self.punch_id_list = []
        self.punch_id = StringVar()
        self.punchbox = ttk.Combobox(self.managerframe3, textvariable= self.punch_id, state= "readonly")
        self.punchbox.grid(column=2,row=3,sticky=(W,E))
        print(self.punch_list)
        self.punchbox.bind("<<ComboboxSelected>>", self.populate_punch)
        
        ttk.Label(self.managerframe3, text = "Month: ").grid(column=1, row= 4, sticky=(E,W))
        self.month_value = StringVar()
        self.month_entry = ttk.Entry(self.managerframe3, textvariable=self.month_value)
        self.month_entry.grid(column=2, row= 4, sticky=(E,W))
        
        ttk.Label(self.managerframe3, text = "Day: ").grid(column=3, row= 4, sticky=(E,W))
        self.day_value = StringVar()
        self.day_entry = ttk.Entry(self.managerframe3, textvariable=self.day_value)
        self.day_entry.grid(column=4, row= 4, sticky=(E,W))
        
        ttk.Label(self.managerframe3, text = "Hour: ").grid(column=1, row= 5, sticky=(E,W))
        self.hour_value = StringVar()
        self.hour_entry = ttk.Entry(self.managerframe3, textvariable=self.hour_value)
        self.hour_entry.grid(column=2, row= 5, sticky=(E,W))
        
        ttk.Label(self.managerframe3, text = "Minute: ").grid(column=3, row= 5, sticky=(E,W))
        self.minute_value = StringVar()
        self.minute_entry = ttk.Entry(self.managerframe3, textvariable=self.minute_value)
        self.minute_entry.grid(column=4, row= 5, sticky=(E,W))
        
        ttk.Button(self.managerframe3, text="Delete", command=self.delete_punch).grid(column=1,row=6,sticky=(E,W))
        ttk.Button(self.managerframe3, text="Add", command=self.add_punch).grid(column=2,row=6,sticky=(E,W))
        ttk.Button(self.managerframe3, text="Update", command=self.update_punch).grid(column=3,row=6,sticky=(E,W))
        
        for child in self.managerframe3.winfo_children(): 
            child.grid_configure(padx=10, pady=10)

        
    def employee_list_gen(self):
        employee_list = []
        for x in query_employees(connect_sql):
            fullName = x[1] + " " + x[2] + " " + str(x[0])
            employee_list.append(fullName)
        employee_list.sort()
        #print(employee_list)
        return employee_list
    
    def populate_employee(self,event):
        self.punch_list = []
        self.punch_id_list = []
        self.punchbox.set(self.punch_list)
        employee_name = self.employee_id.get()
        employee_name = employee_name.split()
        #print(employee_name)
        employee_id = employee_name[2]
        #print(employee_id)
        if employee_id != "":
            employee = query_punch(employee_id, connect_sql)
            print(employee)
            for i in range(len(employee)):
                #print(employee[i])
                punch_time = "{}/{} - {}:{}"
                punch_str = punch_time.format(employee[i][2], employee[i][3], employee[i][4], employee[i][5])
                self.punch_id_list.append(employee[i][0])
                self.punch_list.append(punch_str)
            self.punchbox["value"] = self.punch_list
            print(self.punch_list)
        else:
            print("No employee Selected")
            
            
    def populate_punch(self, event):
        print(self.punch_list)
        print(self.punch_id.get())
        self.punch_id_number = self.punch_id_list[indexOf(self.punch_list, self.punch_id.get())]
        print(self.punch_id_number)
        #ttk.Label(self.managerframe3,text = self.punch_id_number).grid(column=1,row=3,sticky=(W))
        self.current_punch = get_punch(self.punch_id_number, connect_sql)
        
        self.month_value.set(self.current_punch[0][2])
        self.day_value.set(self.current_punch[0][3])
        self.hour_value.set(self.current_punch[0][4])
        self.minute_value.set(self.current_punch[0][5])
    
    def delete_punch(self):
        
        return
    
    def update_punch(self):
        
        return
    
    def add_punch(self):
        
        return
    
    
    #==========================Manage Employee Screen=====================================================

    def manage_employee(self):
        return

    #==========================View Reports Screen===============================================================

    def view_reports(self):
        return

    #===========================Manage Managers Screen=====================================================

    def manage_manager(self):
        return
    
    def logout(self):       #closes manager control window and resets id and password
        self.login_id.set("")
        self.login_password.set("")
        self.branch.destroy()
        self.id_entry.focus()
        root.bind("<Return>", self.enter_time)
        
#========================Creates DB Tables======================================        
    
sql_location = "payroll.sqlite" 
connect_sql = create_connection(sql_location)

create_employee_table = """
CREATE TABLE IF NOT EXISTS employees (
  id INTEGER PRIMARY KEY,
  fName TEXT NOT NULL,
  lName TEXT NOT NULL,
  pay INTEGER
);
"""

print("Creating employee table")
execute_query(connect_sql, create_employee_table)

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

print("Creating punch table")
execute_query(connect_sql, create_punch_table)

create_manager_table = """
CREATE TABLE IF NOT EXISTS managers (
    id INTEGER PRIMARY KEY,
    fName TEXT NOT NULL,
    lName TEXT NOT NULL,
    password TEXT NOT NULL
);
"""

print("Creating manager table")
execute_query(connect_sql, create_manager_table)

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

print("filling test employee table")
execute_query(connect_sql, create_test_employees)

create_test_manager = """
INSERT INTO
    managers (id, fName, lName, password)
VALUES
    (1,'Dead','Pool','GunsAreG00d!');
"""

print("Creating test Manager")
execute_query(connect_sql, create_test_manager)

#================================Starting Loop============================================================

root = Tk()
MainWindow(root)
root.mainloop()