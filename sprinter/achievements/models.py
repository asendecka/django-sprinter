from django.db import models
from django.contrib.auth.models import User

class Sprinter(models.Model):
    user = models.OneToOneField(User)
    trac_login = models.CharField('Trac login', max_length=255,\
            null=True, blank=True)
    trac_email = models.EmailField('Trac e-mail', blank=True, null=True)
    github_login = models.CharField('Github login', max_length=255,\
            null=True, blank=True)
