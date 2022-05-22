import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from modules.communnity.models import Communnity
User=get_user_model()
class CommunnityTest(APITestCase):

    def setUp(self):
        """
        Ensure we can create a new account object.
        """
        url = "http://0.0.0.0:8000/account/register/"
        data = {
            'username': 'DabApps',
            'codeforces': 'elkady',
            'telegram': 'https://web.telegram.org/',
            'email': 'Ahmedabdal@gmail.com',
            'password': 'as112233'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'DabApps')
        self.token=response.data['token']
        self.api_authentication()
        
    def test_create_community(self):
        url = "http://0.0.0.0:8000/community/"
        data = {
            "name":"icpc",
            "university":"Zagazig",
            "owner":1
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Communnity.objects.count(),1)
        self.assertEqual(Communnity.objects.get().name,"icpc")
        self.assertEqual(Communnity.objects.get().owner.username,'DabApps')
        
    def test_create_community_with_notvaliduser(self):
        url = "http://0.0.0.0:8000/community/"
        data = {
            "name":"icpc",
            "university":"Zagazig",
            "owner":2
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
      

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    # def test_get_account(self):
    #     url = "http://0.0.0.0:8000/account/user-retrieve/"
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(CustomUser.objects.get().username, 'DabApps')
    #     self.assertEqual(CustomUser.objects.get().email, 'Ahmedabdal@gmail.com')
    #     self.assertEqual(CustomUser.objects.get().codeforces, 'elkady')
        
    # def test_update_account(self):
    #     url = "http://0.0.0.0:8000/account/user-update/"
    #     data = {
    #         'username': 'D',
    #         'codeforces': 'e'
    #      }
    #     response = self.client.put(url,data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    


