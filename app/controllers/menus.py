from flask import jsonify, make_response
from app.models.Database import Database_connection
import psycopg2
import uuid

class Menus(object):
    def __init__(self):
        self.connection = Database_connection()

    def create_menu(self,data):
        try:
            meal_id = str(uuid.uuid4())
            self.connection.cursor.execute("""INSERT INTO meals(meal_id, name, description)
            VALUES(%s, %s, %s);""",
                                (meal_id, data['name'], data['description']))
            print("INSERTING DATA into MEALS")
            response_object = {
                "status":""
            }
            return(make_response(jsonify(response_object)))
            
        except (Exception, psycopg2.DatabaseError) as error:
            print("ERROR inserting into meals", error)

    def get_menu(self):
        self.connection.cursor.execute(
            """SELECT * FROM meals"""
        )
        news = self.connection.cursor.fetchall()
        return(jsonify(news))
    
    def get_menus(self, id):
        self.connection.cursor.execute(
            "SELECT * FROM  meals WHERE meal_id=%s",[id]
        )
        news = self.connection.cursor.fetchone()
        return(make_response(jsonify(news)))