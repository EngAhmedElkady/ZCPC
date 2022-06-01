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
        self.auth=AuthToken.objects.create(user=self.user)[1]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.auth)
        self.community = Community.objects.create( name='icpc', university='Zagazig', owner=self.user)
        self.team = Team.objects.create(user=self.user, community=self.community, role='Team Leader')
        self.round= Round.objects.create(name='round1',community=self.community)
        self.url = '/community/{}/rounds/{}/levels/'.format(self.community.slug,self.round.slug)
        self.data = {
            'name': 'level1',
        }
        
    def test_create_level(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Level.objects.count(), 1)
        self.assertEqual(Level.objects.get().name, 'level1')