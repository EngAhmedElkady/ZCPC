from django.contrib import admin
from .models import Round, Student, TeamMember, TeamFeedback, RoundFeedback

# Register your models here.

admin.site.register(Round)
admin.site.register(Student)
admin.site.register(TeamMember)
admin.site.register(TeamFeedback)
admin.site.register(RoundFeedback)
