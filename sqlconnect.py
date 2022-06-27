from datetime import datetime
from multiprocessing import Manager
import sqlite3
from sqlite3 import Error
from xml.etree.ElementTree import tostring

 
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