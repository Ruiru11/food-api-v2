import unittest
import json
from app import create_app, db


class MenusTestCase(unittest.TestCase):
    """ TestCase for Menus"""

    def setUp(self):
        self.app = create_app(config_name="test")
        self.client = self.app.test_client
        self.menu_data = {
            "name": "naramat",
            "description": "sweet",
            "price": "500"
        }

        self.user_data = {
            "email": "shs@mail.com",
            "password": "shssss",
            "address": "utawala",
            "username": "ruiru",
            "role": "admin"
        }
        self.login_data = {
            "email": "shs@mail.com",
            "password": "shssss"
        }
        self.admin_data = {
            "email": "admin@mail.com",
            "password": "adminpassword"
        }

        with self.app.app_context():
            db.create_tables()

    def test_admin_login(self):
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

    def test_admin_create_menu(self):
        token = self.get_admin_token()
        res = self.client().post(
            "api/v2/menus",
            data=json.dumps(self.menu_data),
            headers={"content-type": "application/json",
                     "Authorization": token
                     }
        )
        self.assertEqual(res.status_code, 200)

    def test_user_signin(self):
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

    def test_normal_user_creating_menu(self):
        token = self.get_user_token()
        res = self.client().post(
            "api/v2/menus",
            data=json.dumps(self.menu_data),
            headers={"content-type": "application/js",
                     "Authorization": token
                     }
        )
        self.assertEqual(res.status_code, 401)

    def test_anyone_can_view_menus(self):
        res = self.client().get(
            "api/v2/menus",
            headers={"content-type": "application/json"}
        )
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
