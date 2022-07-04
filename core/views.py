from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View

from core.forms import LoginForm, SignupForm


class LoginPage(View):
    form_class = LoginForm
    template_name = "core/login.html"

    def get(self, request):

        form = self.form_class()

        message = ""

        context = {
            "form": form,
            "message": message,
        }

        return render(request, "core/login.html", context)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                return redirect('home')

        message = "Identifiants invalides"

        context = {
            "form": form,
            "message": message
        }

        return render(request, self.template_name, context)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super(LoginPage, self).dispatch(request, *args, **kwargs)


class SignupPage(View):
    form_class = SignupForm

    def get(self, request):
        form = self.form_class()

        context = {
            "form": form,
        }

        return render(request, "core/signup.html", context)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('home')

        return render(request, "core/signup.html", {"form": form})


def logout_user(request):
    logout(request)

    return redirect('login')
