from flask import Blueprint
from flask_restful import reqparse
from app.controllers.users import Users

mod_users = Blueprint('users', __name__, url_prefix='/api/v2')

usr = Users()


@mod_users.route('/signup', methods=['POST'])
def signup():
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True,
                        help="Pease provide an email", location="json")
    parser.add_argument('address', type=str, required=True,
                        help="Pease provide an address", location="json")
    parser.add_argument('password', type=str, required=True,
                        help="Pease provide a password", location="json")
    parser.add_argument('username', type=str, required=True,
                        help="Pease provide username", location="json")
    data = parser.parse_args()
    return usr.create_user(data)


@mod_users.route('/signin', methods=['POST'])
def signin():
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True,
                        help="Pease provide an email", location="json")
    parser.add_argument('password', type=str, required=True,
                        help="Pease provide an password", location="json")
    data = parser.parse_args()
    return usr.sign_in(data)


@mod_users.route('/users', methods=['GET'])
@usr.logged_in
def get_users(user_id=None, res=None):
    print(usr.all_users())
    return usr.all_users()
