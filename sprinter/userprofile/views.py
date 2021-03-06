from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout

from sprinter.achievements.forms import SprinterForm
from sprinter.userprofile.models import Sprinter


def signin(request):
    if request.user.is_authenticated():
        return redirect('/home/')
    return render(request, 'signin.html', {})


def edit_profile(request):
    user = request.user
    saved = False
    sprinter = Sprinter.objects.get(user=user)
    if request.method == "POST":
        form = SprinterForm(request.POST, instance=sprinter)
        if form.is_valid():
            form.save()
            saved = True
    else:
        form = SprinterForm(instance=sprinter)
    return render(request, 'userprofile/edit_profile.html', {
        'form': form,    
        'active': 'edit',
        'saved': saved,
    })


def signout(request):
    logout(request)
    return redirect('/')
