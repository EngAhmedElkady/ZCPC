# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets= fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('name','codeforces_account','github_account',"upload","bio")}),
    )
    list_display = ["username","codeforces_account"]

admin.site.register(CustomUser, CustomUserAdmin)