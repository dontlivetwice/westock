import unittest
from core.managers.user_manager import UserManager
from core.models.user import User

class UserManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.user_manager = UserManager()
        self.user = User(id=123456789, first_name='chris', last_name='imberti', 
            email='chris@gmail.com', username='chris', 
            password='123pass', about='this is me', 
            location='San Francisco, CA', website='https://stoksinterest.io/chris',
            image_url='http://chris', gender='male')

    def test_add_user(self):
        ret = self.user_manager.add_one(self.user)
        self.assertEquals(ret, 1)

        self.user['email'] = 'test@test.com'

        ret = self.user_manager.update_one(self.user)
        self.assertEquals(ret, 1)

        self.user = self.user_manager.get_one(username='chris')
        self.assertEquals(self.user.get('email'), 'test@test.com')

    def test_delete_user(self):
        ret = self.user_manager.delete_one(self.user)
        self.assertEquals(ret, 1)

    def tearDown(self):
        pass