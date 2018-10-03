import unittest
import json
from app import create_app, db


class MenusTestCase(unittest.TestCase):
    """ TestCase for Menus"""

    def setUp(self):
        self.app = create_app(config_name="test")
        self.client = self.app.test_client
        self.menu_data = {
            "name": "ugali",
            "description": "sweet"
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


if __name__ == '__main__':
    unittest.main()
