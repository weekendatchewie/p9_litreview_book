from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass

    def __str__(self):
        return f"Utilisateur : {self.username}"

    def followers(self):
        list_follower = []

        for follower in self.following.all():
            list_follower.append(follower.followed_user)

        return list_follower


class UserFollows(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followed_by', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'followed_user')

    def __str__(self):
        return f"{self.user} abonné(e) à {self.followed_user}"
