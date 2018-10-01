import unittest
import json
from app import create_app, db

class OrdersTestCase(unittest.TestCase):
    """Represesnts orders and menu testcase """

    def setUp(self):
        self.app = create_app(config_name="test")
        self.client = self.app.test_client
        self.Menu = {'matoke','Tamu Sana'}

        with self.app.app_context():
            db.create_tables()

    def register_user(self,email='verbose@gmail.com', password='newhere', address='utawala'):
        user_data = {
            'email':email,
            'password':password,
            'address':address
        }
        return self.client().post('api/v2/signup', data=user_data)
    
    def login_user(self,email='verbose@gmail.com', password='newhere'):
        user_data = {
            'emai':email,
            'password':password
        }
        return self.client().post('api/v2/signin',data=user_data)
    
    def test_menu_creation(self):
        self.register_user()
        result = self.login_user()
        token = json.loads(result.data.decode('utf-8'))['token']
        res = self.client().post(
            'api/v2/menus',
            headers=dict(Authorization + token),
            data=self.Menu
        )
        self.assertEqual(res.status_code,200)
       
       
       


if __name__ == '__main__':
    unittest.main()