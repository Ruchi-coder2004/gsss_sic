import pymysql

class Person:
    def __init__(self, name='', gender='', age=0, location=''):
        self.name = name
        self.gender = gender
        self.age = age
        self.location = location

    def __str__(self):
        return f'Name = {self.name}, Gender = {self.gender}, Age = {self.age}, Location = {self.location}'
    
class Person_operations:
    def connect_db(self):
        try:
            connection = pymysql.Connect(host='localhost', user = 'root', password = 'Ruchi@2004', database = 'ruchitha_db', port = 3306)
            return connection
        except:
            print('Database Connection Failed')
            return None
        
    def disconnect_db(self, connection):
        if connection:
            connection.close()
            print('Database Disconnected')

    def create_row(self, person: Person):
        query = '''Insert into person(name, gender, age, location) Values (%s, %s, %s, %s)'''
        connection = self.connect_db()
        cursor = connection.cursor()
        cursor.execute(query,(person.name,person.gender,person.age,person.location))
        connection.commit()
        person_id_inserted_last = cursor.lastrowid
        cursor.close()
        self.disconnect_db(connection)
        return person_id_inserted_last
    
    def updated_row(self, book_data : tuple):
        query = 'Update person Set name = %s, gender = %s, age = %s, location = %s'
        connection = self.connect_db()
        cursor = connection.cursor()
        count = cursor.execute(query,book_data)
        connection.commit()
        cursor.close()
        self.disconnect_db(connection)
        return count

    def delete_row(self, id: int):
        query = 'DELETE FROM person WHERE id = %s'
        connection = self.connect_db()
        cursor = connection.cursor()
        count = cursor.execute(query, (id,))
        connection.commit()
        cursor.close()
        self.disconnect_db(connection)
        return count

    def search_row(self, id: int):
        query = 'SELECT * FROM person WHERE id = %s'
        connection = self.connect_db()
        cursor = connection.cursor()
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        cursor.close()
        self.disconnect_db(connection)
        return row

    def list_all_rows(self):
        query = 'SELECT * FROM person'
        connection = self.connect_db()
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        self.disconnect_db(connection)
        return rows

    def create_table(self):
        query = '''CREATE TABLE IF NOT EXISTS person(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            gender VARCHAR(50),
            age int,
            location VARCHAR(50)
        )'''
        connection = self.connect_db()
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()
        self.disconnect_db(connection)

    def create_database(self, db_name="ruchitha_db"):
        query = f'CREATE DATABASE IF NOT EXISTS {db_name}'
        connection = self.connect_db()
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()
        self.disconnect_db(connection)    


    
    

