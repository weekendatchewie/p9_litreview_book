from django.shortcuts import render, redirect
from django.views import View

from review import forms
from review.models import Ticket


class HomePage(View):

    def get(self, request):

        user = request.user.username

        tickets = Ticket.objects.all()

        context = {
            'user': user,
            'tickets': tickets
        }

        return render(request, "review/home.html", context)


class TicketCreate(View):

    form_class = forms.TicketForm

    def get(self, request):
        form = self.form_class()

        return render(request, 'review/ticket_create.html', context={'form': form})

    def post(self, request):
        # As we send also a image we pass "request.FILES" to the form
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            ticket = form.save(commit=False)

            # set the uploader to the user before saving the model
            ticket.user = request.user

            ticket.save()

            return redirect('home')
