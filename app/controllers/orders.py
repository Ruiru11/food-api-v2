from flask import jsonify, make_response
from app.models.Database import Database_connection
import psycopg2
import uuid


class Orders(object):
    def __init__(self):
        self.connection = Database_connection()

    def create_order(self, data):
        try:
            order_id = uuid.uuid4()
            self.connection.cursor.execute("""INSERT INTO ORDERS (order_id, status,
                            user_id, cost, description, item) 
            VALUES (%s, %s, %s, %s, %s, %s);""",
                                           (str(order_id),
                                            'inprogress',
                                            data['user_id'],
                                            data['cost'], data['description'],
                                            data['item']))
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
                "message": "cannto"
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
