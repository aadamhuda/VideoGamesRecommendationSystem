from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Question, Game, Profile,PlayList,DislikeList,CompletedList, PageView
admin.site.register(MyUser, UserAdmin)
admin.site.register(Question)
admin.site.register(Game)
admin.site.register(Profile)
admin.site.register(PlayList)
admin.site.register(DislikeList)
admin.site.register(CompletedList)

class PageViewAdmin(admin.ModelAdmin):
    list_display = ['hostname', 'timestamp']

admin.site.register(PageView, PageViewAdmin)

