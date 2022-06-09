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
    """
    Create a ticket to ask a review to another users
    """

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


class ReviewCreate(View):
    """
    Create a ticket and review from the user himself
    """

    ticket_form_class = forms.TicketForm
    review_form_class = forms.ReviewForm

    def get(self, request):
        ticket_form = self.ticket_form_class()
        review_form = self.review_form_class()

        context = {
            "ticket_form": ticket_form,
            "review_form": review_form
        }

        return render(request, 'review/review_create.html', context)

    def post(self, request):

        ticket_form = self.ticket_form_class(request.POST, request.FILES)
        review_form = self.review_form_class(request.POST)

        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()

            return redirect('home')


class ReviewAnswerToTicket(View):
    """
    Answer to a ticket from another user, with a review
    """
    pass
