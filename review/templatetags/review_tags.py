import locale

from django import template
from django.utils import timezone

register = template.Library()

MIN = 60
HOUR = MIN * 60
DAY = HOUR * 24


@register.filter
def model_type(instance):
    return type(instance).__name__


@register.filter
def get_posted_at_display(time):
    seconds_ago = (timezone.now() - time).total_seconds()

    # Fais en sorte que la date retourner avec 'strftime' soit en fr
    try:
        locale.setlocale(locale.LC_TIME, 'fr_FR.utf8')
    except:
        locale.setlocale(locale.LC_TIME, 'fr_FR')

    if seconds_ago <= HOUR:
        return f"Posté il y a {int(seconds_ago // MIN)} minutes"
    elif seconds_ago <= DAY:
        return f"Posté il y a {int(seconds_ago // HOUR)} heures"
    return f"Posté le {time.strftime('%d %B %y à %Hh%M')}"


@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    if user == context['user']:
        return 'Vous avez '
    return f"{user.username} a "
