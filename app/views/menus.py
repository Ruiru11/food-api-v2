from flask import Blueprint
from flask_restful import reqparse
from app.controllers.menus import Menus
from app.controllers.users import Users

mod_menus = Blueprint('menus', __name__, url_prefix='/api/v2')

mnu = Menus()
usr = Users()


@mod_menus.route('/menus', methods=['POST'])
@usr.logged_in
def create_menu(res=None, user_id=None):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, location='json')
    parser.add_argument('description', type=str, location='json')
    data = parser.parse_args()

    return mnu.create_menu(data)


@mod_menus.route('/menus', methods=['GET'])
@usr.logged_in
def get_menu(res=None, user_id=None):
    return mnu.get_menu()


@mod_menus.route('/menus/<int:id>', methods=['GET'])
@usr.logged_in
def get_menus(id):
    return mnu.get_menus(id)
