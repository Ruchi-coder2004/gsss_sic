import db_connect as db

def read_employee_details():
    name = input('Enter Employee Name: ')
    designation = input('Enter Employee designation: ')
    phone_number = input('Enter Employee designation: ')
    commission = input('Enter Employee commision: ')
    salary = input('Enter Employee salary: ')
    years_of_exp = input('Enter Employee years_of_exp: ')
    location = input('Enter Employee location: ')

    return (name, designation, phone_number, commission, salary, years_of_exp, location)

def create_row():
    employee = read_employee_details()
    query = 'insert into employee(name, designation, phone_number, commission, salary, years_of_exp, location) values (%s %s %s %s %s %s %s);'
    connection = db.connect_db
    cursor = connection.cursor()
    count = cursor.execute(query,employee)# here employee is the tuple, from tuple it will assign it to place holder
    if count == 1:
        print('Row inserted')
    else:
        print('Row insertion Failed')

def update_row():
    query = 'update employee set location = %s, sala'

def delete_row():
    pass

def search_row():
    pass

def list_all_rows():
    pass

def create_table():
    query = '''
            create table if not exists employee(id int auto_increment primary key, name varchar(50) not null, designation varchar(50), phone_number bigint unique not null, commission float default(0), salary float check(salary >= 15000), years_of_exp tinyint, location varchar(50));
        '''
    connection = db.connect_db()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()
        db.disconnect_db(connection)
    except:
        print('Table creation Failed')

def create_database():
    db_name = input('Enter the database name: ')
    query = f'create database if not exists {db_name}'
    connection = db.connect_db()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()
        db.disconnect_db(connection)
    except:
        print('Database creation Failed')