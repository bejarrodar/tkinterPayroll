from sqlconnect import *
from tkinter import *
from tkinter import ttk
from operator import indexOf

def punch_control(managerframe, connect):
    global connection
    connection = connect
    
    global employee_id
    employee_id = StringVar()
    employeebox = ttk.Combobox(managerframe, textvariable= employee_id, state= "readonly")
    employeebox.grid(column=2, row=2, sticky=(E,W))
    employee_list = employee_list_gen()
    employeebox["value"] = employee_list
    employeebox.bind("<<ComboboxSelected>>", populate_employee)

    global punch_id
    global punchbox
    punch_id = StringVar()
    punchbox = ttk.Combobox(managerframe, textvariable= punch_id, state= "readonly")
    punchbox.grid(column=2,row=3,sticky=(W,E))
    punchbox.bind("<<ComboboxSelected>>", populate_punch)

    ttk.Label(managerframe, text = "Month: ").grid(column=1, row= 4, sticky=(E,W))
    global month_entry
    global month_value
    month_value = StringVar()
    month_entry = ttk.Entry(managerframe, textvariable=month_value)
    month_entry.grid(column=2, row= 4, sticky=(E,W))

    ttk.Label(managerframe, text = "Day: ").grid(column=3, row= 4, sticky=(E,W))
    global day_entry
    global day_value
    day_value = StringVar()
    day_entry = ttk.Entry(managerframe, textvariable=day_value)
    day_entry.grid(column=4, row= 4, sticky=(E,W))

    ttk.Label(managerframe, text = "Hour: ").grid(column=1, row= 5, sticky=(E,W))
    global hour_entry
    global hour_value
    hour_value = StringVar()
    hour_entry = ttk.Entry(managerframe, textvariable=hour_value)
    hour_entry.grid(column=2, row= 5, sticky=(E,W))

    ttk.Label(managerframe, text = "Minute: ").grid(column=3, row= 5, sticky=(E,W))
    global minute_entry
    global minute_value
    minute_value = StringVar()
    minute_entry = ttk.Entry(managerframe, textvariable=minute_value)
    minute_entry.grid(column=4, row= 5, sticky=(E,W))

    ttk.Button(managerframe, text="Delete", command=delete_punch).grid(column=1,row=6,sticky=(E,W))
    ttk.Button(managerframe, text="Add", command=add_punch).grid(column=2,row=6,sticky=(E,W))
    ttk.Button(managerframe, text="Update", command=update_punch).grid(column=3,row=6,sticky=(E,W))

    for child in managerframe.winfo_children(): 
        child.grid_configure(padx=10, pady=10)


def employee_list_gen():
    employee_list = []
    for x in query_employees(connection):
        fullName = x[1] + " " + x[2] + " " + str(x[0])
        employee_list.append(fullName)
    employee_list.sort()
    return employee_list

def populate_employee(event = None):
    global punch_id_list
    global punch_list
    punch_list = []
    punch_id_list = []
    punchbox.set(punch_list)
    employee_name = employee_id.get()
    employee_name = employee_name.split()
    global employee_id_number
    employee_id_number = employee_name[2]
    if employee_id_number != "":
        employee = query_punch(employee_id_number, connection)
        for i in range(len(employee)):
            punch_time = "{}/{} - {}:{}"
            if employee[i][5] < 10:
                minute = "0" + str(employee[i][5])
            else:
                minute = employee[i][5]
            punch_str = punch_time.format(employee[i][2], employee[i][3], employee[i][4], minute)
            punch_id_list.append(employee[i][0])
            punch_list.append(punch_str)
        punchbox["value"] = punch_list
    else:
        print("No employee Selected")
        
        
def populate_punch(event = None):
    #print(punch_list)
    #print(punch_id.get())
    global punch_id_number
    punch_id_number = punch_id_list[indexOf(punch_list, punch_id.get())]
    #print(punch_id_number)
    current_punch = get_punch(punch_id_number, connection)

    month_value.set(current_punch[0][2])
    day_value.set(current_punch[0][3])
    hour_value.set(current_punch[0][4])
    minute_value.set(current_punch[0][5])

def delete_punch():
    del_punch_db(punch_id_number, connection)

def update_punch():
    update = []
    update.append(punch_id_number)
    update.append(month_value.get())
    update.append(day_value.get())
    update.append(hour_value.get())
    update.append(minute_value.get())
    update_punch_db(update, connection)

def add_punch():
    update = []
    update.append(employee_id_number)
    update.append(month_value.get())
    update.append(day_value.get())
    update.append(hour_value.get())
    update.append(minute_value.get())
    punch_add(update, connection)