from flask import jsonify, make_response
from app.models.Database import Database_connection
import psycopg2
import uuid


class Menus(object):
    def __init__(self):
        self.connection = Database_connection()

    def create_menu(self, data):
        try:
            meal_id = str(uuid.uuid4())
            self.connection.cursor.execute("""INSERT INTO meals(meal_id, dish, description, price)
            VALUES(%s, %s, %s, %s);""",
                                           (meal_id,
                                            data['dish'],
                                            data['description'],
                                            data['price']))
            print("INSERTING DATA into MEALS")
            response_object = {
                "status": "Item Added to Menu "
            }
            return(make_response(jsonify(response_object)), 403)

        except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                response_object = {
                    "status": "fail",
                    "message": "dish already exists"
                }
                return(make_response(jsonify(response_object)))

    def get_menu(self):
        self.connection.cursor.execute(
            """SELECT * FROM meals"""
        )
        news = self.connection.cursor.fetchall()
        return(jsonify(news))

    def get_menus(self, id):
        print('id', id)
        self.connection.cursor.execute(
            "SELECT * FROM  meals WHERE meal_id=%s", [id]
        )
        news = self.connection.cursor.fetchone()
        return(make_response(jsonify(news)))
