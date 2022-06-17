from datetime import datetime
from itertools import chain

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView
from django.core.paginator import Paginator

from core.models import User, UserFollows
from review import forms
from review.models import Ticket, Review


class HomePage(View):

    def get(self, request):
        user = request.user

        tickets = Ticket.objects.filter(Q(user__in=user.followed_people) | Q(user=user))
        reviews = Review.objects.filter(Q(user__in=user.followed_people) | Q(user=user))

        """
        La méthode 'itertools.chain' retourne un itérateur qui itère sur tous les éléments itérables fournis, 
        comme s’il s’agissait d’une seule séquence d’objets.
        """
        tickets_and_reviews = sorted(chain(tickets, reviews), key=lambda x: x.date_created, reverse=True)

        today = datetime.now()

        # Pagination : On met le nombre d'élément que l'on souhaite par page
        paginator = Paginator(tickets_and_reviews, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'user': user,
            'tickets': tickets,
            'tickets_and_reviews': tickets_and_reviews,
            'today': today,
            'page_obj': page_obj
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


class TicketsReviewsFeed(View):

    def get(self, request):
        tickets = Ticket.objects.filter(user=request.user)
        reviews = Review.objects.filter(user=request.user)

        tickets_and_reviews = sorted(chain(tickets, reviews), key=lambda x: x.date_created, reverse=True)

        return render(request, 'review/tickets_reviews_feed.html', context={"tickets_and_reviews": tickets_and_reviews})


class TicketUpdate(View):

    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)

        form = forms.TicketForm(instance=ticket)

        context = {
            "form": form,
        }

        return render(request, 'review/ticket_update.html', context)

    def post(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)

        form = forms.TicketForm(request.POST, request.FILES, instance=ticket)

        if form.is_valid():
            form.save()

        return redirect('tickets_reviews_feed')


class TicketDelete(DeleteView):
    model = Ticket
    template_name = "review/review_delete.html"
    success_url = reverse_lazy("tickets_reviews_feed")


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


class ReviewUpdate(View):
    review_form_class = forms.ReviewForm

    def get(self, request, review_id):
        ticket = get_object_or_404(Ticket, review__pk=review_id)

        review = get_object_or_404(Review, id=review_id)

        review_form = self.review_form_class(instance=review)

        context = {
            "ticket": ticket,
            "review_form": review_form,
        }

        return render(request, 'review/review_update.html', context)

    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)

        review_form = self.review_form_class(request.POST, instance=review)

        if review_form.is_valid():
            review_form.save()

            return redirect('tickets_reviews_feed')


class ReviewDelete(DeleteView):
    model = Review
    template_name = "review/review_delete.html"
    success_url = reverse_lazy("tickets_reviews_feed")


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


class UsersList(View):
    """
    On récupère tous les utilisateurs excepté celui qui est connecté, et tous ses followers
    """

    def get(self, request):
        user = request.user
        users_to_follow = User.objects.all().exclude(id=request.user.id)

        list_followed_people = user.followed_people

        # user.followers

        context = {
            "users_to_follow": users_to_follow,
            "followed_people": list_followed_people,
        }

        return render(request, 'review/users_list.html', context)


class AddFollower(View):

    def post(self, request, pk, *args, **kwargs):
        user = User.objects.get(pk=pk)

        UserFollows.objects.create(user=request.user, followed_user=user)

        return redirect('users-list')


class Unfollow(View):

    def post(self, request, pk, *args, **kwargs):

        user = User.objects.get(pk=pk)

        follow_user = UserFollows.objects.filter(user=request.user, followed_user=user)

        follow_user.delete()

        return redirect('users-list')
