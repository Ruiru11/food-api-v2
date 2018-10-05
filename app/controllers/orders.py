from flask import jsonify, make_response
from app.models.Database import Database_connection
import psycopg2
import uuid


class Orders(object):
    def __init__(self):
        self.connection = Database_connection()

    def create_order(self, data):
        get_meal = self.connection.cursor.execute(
            "SELECT * FROM meals WHERE  meal_id=%s ", [data['meal_id']])
        meal = self.connection.cursor.fetchone()
        print("meal>>>", meal)
        if meal:
            try:
                order_id = uuid.uuid4()

                self.connection.cursor.execute("""INSERT INTO ORDERS (order_id, status,
                                user_id, description, item, meal_id)
                VALUES (%s, %s, %s, %s, %s, %s);""",
                                               (str(order_id),
                                                'inprogress',
                                                data['user_id'],
                                                data['description'],
                                                data['item'], data['meal_id']))
                print("Inserting DATA into ORDERS")
                response_object = {
                    "satus": "pass",
                    "message": "order created succesfully"
                }
                return(make_response(jsonify(response_object)))

            except (Exception, psycopg2.DatabaseError) as error:
                print("ERROR inserting into ORDERS", error)
                response_object = {
                    "satus": "fail",
                    "message": "Problems while creating orders"
                }
                return(make_response(jsonify(response_object)))
        else:
            response_object = {
                "status": "fail",
                "message": "meal with given id does not exist"
            }
            return(make_response(jsonify(response_object)))

    def get_orders(self):
        self.connection.cursor.execute("""SELECT * FROM orders""")
        response = self.connection.cursor.fetchall()
        return(jsonify(response))

    def get_user_orders(self, id):
        self.connection.cursor.execute(
            "SELECT * FROM orders WHERE user_id=%s ", [id])
        response = self.connection.cursor.fetchall()
        return(jsonify(response))

    def get_order(self, id):
        self.connection.cursor.execute(
            " SELECT * FROM orders WHERE order_id=%s ", [id])
        response = self.connection.cursor.fetchone()
        return(make_response(jsonify(response)))

    def update_order(self, id):
        self.connection.cursor.execute(
            "UPDATE orders SET status='complete' WHERE order_id=%s", [id])
        response_object = {
            "satus": "pass",
            "message": "status update complete"
        }
        return(make_response(jsonify(response_object)))

    def delete_order(self, id):
        self.connection.cursor.execute(
            "DELETE FROM orders WHERE order_id=%s", [id]
        )
        response_object = {
            "satus": "pass",
            "message": "order deleted"
        }
        return(make_response(jsonify(response_object)))
