from django.contrib import admin
from .models import Round

# Register your models here.
class RoundAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
admin.site.register(Round,RoundAdmin)
