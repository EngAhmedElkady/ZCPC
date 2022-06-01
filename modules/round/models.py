from random import choices
from django.db import models
from modules.community.models import Community
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
User = get_user_model()
# Create your models here.


class Round(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=False, unique=True)
    description = models.TextField(max_length=700, blank=True, null=True)
    community = models.ForeignKey(
        Community, on_delete=models.CASCADE, related_name="rounds")
    created_at = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Round"
        verbose_name_plural = "Rounds"

    def __str__(self):
        return f"{self.name}_{self.community.name}"

    def get_community(self):
        return self.community
    
