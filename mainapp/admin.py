from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Question, Game

admin.site.register(MyUser, UserAdmin)
admin.site.register(Question)
admin.site.register(Game)

