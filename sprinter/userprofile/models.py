import hashlib
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Q
from django.dispatch import receiver
from social_auth.signals import socialauth_registered


class SprinterManager(models.Manager):
    def with_achievement_counts(self):
        qs = self.annotate(achievements_count=Count('achievements'))
        return qs.order_by('-achievements_count')

    def get_by_trac_author(self, author):
        by_login = Q(trac_login__iexact=author)
        by_email = Q(trac_email__iexact=author)
        return self.get(by_email | by_login)


class Sprinter(models.Model):
    """Sprint participant profile. Stores all necessary data to identify the
    user in Trac and Github."""
    user = models.OneToOneField(User)
    trac_login = models.CharField(max_length=250, blank=True)
    trac_email = models.EmailField(blank=True)
    github_login = models.CharField(max_length=250, blank=True)
    achievements = models.ManyToManyField(
        'achievements.Achievement', blank=True)

    objects = SprinterManager()

    def get_email_hash(self):
        email = self.user.email or self.trac_email or ''
        return hashlib.md5(email).hexdigest()

    def __unicode__(self):
        return self.user.username


@receiver(socialauth_registered)
def new_users_handler(sender, user, response, details, **kwargs):
    Sprinter.objects.create(user=user)


class SprinterChange(models.Model):
    sprinter = models.ForeignKey(Sprinter, related_name='changes')
    ticket_change = models.OneToOneField('trac.Change', null=True, blank=True)
    kind = models.CharField('trac type', max_length=250, blank=True)
    component = models.CharField(max_length=250, blank=True)
    resolution = models.CharField(max_length=250, blank=True)
    status = models.CharField(max_length=250, blank=True)
    severity = models.CharField(max_length=250, blank=True)
    ticket_id = models.IntegerField()
    field = models.CharField(max_length=250)
