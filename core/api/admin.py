from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.models import MyUser

admin.site.register(MyUser, UserAdmin)
