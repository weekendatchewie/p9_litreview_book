from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView

from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

import core.views
import review.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core.views.LoginPage.as_view(), name='login'),
    path('signup/', core.views.SignupPage.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('password-change/', PasswordChangeView.as_view(success_url='login'), name='password-change'),
    path('password-done/', PasswordChangeDoneView.as_view(), name='password-done'),

    path('home/', login_required(review.views.HomePage.as_view()), name='home'),

    path('ticket/feed', login_required(review.views.TicketsReviewsFeed.as_view()), name='tickets_reviews_feed'),
    path('ticket/create', login_required(review.views.TicketCreate.as_view()), name='ticket-create'),
    path('ticket/<int:ticket_id>/update', login_required(review.views.TicketUpdate.as_view()), name='ticket-update'),
    path('ticket/<int:ticket_id>/review-answer', login_required(review.views.ReviewAnswerToTicket.as_view()),
         name='review-answer'),
    path('ticket/<int:pk>/delete', login_required(review.views.TicketDelete.as_view()), name="ticket-delete"),

    path('review/create', login_required(review.views.ReviewCreate.as_view()), name='review-create'),
    path('review/<int:review_id>/update', login_required(review.views.ReviewUpdate.as_view()), name='review-update'),
    path('review/<int:pk>/delete', login_required(review.views.ReviewDelete.as_view()), name="review-delete"),

    path('users/list', login_required(review.views.UsersList.as_view()), name='users-list'),
    path('users/<int:pk>/followers/add', review.views.AddFollower.as_view(), name='add-follower'),
    path('users/<int:pk>/followers/remove', review.views.Unfollow.as_view(), name='remove-follower'),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )