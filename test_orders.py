import unittest
import json
from app import create_app, db

class OrdersTestCase(unittest.TestCase):
    """Represesnts orders and menu testcase """

    def setUp(self):
        self.app = create_app(config_name="test")
        self.client = self.app.test_client


        with self.app.app_context():
            db.create_tables()

    def register_user(self,email='verbose@gmail.com', password='newhere', address='utawala'):
        user_data = {
            'email':email,
            'password':password,
            'address':address
        }
        return self.client().post('api/v2/signup', data=user_data)
        result = json.loads(res.user_data.decode('utf-8'))
        print(result)
    
    def login_user(self,email='verbose@gmail.com', password='newhere'):
        user_data = {
            'emai':email,
            'password':password
        }
        return self.client().post('api/v2/signin',data=user_data)
     
    
    def test_order_creation(self):
        data =  {
            "item":"mbuzi",
            "description":"fry",
            "cost":"500","user_id":"1",
            "order_id":"7"
            }
        res = self.client().post(
            "/api/v2/orders",
            data=json.dumps(data),
            headers={"content-type": "application/json"}
        )
        result = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code,200)
        #self.assertEqual(result['message'], 'order created successfully')
       
       
       


if __name__ == '__main__':
    unittest.main()