from datetime import datetime
import sqlite3
from sqlite3 import Error

 
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred on create")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred on execute")
        
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred on read") 
        
def time_entry(value, connect_sql):
        print(value)
        select_employee = ("SELECT id FROM employees WHERE id=" + value)
        employee = execute_read_query(connect_sql, select_employee)
        print(employee)
        if employee != []:
            try:
                
                current_time = datetime.now()
                day = current_time.strftime("%d")
                month = current_time.strftime("%m")
                hour = current_time.strftime("%H")
                minute = current_time.strftime("%M")
                punch = """
                INSERT INTO 
                    punches (employeeID, punchMonth, punchDay, punchHour, punchMinute)
                VALUES
                    (""" + value + ", " + month + ", " + day + ", " + hour + ", " + minute + """);
                """
                execute_query(connect_sql, punch)
                return True 
            except ValueError:
                pass
        else:
            return False
        
def login_manager(login, password, connection):
    print("Login attempt with id: " + login)
    select_manager = ("SELECT id, password FROM managers WHERE id=" + login)
    manager = execute_read_query(connection, select_manager)
    test = [(int(login), password)]
    print(manager)
    print(test)
    if manager !=[]:
        if manager == test:
            return True
        else:
            return False
    else:
        return False 
    
def query_manager(id, connection):
    manager_get = ("SELECT fName, lName FROM managers WHERE id=" + id)
    manager = execute_read_query(connection, manager_get)
    return manager

def query_employees(connection):
    employees_get = ("SELECT * FROM employees")
    employees = execute_read_query(connection, employees_get)
    return employees

def query_punch(id,connection):
    employee_get = ("SELECT * FROM punches WHERE employeeID=" + id)
    employee = execute_read_query(connection, employee_get)
    return employee

def get_punch(id, connection):
    punch_get = ("SELECT * FROM punches WHERE id=" +str(id))
    punch = execute_read_query(connection, punch_get)
    return punch

def del_punch_db(id, connection):
    punch_del = ("DELETE FROM punches WHERE id=" + str(id))
    execute_query(connection, punch_del)
    
def update_punch_db(update, connection): #update is (id, punchMonth, punchDay, punchHour, punchMinute)
    punch_update = """
                    UPDATE
                        punches
                    SET
                        punchMonth = {1},
                        punchDay = {2},
                        punchHour = {3},
                        punchMinute = {4}
                    WHERE
                        id = {0}
                    """
    punch_update_str = punch_update.format(update[0], update[1], update[2], update[3], update[4])
    print(punch_update_str)
    execute_query(connection, punch_update_str)
    
def punch_add(list, connection): #list is (employeeID, punchMonth, punchDay, punchHour, punchMinute)
    punch = """
            INSERT INTO 
                punches (employeeID, punchMonth, punchDay, punchHour, punchMinute)
            VALUES
                ({0}, {1}, {2}, {3}, {4});
            """
    punch_added = punch.format(list[0], list[1], list[2], list[3], list[4])
    print(punch_added)
    execute_query(connection, punch_added)
    
def get_employee(id, connection):
    query = ("SELECT * FROM employees WHERE id=" +str(id))
    output = execute_read_query(connection, query)
    out_id = output[0][0]
    out_fname = output[0][1]
    out_lname = output[0][2]
    out_pay = output[0][3]
    employee = {"id":out_id, "fname":out_fname, "lname": out_lname, "pay":out_pay}
    return employee

def del_employee_db(id, connection):
    employee_del = ("DELETE FROM employees WHERE id=" + str(id))
    execute_query(connection, employee_del)
    
def employee_add(connection, employee):
    change = """
            INSERT INTO 
                employees (id, fname, lname, pay)
            VALUES
                ({0}, '{1}', '{2}', {3});
            """
    changed = change.format(employee["id"], employee["fname"], employee["lname"], employee["pay"])
    print(changed)
    execute_query(connection, changed)
    
def update_employees_db(employee, connection): 
    employee_update = """
                    UPDATE
                        employees
                    SET
                        fName = '{1}',
                        lName = '{2}',
                        pay = {3}
                    WHERE
                        id = {0}
                    """
    employee_update_str = employee_update.format(employee["id"], employee["fname"], employee["lname"], employee["pay"])
    print(employee_update_str)
    execute_query(connection, employee_update_str)