from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from knox.models import AuthToken

from modules.community.models import Community, Team
User = get_user_model()


class CommunnityTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', codeforces='e', telegram='https://web.telegram.org/',
                                        email='test@gmail.com', password='testpassword')
        self.token = AuthToken.objects.create(user=self.user)[1]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post('/community/', {
            "name": "icpc",
            "university": "Zagazig",
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'icpc')
        self.assertEqual(response.data['university'], 'Zagazig')
        self.assertEqual(response.data['owner'], self.user.id)
        self.assertEqual(response.data['slug'], 'icpc')
        self.assertEqual(response.data['bio'], None)
        self.assertEqual(response.data['image'], None)

    def test_create_community(self):
        response = self.client.post('/community/', {
            "name": "new",
            "university": "Zagazig",
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'new')
        self.assertEqual(response.data['university'], 'Zagazig')
        self.assertEqual(response.data['owner'], self.user.id)
        self.assertEqual(response.data['slug'], 'new')
        self.assertEqual(response.data['bio'], None)
        self.assertEqual(response.data['image'], None)

    def test_get_communities(self):
        response = self.client.get('/community/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'icpc')
        self.assertEqual(response.data['results'][0]['university'], 'Zagazig')
        self.assertEqual(response.data['results'][0]['owner'], self.user.id)
        self.assertEqual(response.data['results'][0]['slug'], 'icpc')
        self.assertEqual(response.data['results'][0]['bio'], None)
        self.assertEqual(response.data['results'][0]['image'], None)

    def test_get_community(self):
        response = self.client.get('/community/icpc/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'icpc')
        self.assertEqual(response.data['university'], 'Zagazig')
        self.assertEqual(response.data['owner'], self.user.id)
        self.assertEqual(response.data['slug'], 'icpc')
        self.assertEqual(response.data['bio'], None)
        self.assertEqual(response.data['image'], None)

    def test_update_community(self):
        response = self.client.patch('/community/icpc/', {
            "name": "icpcs",
            "university": "Zagazigs",
            "bio": "test",
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'icpcs')
        self.assertEqual(response.data['university'], 'Zagazigs')
        self.assertEqual(response.data['owner'], self.user.id)
        self.assertEqual(response.data['slug'], 'icpcs')
        self.assertEqual(response.data['bio'], 'test')

    def test_update_community_with_wrong_user(self):
        user = User.objects.create(username='testuser2', codeforces='e', telegram='https://sweb.telegram.org/',
                                   password='testpassword')
        token = AuthToken.objects.create(user=user)[1]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.patch('/community/icpc/', {"name": "icpcs",
                                                          "university": "Zagazigs"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_community(self):
        response = self.client.delete('/community/icpc/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_community_with_wrong_slug(self):
        user = User.objects.create(username='testuser2', codeforces='e', telegram='https://sweb.telegram.org/',
                                   password='testpassword')
        token = AuthToken.objects.create(user=user)[1]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.delete('/community/icpc/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TeamTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', codeforces='e', telegram='https://web.telegram.org/',
                                        email='test@gmail.com', password='testpassword')
        self.token = AuthToken.objects.create(user=self.user)[1]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.community = Community.objects.create(
            name='icpc', university='Zagazig', owner=self.user)
        self.url = '/community/'+self.community.slug+'/team/'
        self.member = Team.objects.create(
            community=self.community, user=self.user)

    def test_create_team(self):
        tester = User.objects.create(username='tester', codeforces='e', telegram='https://web.telegram.orEg/',
                                     password='testpassword', email='a@gmail.com')
        response = self.client.post(self.url, {
            'email': "a@gmail.com",
            'role': "Team Leader"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 2)

    def test_create_team_with_user_not_a_team_leader_or_vice_or_owner(self):
        user = User.objects.create(username='testuser2', codeforces='e', telegram='https://sweb.telegram.org/',
                                   password='testpassword', email='a@gmail.com')
        token = AuthToken.objects.create(user=user)[1]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post(self.url, {
            'email': "a@gmail.com",
            'role': "Team Leader"
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_team_with_community_not_exist(self):
        response = self.client.post('/community/ccpc/team/', {'role': "Team Leader",
                                                              'email': "a@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_team_with_email_not_exist(self):
        response = self.client.post('/community/icpc/team/', {'role': "Team Leader",
                                                              'email': "a@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_members_of_team(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_member_of_team(self):
        response = self.client.get(
            self.url+str(self.member.username)+'/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_team(self):
        response = self.client.patch(self.url+str(self.member.username)+'/', {
            "role": "Team Leader",
            'status': True})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], 'Team Leader')

    def test_delete_team(self):
        response = self.client.delete(
            self.url+str(self.member.username)+'/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Team.objects.count(), 0)
        
        
        
    # def test_delete_team_with_wrong_user(self):
    #     user = User.objects.create(username='testuser3', codeforces='el',email="aa@gmail.com", telegram='https://sweb.telegram.org/',
    #                                password='testlpassword')
    #     token = AuthToken.objects.create(user=user)[1]
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    #     response = self.client.delete(
    #         self.url+str(self.member.username)+'/')
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
