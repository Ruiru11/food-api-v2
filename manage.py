import os
import psycopg2
from flask_script import Manager
from app import create_app, db

environment = os.getenv('ENV') or 'dev'
app = create_app(environment)

manager = Manager(app)


@manager.command
def run():
    app.run()


@manager.command
def init_db():
    try:
        print("CREATING TABLES")
        db.create_tables()
    except (Exception, psycopg2.DatabaseError) as error:
        print("FAILED TO CREATE TABLES", error)


@manager.command
def create_admin():
    try:
        print("CREATING ADMIN")
        db.create_admin()
    except (Exception, psycopg2.DatabaseError) as error:
        print("FAILED TO CREATE TABLES", error)


if __name__ == '__main__':
    manager.run()
