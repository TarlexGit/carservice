from django.contrib import admin
from .models import Profile

from django.contrib.auth.admin import UserAdmin
# from rest_framework_simplejwt.models import TokenUser

admin.site.register(Profile)

# admin.site.register(TokenUser)
# Register your models here.

