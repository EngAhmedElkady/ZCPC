from rest_framework import status
from rest_framework.test import APITestCase
from knox.models import AuthToken
from django.contrib.auth import get_user_model
from modules.community.models import Community, Team
from modules.round.models import Round
from modules.level.models import Level
User = get_user_model()

# Create your tests here.


class LevelTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', codeforces='e',
                                        telegram='https://web.telegram.org/', password='testpassword',
                                        email="a@gmail.com")
        self.token = AuthToken.objects.create(user=self.user)[1]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.community = Community.objects.create(
            name='icpc', university='Zagazig', owner=self.user)
        self.team = Team.objects.create(
            user=self.user, community=self.community, role='Team Leader')
        self.round = Round.objects.create(
            name='round1', community=self.community)
        self.url = '/community/{}/rounds/{}/levels/'.format(
            self.community.slug, self.round.slug)
        self.data = {
            'name': 'level1',
        }

    def test_create_level(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Level.objects.count(), 1)
        self.assertEqual(Level.objects.get().name, 'level1')

    def test_create_level_without_name(self):
        self.data['name'] = ''
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Level.objects.count(), 0)

    def test_create_level_with_member(self):
        self.team.role = "Member"
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_level_with_member_not_in_team(self):
        team = Team.objects.get(id=1)
        team.delete()
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_levels(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_level(self):
        level = Level.objects.create(name='level1', round=self.round)
        response = self.client.get(self.url+str(level.name)+'/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'level1')

    def test_update_level(self):
        level = Level.objects.create(name='level1', round=self.round)
        self.data['name'] = 'level2'
        response = self.client.put(self.url+str(level.name)+'/', self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Level.objects.get().name, 'level2')

    def test_delete_level(self):
        level = Level.objects.create(name='level1', round=self.round)
        response = self.client.delete(self.url+str(level.name)+'/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Level.objects.count(), 0)

    def test_delete_level_with_member(self):
        self.team.role = "Member"
        self.team.save()
        level = Level.objects.create(name='level1', round=self.round)
        response = self.client.delete(self.url+str(level.name)+'/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
