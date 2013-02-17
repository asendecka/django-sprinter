from django import forms

from sprinter.achievements.models import Sprinter

class SprinterForm(forms.ModelForm):
    gravatar_email = forms.EmailField()

    def save(self, *args, **kwargs):
        instance = super(SprinterForm, self).save(*args, **kwargs)
        print self.cleaned_data
        if self.instance and self.instance.pk:
            self.instance.user.email = self.cleaned_data.get('gravatar_email')
            self.instance.user.save()

        return instance

    class Meta:
        model = Sprinter
        fields = ('trac_login', 'trac_email', 'github_login',)
