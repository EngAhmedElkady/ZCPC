from rest_framework import status
from rest_framework.test import APITestCase
from knox.models import AuthToken
from django.contrib.auth import get_user_model
from modules.community.models import Community, Team
User = get_user_model()


# Create your tests here.
# test round
class RoundTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', codeforces='e',
                                        telegram='https://web.telegram.org/', password='testpassword', email='test@gmail.com')
        self.token = AuthToken.objects.create(user=self.user)[1]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.community = Community.objects.create(
            name='icpc', university='Zagazig', owner=self.user)
        self.team = Team.objects.create(
            user=self.user, community=self.community, role='Team Leader')
        self.url = '/community/{}/rounds/'.format(self.community.slug)
        self.data = {
            "name": "round1",
            'description': 'round1',
        }

    def test_create_round(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_round_with_user_not_in_team(self):
        self.team.delete()
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_round_with_community_not_exist(self):
        response = self.client.post('/community/not_exist/rounds/', self.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_rounds(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_round_does_not_exist(self):
        response = self.client.get(self.url + 'round1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_round(self):
        data = {
            "name": "round1"
        }
        response = self.client.post(self.url, data)
        response = self.client.delete(self.url + 'round1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_round_with_user_is_not_TeamLeader_or_Vice(self):
        self.team.role = 'Member'
        self.team.save()
        
        data = {
            "name": "round1"
        }
        response = self.client.post(self.url, data)
        response = self.client.delete(self.url + 'round1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
