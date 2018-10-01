import psycopg2
from app.models.tables import commands
from app import bcrypt
import uuid

class Database_connection():
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                "dbname='ruiru' user='ruiru' password='ruiru' host='localhost' port='5432'"
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print("CANNOT CONNECT TO DATABASE INVALID DATABASE URL",error)

    def create_tables(self):
        for command in commands:
            self.cursor.execute(command)
    
    def create_admin(self):
        user_id=uuid.uuid4()
        encrypted_password = bcrypt.generate_password_hash('adminpassword', 12).decode("utf-8")
        self.cursor.execute("""INSERT INTO users(id, email, username, password, address, role)
        VALUES(%s,%s,%s, %s, %s, %s);""",
        (str(user_id), 'admin@mail.com', 'master', encrypted_password, 'utawala', 'admin' ))
