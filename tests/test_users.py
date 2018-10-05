import unittest
import json
from app import create_app, db


class UsersTestCase(unittest.TestCase):
    """Represesnts users testcase """

    def setUp(self):
        self.app = create_app(environment="testing")
        self.client = self.app.test_client

        self.user_data = {
            "email": "yyy@mail.com",
            "password": "shssss",
            "address": "utawala",
            "username": "ruiru"
        }

        self.new_data = {
            "email": "mail.com",
            "password": "shssss",
            "address": "utawala",
            "username": "ruiru"
        }

        self.signin_data = {
            "email": "yyy@mail.com",
            "password": "shssss"
        }

        with self.app.app_context():
            db.create_tables()

    def test_user_signup_with_wrong_email_format(self):
        res = self.client().post(
            "api/v2/signup",
            data=json.dumps(self.new_data),
            headers={"content-type": "application/json"}
        )
        self.assertEqual(res.status_code, 403)

    def test_user_signup(self):
        res = self.client().post(
            "api/v2/signup",
            data=json.dumps(self.user_data),
            headers={"content-type": "application/json"}
        )
        self.assertEqual(res.status_code, 201)

    def test_user_signin(self):
        res = self.client().post(
            "api/v2/signin",
            data=json.dumps(self.signin_data),
            headers={"content-type": "application/json"}
        )
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
