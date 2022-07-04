from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass

    def __str__(self):
        return f"Utilisateur : {self.username}"

    @property
    def followed_people(self):
        """
        Liste des gens que suit l'utilisateur
        """
        list_followed_people = []

        for followed_people in self.following.all():
            list_followed_people.append(followed_people.followed_user)

        return list_followed_people

    def count_followed_people(self):
        return len(self.followed_people)

    @property
    def followers(self):
        """
        Liste des gens qui suivent l'utilisateur
        """

        list_followers = []

        for follower in self.followed_by.all():
            if follower.user != self:
                list_followers.append(follower.user)
        return list_followers

    def count_followers(self):
        return len(self.followers)

    @property
    def user_reviews(self):
        """
        Liste des id des tickets associés aux critiques.
        Permet de conditionner l'affichage d'un bouton "créer avis"
        Si un utilisateur a déjà posté une critique sur un ticket, il ne pourra pas reposter une critique
        """
        list_user_reviews = []

        for review in self.review_set.all():
            if review:
                list_user_reviews.append(review.ticket.id)

        return list_user_reviews


class UserFollows(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followed_by', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'followed_user')

    def __str__(self):
        return f"{self.user} abonné(e) à {self.followed_user}"
