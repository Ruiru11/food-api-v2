import unittest
import json
import jwt
from app import create_app, db


class OrdersTestCase(unittest.TestCase):
    """Represesnts orders and menu testcase """

    def setUp(self):
        self.app = create_app(config_name="test")
        self.client = self.app.test_client
        self.menu_data = {
            "name": "ugali",
            "description": "sweet"
        }
        self.order_data = {
            "user_id": "7",
            "item": "fries",
            "order_id": "10",
            "description": "served hot",
            "cost": "120"
        }
        self.user_data = {
            "email": "shs@mail.com",
            "password": "shssss",
            "address": "utawala",
            "username": "ruiru"
        }
        self.login_data = {
            "email": "shs@mail.com",
            "password": "shssss"
        }

        with self.app.app_context():
            db.create_tables()

    def test_create_new_user(self):
        res = self.client().post(
            "api/v2/signup",
            data=json.dumps(self.user_data),
            headers={"content-type": "application/json"}

        )
        self.assertEqual(res.status_code, 200)

    def get_user_token(self):
        res = self.client().post(
            "api/v2/signin",
            data=json.dumps(self.login_data),
            headers={"content-type": "application/json"}
        )
        response = json.loads(res.data.decode('utf-8'))['token']
        return response

    def test_create_menu(self):
        # tests if an menu is created succsefully
        token = self.get_user_token()
        res = self.client().post(
            "/api/v2/menus",
            data=json.dumps(self.menu_data),
            headers={
                "content-type": "application/json",
                "Authorization": token

            }
        )
        self.assertEqual(res.status_code, 200)

    def test_create_menu_without_token(self):
        # tests authorization needed
        res = self.client().post(
            "/api/v2/menus",
            data=json.dumps(self.menu_data),
            headers={
                "content-type": "application/json"
            }
        )
        self.assertEqual(res.status_code, 401)

    def test_create_order(self):
        # test if an order gets created
        token = self.get_user_token()
        res = self.client().post(
            "/api/v2/orders",
            data=json.dumps(self.order_data),
            headers={
                "content-type": "application/json",
                "Authorization": token
            }
        )
        self.assertEqual(res.status_code, 200)

    def test_create_order_without_token(self):
        # test creating an order without a token
        res = self.client().post(
            "/api/v2/orders",
            data=json.dumps(self.order_data),
            headers={
                "content-type": "application/json"
            }
        )
        self.assertEqual(res.status_code, 401)

    def test_get_orders(self):
        # test if orders can be retrieved
        token = self.get_user_token()
        res = self.client().get(
            "/api/v2/orders",
            headers={
                "content-type": "application/json",
                "Authorization": token
            }
        )
        self.assertEqual(res.status_code, 200)

    def test_get_orders_without_token(self):
        # test geting orders without id
        res = self.client().get(
            "/api/v2/orders",
            headers={
                "content-type": "application/json"
            }
        )
        self.assertEqual(res.status_code, 401)

    def test_get_orders_by_id(self):
        # test if an order can be accessed using its id
        token = self.get_user_token()
        res = self.client().get(
            "/api/v2/orders/7",
            headers={
                "content-type": "application/json",
                "Authorization": token
            }
        )
        self.assertEqual(res.status_code, 200)

    def test_get_orders_by_id_without_token(self):
        # test if order can be gotten without authorization
        res = self.client().get(
            "/api/v2/orders/7",
            headers={
                "content-type": "application/json"
            }
        )
        self.assertEqual(res.status_code, 401)

    def test_update_order_status(self):
        # test update method
        token = self.get_user_token()
        res = self.client().put(
            "/api/v2/orders/7",
            headers={
                "content-type": "application/json",
                "Authorization": token
            }
        )
        self.assertEqual(res.status_code, 200)

    def test_update_test_without_token(self):
        # test update an order without token
        res = self.client().put(
            "/api/v2/orders/7",
            headers={
                "content-type": "application/json"
            }
        )
        self.assertEqual(res.status_code, 401)


if __name__ == '__main__':
    unittest.main()
