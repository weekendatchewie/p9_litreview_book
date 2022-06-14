from django.contrib import admin

from core.models import User, UserFollows


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "first_name", "last_name"]


@admin.register(UserFollows)
class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ["user", "followed_user"]
