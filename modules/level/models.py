from django.db import models
from modules.round.models import Round
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()
# Create your models here.


class Level(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=700,blank=True,null=True)
    round = models.ForeignKey(
        Round, on_delete=models.CASCADE, related_name="levels")
    created_at = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "level"
        verbose_name_plural = "levels"
        unique_together = ('round', 'name',)

    def __str__(self):
        return f"{self.name}"

    def get_community(self):
        community = self.round.community
        return community


class LevelTeam(models.Model):

    fields = [('instructor', 'instructor'), ('mentor', 'mentor')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.ForeignKey(
        Level, on_delete=models.CASCADE, related_name="team")
    role = models.CharField(max_length=200, choices=fields)

    class Meta:
        verbose_name = "LevelTeam"
        verbose_name_plural = "LevelTeams"

    def __str__(self):
        return f"{self.user} at {self.level} as {self.role}."

    def get_community(self):
        community = self.level.get_community()
        return community


class Student(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.ForeignKey(
        Level, on_delete=models.CASCADE, related_name="student")
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return f"{self.user_id} at {self.level}."

    def get_community(self):
        community = self.level.get_community()
        return community


class LevelFeedback(models.Model):
    "store the feedback about all members in level team."

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE,related_name="feedback")
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    disc = models.TextField()

    def __str__(self):
        return str(self.level)

    def get_community(self):
        community= self.level.get_community()
        return community


class TeamFeedback(models.Model):
    "store the feedback about all members in level team."
    level = models.ForeignKey(Level, on_delete=models.CASCADE,related_name="teamfeedback")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="userteamfeedback")
    team_member = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='teamfeedback')
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    disc = models.TextField()

    def __str__(self):
        return str(self.team_member)

    def get_community(self):
        community = self.level.get_community()
        return community
