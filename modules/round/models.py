from django.db import models
from modules.communnity.models import Communnity
# Create your models here.


class Round(models.Model):

    communnity_id = models.ForeignKey(Communnity, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    disc = models.TextField(max_length=700)
    created_at = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Round"
        verbose_name_plural = "Rounds"

    def str(self):
        return f"{self.name} at {self.communnity_id}."
