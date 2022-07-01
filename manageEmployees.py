from sqlconnect import *
from tkinter import *
from tkinter import ttk


def show_manage_employee(managerframe,connect):
    global connection
    connection = connect
    employee_id = StringVar()
    global employeebox
    employeebox = ttk.Combobox(managerframe, textvariable= employee_id, state= "readonly")
    employeebox.grid(column=2, row=2, sticky=(E,W))
    global employee_list
    employee_list = employee_list_gen(connection)
    employeebox["value"] = employee_list
    def handle(event, connection = connection, employee_id = employee_id):
        populate_employee(connection, employee_id.get())
    employeebox.bind("<<ComboboxSelected>>", handle)
    
    ttk.Label(managerframe, text = "First Name = ").grid(column=1, row=3, sticky=(E))
    global entry_employee_fname 
    entry_employee_fname= StringVar()
    global fname_input
    fname_input = ttk.Entry(managerframe, textvariable=entry_employee_fname)
    fname_input.grid(column=2, row=3, sticky=(W))
    
    ttk.Label(managerframe, text = "ID = ").grid(column=1, row=4, sticky=(E))
    global entry_employee_id 
    entry_employee_id= StringVar()
    global id_input
    id_input = ttk.Entry(managerframe, textvariable=entry_employee_id)
    id_input.grid(column=2, row=4, sticky=(W))
    
    ttk.Label(managerframe, text = "Last Name = ").grid(column=3, row=3, sticky=(E))
    global entry_employee_lname
    entry_employee_lname= StringVar()
    global lname_input
    lname_input = ttk.Entry(managerframe, textvariable=entry_employee_lname)
    lname_input.grid(column=4, row=3, sticky=(W))
    
    ttk.Label(managerframe, text = "Pay = ").grid(column=3, row=4, sticky=(E))
    global entry_employee_pay 
    entry_employee_pay= StringVar()
    global pay_input
    pay_input = ttk.Entry(managerframe, textvariable=entry_employee_pay)
    pay_input.grid(column=4, row=4, sticky=(W))
    
    ttk.Button(managerframe, text="Delete", command=del_employee).grid(column=1,row=6,sticky=(E,W))
    ttk.Button(managerframe, text="Add", command=add_employee).grid(column=2,row=6,sticky=(E,W))
    ttk.Button(managerframe, text="Update", command=update_employee).grid(column=3,row=6,sticky=(E,W))
    
    for child in managerframe.winfo_children(): 
        child.grid_configure(padx=10, pady=10)
    
def populate_employee(connection, employee_id = ""):
    if employee_id != "":
        employee_name = employee_id.split()
        employee_id_number = employee_name[2]
        employee = get_employee(employee_id_number,connection)
        #print(employee)
        entry_employee_fname.set(employee["fname"])
        entry_employee_id.set(employee["id"])
        entry_employee_lname.set(employee["lname"])
        entry_employee_pay.set(employee["pay"])        
    
def del_employee():
    del_employee_db(entry_employee_id.get(),connection)
    clear_all

def add_employee():
    employee = {"id":entry_employee_id.get(), "fname":entry_employee_fname.get(), "lname": entry_employee_lname.get(), "pay":entry_employee_pay.get()}
    employee_add(connection,employee)
    clear_all

def update_employee():
    employee = {"id":entry_employee_id.get(), "fname":entry_employee_fname.get(), "lname": entry_employee_lname.get(), "pay":entry_employee_pay.get()}
    print(employee)
    update_employees_db(employee, connection)
    clear_all

def employee_list_gen(connection):
    employee_list = []
    for x in query_employees(connection):
        fullName = x[1] + " " + x[2] + " " + str(x[0])
        employee_list.append(fullName)
    employee_list.sort()
    return employee_list

def clear_all():
    employee_list = employee_list_gen(connection)
    employeebox["value"] = employee_list
    entry_employee_fname.set("")
    entry_employee_id.set("")
    entry_employee_lname.set("")
    entry_employee_pay.set("")
