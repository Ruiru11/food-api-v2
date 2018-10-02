from flask import Blueprint
from flask_restful import reqparse
from app.controllers.orders import Orders
from app.controllers.users import Users

order_instance = Orders()
usr = Users()


mod_orders = Blueprint('orders', __name__, url_prefix='/api/v2')


@mod_orders.route('/orders', methods=['POST'])
@usr.logged_in
def create_order(res=None, user_id=None):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=int, location="json")
    parser.add_argument('item', type=str, location="json")
    parser.add_argument('order_id', type=int, location="json")
    parser.add_argument('description', type=str, location="json")
    parser.add_argument('cost', type=int, location="json")
    data = parser.parse_args()

    return order_instance.create_order(data)


@mod_orders.route('/orders', methods=['GET'])
@usr.logged_in
def get_orders(res=None, user_id=None):
    return order_instance.get_orders()


@mod_orders.route('/orders/<int:id>', methods=['GET'])
@usr.logged_in
def get_order(id, res=None, user_id=None):
    return order_instance.get_order(id)


@mod_orders.route('/orders/<int:id>', methods=['PUT'])
@usr.logged_in
def update_order(id, res=None, user_id=None):
    return order_instance.update_order(id)


@mod_orders.route('/orders/<int:id>', methods=['DELETE'])
@usr.logged_in
def delete_order(id, res=None, user_id=None):
    return order_instance.delete_order(id)
