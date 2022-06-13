from itertools import chain

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from review import forms
from review.models import Ticket, Review


class HomePage(View):

    def get(self, request):

        user = request.user.username

        tickets = Ticket.objects.all()
        reviews = Review.objects.all()

        """
        La méthode 'itertools.chain' retourne un itérateur qui itère sur tous les éléments itérables fournis, 
        comme s’il s’agissait d’une seule séquence d’objets.
        """
        tickets_and_reviews = sorted(chain(tickets, reviews), key=lambda x: x.date_created, reverse=True)

        context = {
            'user': user,
            'tickets': tickets,
            'tickets_and_reviews': tickets_and_reviews
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
    review_form_class = forms.ReviewForm

    def get(self, request, ticket_id):

        ticket = get_object_or_404(Ticket, id=ticket_id)

        review_form = self.review_form_class()

        context = {
            "ticket": ticket,
            "review_form": review_form,
        }

        return render(request, 'review/review_answer_to_ticket.html', context)

    def post(self, request, ticket_id):
        review_form = self.review_form_class(request.POST)

        ticket = get_object_or_404(Ticket, id=ticket_id)

        if review_form.is_valid():

            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()

            return redirect('home')
