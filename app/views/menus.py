from flask import Blueprint
from flask_restful import reqparse
from app.controllers.menus import Menus
from app.controllers.users import Users

mod_menus = Blueprint('menus', __name__, url_prefix='/api/v2')

mnu = Menus()
usr = Users()


@mod_menus.route('/menus', methods=['POST'])
@usr.logged_in
@usr.check_admin
def create_menu(res=None, user_id=None, user_role=None):
    parser = reqparse.RequestParser()
    parser.add_argument('dish', type=str, location='json')
    parser.add_argument('price', type=int, location='json')
    parser.add_argument('description', type=str, location='json')
    data = parser.parse_args()

    return mnu.create_menu(data)


@mod_menus.route('/menus', methods=['GET'])
def get_menu():
    return mnu.get_menu()


@mod_menus.route('/menus/<id>', methods=['GET'])
@usr.logged_in
@usr.check_admin
def get_menus(id, res=None, user_id=None, user_role=None):
    return mnu.get_menus(id)
