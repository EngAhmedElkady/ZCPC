from random import choices
from django.db import models
from modules.communnity.models import Communnity
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()
# Create your models here.


class Round(models.Model):

    name = models.CharField(max_length=200)
    disc = models.TextField(max_length=700)
    communnity_id = models.ForeignKey(Communnity, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Round"
        verbose_name_plural = "Rounds"

    def str(self):
        return f"{self.name} round at {self.communnity_id}."

    def team(self):
        "return the team for this round"
        pass

    def members(self):
        "return all members study in this round"
        pass


class RoundTeam(models.Model):
    "This is a team for this round because each round maybe has different team"

    fields = [('instructor', 'instructor'), ('mentor', 'mentor')]

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    round_id = models.ForeignKey(Round, on_delete=models.CASCADE)
    role = models.CharField(max_length=200,choices=fields)

    class Meta:
        verbose_name = "RoundTeam"
        verbose_name_plural = "RoundTeams"

    def str(self):
        return f"{self.name} at {self.round.id} as {self.role}."


class Student(models.Model):
    "all students study at round "

    """
    status : if student does not solve the problems, it will be false
             that is mean remove from training but still in member 
    """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    round_id = models.ForeignKey(Round, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def str(self):
        return f"{self.user_id} at {self.round_id}."


class RoundFeedback(models.Model):
    student=models.ForeignKey(Student, on_delete=models.CASCADE)
    round_id = models.ForeignKey(Round, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    disc=models.TextField()

    

class TeamFeedback(models.Model):
    
    """store the feedback about all members in round team.
    
    """
    student=models.ForeignKey(Student, on_delete=models.CASCADE)
    team_member = models.ForeignKey(RoundTeam, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    disc=models.TextField()
    
    


    