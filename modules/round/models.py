from random import choices
from django.db import models
from modules.communnity.models import Communnity
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()
# Create your models here.


class Round(models.Model):
    """
    each communnity has many round each round has the following:
    - team    : like instructor and mentors
    - student : study in this roudn

    Args:
        name      : name of this Round
        disc      : description
        created_at: the time started at 
        end_date  : the time ended at 
        status    : boolean field be False if round ended 


    Returns:
        team     : function > "return the team for this round"
        students : function > "return all students study in this round"
        feedback : function > "return feedback about round and average rate"



    """
    name = models.CharField(max_length=200)
    disc = models.TextField(max_length=700)
    communnity = models.ForeignKey(
        Communnity, on_delete=models.CASCADE, related_name="rounds")
    created_at = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Round"
        verbose_name_plural = "Rounds"

    def __str__(self):
        return f"{self.name} at {self.communnity}."

    def get_community(self):
        community_id = self.communnity.id
        return community_id


class RoundTeam(models.Model):
    """
    This is a team for this round because each round maybe has different team.

    - member      : like instructor and mentors

    Args:
        user   : member (should become at the communnity team)
        round  : the round
        role      : role like as instructor or mentor



    Returns:
        feedback : function > "return feedback about round and average rate"  

    """

    fields = [('instructor', 'instructor'), ('mentor', 'mentor')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    round = models.ForeignKey(
        Round, on_delete=models.CASCADE, related_name="roundteam")
    role = models.CharField(max_length=200, choices=fields)

    class Meta:
        verbose_name = "RoundTeam"
        verbose_name_plural = "RoundTeams"

    def __str__(self):
        return f"{self.user_id} at {self.round} as {self.role}."

    def get_community(self):
        community_id = self.round.communnity.id
        return community_id


class Student(models.Model):
    "all students study at round "

    """
    status : if student does not solve the problems, it will be false
             that is mean remove from training but still in member 
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE,related_name="roundstudent")
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return f"{self.user_id} at {self.round}."
    
    def get_community(self):
        community_id = self.round.communnity.id
        return community_id


class RoundFeedback(models.Model):
    "store the feedback about all members in round team."

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    disc = models.TextField()

    def __str__(self):
        return str(self.round)
    
    def get_community(self):
        community_id = self.round.communnity.id
        return community_id


class TeamFeedback(models.Model):
    "store the feedback about all members in round team."

    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="userteamfeedback")
    team_member = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='teamfeedback')
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    disc = models.TextField()

    def __str__(self):
        return str(self.team_member)
    
    def get_community(self):
        community_id = self.round.communnity.id
        return community_id
