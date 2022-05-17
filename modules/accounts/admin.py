# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    #  to display this field in admin panal
    fieldsets= fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('name','codeforces','github',"upload","bio")}),
    )
    list_display = ["username","codeforces"]

admin.site.register(CustomUser, CustomUserAdmin)