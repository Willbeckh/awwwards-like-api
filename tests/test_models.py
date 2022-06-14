"test suite for testing the api model"
import unittest
from api.models import UserProfile, User, Project


class UserTest(unittest.TestCase):
    """
    this class sets the test case for user model
    """
    def setUp(self):
        self.new_user = User(username='avocado_dev', email='avoca@dev.do', password='password12')
    
    def test_isinstance(self):
        self.assertTrue(isinstance(self.new_user, User))
