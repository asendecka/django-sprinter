from datetime import datetime
import os

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.contrib.auth.decorators import login_required

from sprinter.achievements.models import Sprinter, Achievement
from sprinter.achievements.proxies import TicketChangesImporter, GithubImporter

# TODO: remove this view
def test_trac(request):
    start_date = datetime(2013, 2, 9, 10, 0, 0, 0)
    logins = [sprinter.trac_login for sprinter in Sprinter.objects.all()]
    user = os.environ['TRAC_USER']
    password = os.environ['TRAC_PASSWORD']
    proxy = TicketChangesImporter(user=user, password=password, logins=logins,\
            start_date=start_date)
    changes = proxy.fetch()

    return render(request, 'achievements/test_trac.html', {
        'changes': changes
    })

# TODO: remove this view
def test_github(request):
    start_date = datetime(2013, 2, 1, 10, 0, 0, 0)
    logins = [sprinter.github_login for sprinter in Sprinter.objects.all() if \
            sprinter.github_login]
    proxy = GithubImporter(logins=logins, start_date=start_date)
    changes = proxy.fetch()

    return render(request, 'achievements/test_github.html', {
        'changes': changes
    })


def board(request):
    sprinters = Sprinter.objects.all().annotate(achievements_count=\
            Count('achievements')).order_by('-achievements_count')
    return render(request, 'achievements/board.html', {
        'sprinters': sprinters,
        'active': 'board',
    })

def sprinter_detail(request, pk):
    sprinter = get_object_or_404(Sprinter, pk=pk)

    return render(request, 'achievements/sprinter_detail.html', {
        'sprinter': sprinter,
        'active': 'sprinter',
    })

def achievement_detail(request, pk):
    achievement = get_object_or_404(Achievement, pk=pk)
    
    return render(request, 'achievements/achievement_detail.html', {
        'achievement': achievement,
        'active': 'achievements',
    })

@login_required
def home(request):
    sprinter = request.user.get_profile()

    return render(request, 'achievements/sprinter_detail.html', {
        'sprinter': sprinter,
        'active': 'home',
    })

def achievements(request):
    achievements = Achievement.objects.all()

    return render(request, 'achievements/achievements.html', {
        'achievements': achievements,
        'active': 'achievements',
    })
