from django.test import TestCase 
from .models import CustomUser
# create test user
class TestUser(TestCase):
    def test_user_model(self):
        user = CustomUser.objects.create_user(username="abdelrahman",
            email='abdo@gmail.com' , name="abdo", bio="abdelrahman ibrahem" , 
            codeforces_account="Abdo_ibrahem", github_account="Abdo_ibrahem" , password="password")
        self.assertEqual(user.username,'abdelrahman')
        self.assertEqual(user.email ,'abdo@gmail.com')
        self.assertEqual(user.name ,'abdo' )
        self.assertEqual(user.bio ,'abdelrahman ibrahem')
        self.assertEqual(user.codeforces_account ,'Abdo_ibrahem' )
        self.assertEqual(user.github_account ,'Abdo_ibrahem')

    def test_super_user(self):
        super_user = CustomUser.objects.create_superuser(
            username="abdelrahman",
            email="abdelrahman@gmail.com",
            password="password"
        )
        self.assertEqual(super_user.username ,'abdelrahman')
        self.assertEqual(super_user.email ,'abdelrahman@gmail.com')
        self.assertTrue(super_user.is_superuser)
    
    