import pymysql

class Book:
    def __init__(self, title='', author='', price=0, publisher='', edition='', number_of_pages=0):
        self.title = title
        self.author = author
        self.price = price
        self.publisher = publisher
        self.edition = edition
        self.number_of_pages = number_of_pages

    def __str__(self):
        return f'Title={self.title}, Author={self.author}, Price={self.price}, Publisher={self.publisher}, Edition={self.edition}, Pages={self.number_of_pages}'

class BookOperations:
    def connect_db(self):
        try:
            connection = pymysql.Connect(host='localhost',user='root',password='Ruchi@2004',database='ruchitha_db',port=3306)
            return connection
        except:
            print('Database connection failed')
            return None

    def disconnect_db(self, connection):
        if connection:
            connection.close()
            print('Database disconnected')

    def create_row(self, book: Book):
        query = '''INSERT INTO books(title, author, price, publisher, edition, number_of_pages) VALUES(%s, %s, %s, %s, %s, %s)'''
        connection = self.connect_db()
        cursor = connection.cursor()
        cursor.execute(query, (book.title, book.author, book.price, book.publisher, book.edition, book.number_of_pages))
        connection.commit()
        book_id = cursor.lastrowid
        cursor.close()
        self.disconnect_db(connection)
        return book_id

    def update_row(self, book_data: tuple):
        query = '''UPDATE books SET title=%s, author=%s, price=%s, publisher=%s, edition=%s, number_of_pages=%s WHERE id=%s'''
        connection = self.connect_db()
        cursor = connection.cursor()
        count = cursor.execute(query, book_data)
        connection.commit()
        cursor.close()
        self.disconnect_db(connection)
        return count

    def delete_row(self, id: int):
        query = 'DELETE FROM books WHERE id = %s'
        connection = self.connect_db()
        cursor = connection.cursor()
        count = cursor.execute(query, (id,))
        connection.commit()
        cursor.close()
        self.disconnect_db(connection)
        return count

    def search_row(self, id: int):
        query = 'SELECT * FROM books WHERE id = %s'
        connection = self.connect_db()
        cursor = connection.cursor()
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        cursor.close()
        self.disconnect_db(connection)
        return row

    def list_all_rows(self):
        query = 'SELECT * FROM books'
        connection = self.connect_db()
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        self.disconnect_db(connection)
        return rows

    def create_table(self):
        query = '''CREATE TABLE IF NOT EXISTS books(
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(50) NOT NULL,
            author VARCHAR(50),
            price INT NOT NULL,
            publisher VARCHAR(50),
            edition VARCHAR(50),
            number_of_pages INT
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
