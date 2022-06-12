from rest_framework import status
from rest_framework.test import APITestCase
from knox.models import AuthToken
from django.contrib.auth import get_user_model
from modules.community.models import Community, Team
from modules.round.models import Round
from modules.level.models import Level, LevelFeedback, LevelTeam, Student
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


class LevelTeamTest(APITestCase):
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
        self.level = Level.objects.create(name='level1', round=self.round)
        self.url = '/community/{}/rounds/{}/levels/{}/'.format(
            self.community.slug, self.round.slug, self.level.name)

    def test_create_level_team(self):
        response = self.client.post(self.url+'team/', {'user': self.user.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LevelTeam.objects.count(), 1)
        self.assertEqual(LevelTeam.objects.get().user, self.user)
        self.assertEqual(LevelTeam.objects.get().level, self.level)
        self.assertEqual(LevelTeam.objects.get().role, 'mentor')

    def test_create_level_team_without_invalid_user(self):
        response = self.client.post(self.url+'team/', {'user': ''})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(LevelTeam.objects.count(), 0)

    def test_create_level_team_without_user(self):
        response = self.client.post(self.url+'team/', {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(LevelTeam.objects.count(), 0)

    def test_create_level_team_without_user_in_team(self):
        user = User.objects.create(username='testuser2', codeforces='e', telegram='https://webl.telegram.org/', password='testpassword',
                                   email='al@gmail.com')

        response = self.client.post(self.url+'team/', {'user': user.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(LevelTeam.objects.count(), 0)

    def test_create_level_team_with_memeber(self):
        self.team.role = "Member"
        response = self.client.post(self.url+'team/', {'user': self.user.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_level_team(self):
        response = self.client.get(self.url+'team/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_level_team_member(self):
        member = LevelTeam.objects.create(
            user=self.user, level=self.level, role='mentor')
        response = self.client.get(self.url+'team/'+str(member.user)+'/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_level_team_member_not_in_team(self):
        response = self.client.get(self.url+'team/'+str(self.user)+'/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_level_team_member(self):
        member = LevelTeam.objects.create(
            user=self.user, level=self.level, role='mentor')
        response = self.client.put(
            self.url+'team/'+str(member.username)+'/', {'role': 'instructor'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(LevelTeam.objects.get().role, 'instructor')

    def test_delete_level_team(self):
        member = LevelTeam.objects.create(
            user=self.user, level=self.level, role='mentor')
        response = self.client.delete(
            self.url+'team/'+str(member.username)+'/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(LevelTeam.objects.count(), 0)


class StudentTest(APITestCase):

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
        self.level = Level.objects.create(name='level1', round=self.round)
        self.url = '/community/{}/rounds/{}/levels/{}/'.format(
            self.community.slug, self.round.slug, self.level.name)

    def test_create_level_student(self):
        response = self.client.post(self.url+'students/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(Student.objects.get().user, self.user)
        self.assertEqual(Student.objects.get().level, self.level)
        self.assertEqual(Student.objects.get().status, True)
        
    
    def test_get_level_student(self):
        response = self.client.get(self.url+'students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        
    def test_get_student_in_level(self):
        student = Student.objects.create(
            user=self.user, level=self.level, status=True)
        response = self.client.get(self.url+'students/'+str(student.username)+'/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Student.objects.get().user, self.user)
        
        
    def test_get_student_not_in_level(self):
        response = self.client.get(self.url+'students/'+str(self.user.username)+'/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_update_level_student(self):
        student = Student.objects.create(
            user=self.user, level=self.level, status=True)
        response = self.client.put(
            self.url+'students/'+str(student.username)+'/', {'status': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Student.objects.get().status, False)
        
    def test_delete_level_student(self):
        student = Student.objects.create(
            user=self.user, level=self.level, status=True)
        response = self.client.delete(
            self.url+'students/'+str(student.username)+'/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Student.objects.count(), 0)
        
    def test_delete_level_student_not_in_level(self):
        response = self.client.delete(
            self.url+'students/'+str(self.user.username)+'/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Student.objects.count(), 0)
        
    def test_delete_level_student_with_not_current_user(self):
        student = Student.objects.create(
            user=self.user, level=self.level, status=True)
        user = User.objects.create(username='testuser2', codeforces='e',
                                   telegram='https://web.telegraem.org/', password='testpassword',
                                   email="a@gmalil.com")
        token = AuthToken.objects.create(user=user)[1]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.delete(
            self.url+'students/'+str(self.user.username)+'/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
       
class LevelFeedbackTest(APITestCase):
    
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
        self.round = Round.objects.create( name='round1', community=self.community)
        self.level = Level.objects.create(name='level1', round=self.round)
        self.url = '/community/{}/rounds/{}/levels/{}/'.format(
            self.community.slug, self.round.slug, self.level.name)
        
        
    def test_create_level_feedback_not_in_level(self):
        response = self.client.post(self.url+'feedbacks/', {'feedback': 'test'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_create_level_feedback_student_does_not_in_level(self):
        level = Level.objects.create(name='level2', round=self.round)
        student=Student.objects.create(user=self.user, level=level, status=True)
        feedback=LevelFeedback.objects.create(feedback='test', stars=10,student=student,level=level)
        response = self.client.post(self.url+'feedbacks/', {'feedback': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_level_feedback_in_level(self):
        student_feedback=Student.objects.create(user=self.user, level=self.level, status=True)
        response = self.client.post(self.url+'feedbacks/', {'feedback': 'test','stars':10})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LevelFeedback.objects.count(), 1)
        self.assertEqual(LevelFeedback.objects.get().feedback, 'test')
        self.assertEqual(LevelFeedback.objects.get().stars, 10)
        
    def test_get_level_feedbacks(self):
        new_student=Student.objects.create(user=self.user, level=self.level, status=True)
        LevelFeedback.objects.create(feedback='test', stars=10,student=new_student,level=self.level)
        response = self.client.get(self.url+'feedbacks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_get_level_feedback(self):
        new_student=Student.objects.create(user=self.user, level=self.level, status=True)
        feedback=LevelFeedback.objects.create(feedback='test', stars=10,student=new_student,level=self.level)
        response = self.client.get(self.url+'feedbacks/'+str(feedback.id)+'/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(LevelFeedback.objects.get().feedback, 'test')
        
    def test_update_level_feedback(self):
        student=Student.objects.create(user=self.user, level=self.level, status=True)
        feedback=LevelFeedback.objects.create(feedback='test', stars=10,student=student,level=self.level)
        response = self.client.put(self.url+'feedbacks/'+str(feedback.id)+'/', {'feedback': 'test2','stars':10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(LevelFeedback.objects.get().feedback, 'test2')
        self.assertEqual(LevelFeedback.objects.get().stars, 10)
        
    
        
      