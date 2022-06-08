from django.shortcuts import render
from django.views import View


class HomePage(View):

    def get(self, request):

        user = request.user.username

        context = {
            'user': user
        }

        return render(request, "review/home.html", context)
