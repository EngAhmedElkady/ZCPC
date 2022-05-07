from django.test import TestCase

# Create your tests here.
from django.test import TestCase 
from .models import CustomUser
# create test user
class TestUser(TestCase):
    
    def __init__(self):
        user = CustomUser.objects.create_user(username="Ahmed",
        email='ahmed@gmail.com' , name="degea", bio="team leader" , 
        codeforces_account="Abdo_ibrahem", github_account="Abdo_ibrahem" , password="password")
    def test_user_model(self):
        
        self.assertEqual(self.user.username,'ahmed')
        self.assertEqual(self.user.email ,'ahmed@gmail.com')
        self.assertEqual(self.user.name ,'degea' )
        self.assertEqual(self.user.bio ,'team leader')
        self.assertEqual(self.user.codeforces_account ,'Abdo_ibrahem' )
        self.assertEqual(self.user.github_account ,'Abdo_ibrahem')

    def test_super_user(self):
        super_user = CustomUser.objects.create_superuser(
            username="abdelrahman",
            email="abdelrahman@gmail.com",
            password="password"
        )
        self.assertEqual(super_user.username ,'abdelrahman')
        self.assertEqual(super_user.email ,'abdelrahman@gmail.com')
        self.assertTrue(super_user.is_superuser)
    
