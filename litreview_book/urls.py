from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path

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

]
