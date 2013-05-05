from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from sprinter.achievements.models import Achievement
from sprinter.userprofile.models import Sprinter


def board(request):
    sprinters = Sprinter.objects.with_achievement_counts()
    sprinters = sprinters.select_related('user')
    sprinters = sprinters.prefetch_related('achievements')
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
    sprinter = request.user.sprinter
    return render(request, 'achievements/sprinter_detail.html', {
        'sprinter': sprinter,
        'active': 'home',
    })


def achievements(request):
    achievements_qs = Achievement.objects.filter(secret=False)
    achievements_qs = achievements_qs.prefetch_related('sprinter_set__user')
    secret_achievements_count = Achievement.objects.filter(secret=True).count()

    return render(request, 'achievements/achievements.html', {
        'achievements': achievements_qs,
        'secret_achievements_count': secret_achievements_count,
        'active': 'achievements',
    })
