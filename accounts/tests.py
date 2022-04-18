from django.test import TestCase
from d
# Create your tests here.
class UserTest(TestCase):
    """
    test the following:
    1- register_user
    2- login_user
    3- update_user
    
    """
    
    def setUp(self):
        self.user=