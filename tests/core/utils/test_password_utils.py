import unittest
from core.utils.password_utils import encrypt_password, check_password

class UserManagerTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_password_utils(self):
        self.encrypted_password = encrypt_password('test123')
        is_correct = check_password('test123', self.encrypted_password)
        self.assertEquals(is_correct, True)

        is_correct = check_password('test1234', self.encrypted_password)
        self.assertEquals(is_correct, False)

    def tearDown(self):
        pass