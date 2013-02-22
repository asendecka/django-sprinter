from django import forms

from sprinter.achievements.models import Sprinter

class SprinterForm(forms.ModelForm):
    gravatar_email = forms.EmailField(label="Gravatar email", required=False)

    def __init__(self, *args, **kwargs):
        super(SprinterForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['gravatar_email'].initial = self.instance.user.email

    def save(self, *args, **kwargs):
        instance = super(SprinterForm, self).save(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.instance.user.email = self.cleaned_data.get('gravatar_email')
            self.instance.user.save()

        return instance

    class Meta:
        model = Sprinter
        fields = ('trac_login', 'trac_email', 'github_login',)
