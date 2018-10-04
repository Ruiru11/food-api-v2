import unittest
import json
from app import create_app, db


class OrdersTestCase(unittest.TestCase):
    """Represesnts orders testcase """

    def setUp(self):
        self.app = create_app(config_name="test")
        self.client = self.app.test_client

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
        self.orders_data = {
            "item": "ugali",
            "description": "seven",
            "cost": "500"
        }
        self.admin_data = {
            "email": "admin@mail.com",
            "password": "adminpassword"
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

    def test_user_login(self):
        res = self.client().post(
            "api/v2/signin",
            data=json.dumps(self.login_data),
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

    def test_create_order(self):
        token = self.get_user_token()
        res = self.client().post(
            "api/v2/orders",
            data=json.dumps(self.orders_data),
            headers={"content-type": "application/json",
                     "Authorization": token
                     }
        )
        self.assertEqual(res.status_code, 200)

    def test_signin_admin(self):
        res = self.client().post(
            "api/v2/signin",
            data=json.dumps(self.admin_data),
            headers={"content-type": "application/json"}
        )
        self.assertEqual(res.status_code, 200)

    def get_admin_token(self):
        res = self.client().post(
            "api/v2/signin",
            data=json.dumps(self.admin_data),
            headers={"content-type": "application/json"}
        )
        response = json.loads(res.data.decode('utf-8'))['token']
        return response

    def test_admin_views_all_orders(self):
        token = self.get_admin_token()
        res = self.client().get(
            "api/v2/orders",
            headers={"content-type": "application/json",
                     "Authorization": token
                     }
        )
        self.assertEqual(res.status_code, 200)

    def test_admin_views_single_order(self):
        token = self.get_admin_token()
        res = self.client().get(
            "api/v2/orders/7c4961f9-50a8-47c8-b148-81711278da66",
            headers={"content-type": "application/json",
                     "Authorization": token
                     }
        )
        self.assertEqual(res.status_code, 200)

    def test_updates_order_status(self):
        token = self.get_admin_token()
        res = self.client().put(
            "api/v2/orders/7c4961f9-50a8-47c8-b148-81711278da66",
            headers={"content-type": "application/json",
                     "Authorization": token
                     }
        )
        self.assertEqual(res.status_code, 200)

    def test_admin_get_order_history_of_user(self):
        token = self.get_admin_token()
        res = self.client().get(
            "api/v2/user-orders/ba91c828-4687-40bb-affd-ae634461478b",
            headers={"content-type": "application/json",
                     "Authorization": token
                     }
        )
        self.assertEqual(res.status_code, 200)

    def test_normal_user_trying_to_access_user_order_history(self):
        token = self.get_user_token()
        res = self.client().get(
            "api/v2/user-orders/ba91c828-4687-40bb-affd-ae634461478b",
            headers={"content-type": "application/json",
                     "Authorization": token
                     }
        )
        self.assertEqual(res.status_code, 401)

    def test_if_normal_user_access_orders(self):
        # test normal user trying to view admin routes
        token = self.get_user_token()
        res = self.client().get(
            "api/v2/orders",
            headers={"content-type": "application/json",
                     "Authorization": token
                     }
        )
        self.assertEqual(res.status_code, 401)

    def test_if_normal_user_views_single_order(self):
        # test if normal users tries to access a single order
        token = self.get_user_token()
        res = self.client().get(
            "api/v2/orders/7c4961f9-50a8-47c8-b148-81711278da66",
            headers={"content-type": "application/json",
                     "Authorization": token
                     }
        )
        self.assertEqual(res.status_code, 401)


if __name__ == '__main__':
    unittest.main()
