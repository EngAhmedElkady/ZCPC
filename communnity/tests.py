from django.test import TestCase
from .models import Communnity
from django.contrib.auth import get_user_model
# Create your tests here.


User = get_user_model()
# test community model
class TestCommunity(TestCase):
    def test_model(self):
        user = User.objects.create_user(username="abdelrahman" , email="abdo@gmail.com" , password="password")
        community = Communnity.objects.create(name="icpc" , university="suez canal" , owner=user)
        self.assertEqual(community.name , 'icpc')
        self.assertEqual(community.university , 'suez canal')
        self.assertEqual(community.owner , user)
