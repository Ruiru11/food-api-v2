from flask import jsonify, make_response, request
import os
import datetime
import jwt
from app.models.Database import Database_connection
from functools import wraps
import psycopg2
import uuid
from app import bcrypt

class Users(object):
    def __init__(self):
        self.connection = Database_connection()
    
    def create_user(self, data):
        try:
            user_id=uuid.uuid4()
            print(data)
            encrypted_password = bcrypt.generate_password_hash(data['password'], 12).decode("utf-8")
            self.connection.cursor.execute("""INSERT INTO users(id, email, username, password, address, role)
            VALUES(%s,%s,%s, %s, %s, %s);""",
            (str(user_id), data['email'], data['username'], encrypted_password, data['address'], 'user' ))
            print("Inserting data into users")
            response_object = {
                "status":"pass",
                "message":"user added succesfuly"
            }
            return(make_response(jsonify(response_object)))
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            response_object = {
                "status":"fail",
                "message":"Entry with same id already exists or wrong format used"
            }
            return(make_response(jsonify(response_object)))
    
    def all_users(self):
        self.connection.cursor.execute("""SELECT * FROM users""")
        users = self.connection.cursor.fetchall()
        for user in users:
            return(jsonify(users))
    
    def sign_in(self, data):
        self.connection.cursor.execute(
            " SELECT * FROM users WHERE email=%s ", [data['email']])
        user = self.connection.cursor.fetchone()
        if not user:
            response = {
                'status': 'fail',
                'message': 'Email used is not registered'
            }
            return(make_response(jsonify(response)))
        else:
            check_hash = bcrypt.check_password_hash(
                user[3],data['password']
            )
            if check_hash is True:
                user_id = user[0]

                token = self.generate_token(str(user_id), user[1], user[5])
                response = {
                    'status': 'success',
                    'message': 'Sign in successful',
                    'token': str(token)
                }
                return(make_response(jsonify(response)))
            else:
                response = {
                    'status': 'fail',
                    'message':'Please check your password'
                }
                return(make_response(jsonify(response)))
                
    def generate_token(self, id, username, role):
        """Generate authentication token."""
        payload = {
            'exp': datetime.datetime.now() + datetime.timedelta(seconds=9000),
            'iat': datetime.datetime.now(),
            'sub': id,
            'username': username,
            'role': role
        }
        return jwt.encode(
            payload,
            'qwertyuiop',
            algorithm='HS256'
        ).decode("utf-8")

    def logged_in(self, func):
        @wraps(func)
        def decorator(*args, **kwargs):
            try:
                token = request.headers.get('Authorization')
                payload = jwt.decode(token, 'qwertyuiop')
                user_id = payload['sub']
                self.connection.cursor.execute(
                    " SELECT * FROM users WHERE id=%s ", [user_id])
                user = self.connection.cursor.fetchone()
                if user:
                    responseObject = {
                        'staus': 'sucess',
                        'message': 'user logged in'
                    }
                    new_kwargs = {
                        'res': responseObject,
                        'user_id': user[0]
                    }
                    kwargs.update(new_kwargs)
                else:
                    responseObject = {
                        'status': 'fail',
                        'message': 'User not found'
                    }
                    new_kwargs = {
                        'res': responseObject,
                        'user_id': None
                    }
                    kwargs.update(new_kwargs)
            except jwt.ExpiredSignatureError:
                responseObject = {
                    'status': 'Fail',
                    'message': 'Token expired please login'
                }
                return make_response(jsonify(responseObject),401)
            except jwt.InvalidTokenError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Invalid token, please log in'
                }
                return make_response(jsonify(responseObject), 401)
            return func(*args, **kwargs)
        return decorator