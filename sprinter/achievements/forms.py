from django import forms

from sprinter.achievements.models import Sprinter

class SprinterForm(forms.ModelForm):

    class Meta:
        model = Sprinter
        fields = ('trac_login', 'trac_email', 'github_login',)
