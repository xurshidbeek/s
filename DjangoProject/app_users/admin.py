from django.contrib import admin
from django.contrib.auth.admin import Group
from app_users.models import User

admin.site.unregister(Group)
admin.site.register(User)
