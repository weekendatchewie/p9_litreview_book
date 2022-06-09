from django.contrib import admin

from review.models import Ticket, Review


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "user"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["headline", "body", "user", "ticket"]