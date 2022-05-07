from random import choices
from django.db import models
from modules.communnity.models import Communnity
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify  # new
import uuid
User = get_user_model()
# Create your models here.


class Round(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=700)
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


