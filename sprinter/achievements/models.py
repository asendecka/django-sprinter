from django.db import models
from django.contrib.auth.models import User

from sprinter.achievements.trac_types import *

class Achievement(models.Model):
    """Achievement with fields that specify the set of rules to gain it. 
    For now all rule fields works with AND (user has to satisfy all non-null 
    rules to receive an achievement)."""

    name = models.CharField('Achievement title', max_length=255)
    description = models.CharField('Description', max_length=2000)

    ticket_count = models.IntegerField(null=True, blank=True)
    attachment_count = models.IntegerField(null=True, blank=True)
    comment_count = models.IntegerField(null=True, blank=True)

    # current status of the ticket (no matter if user changed it to the given state or not)
    severity = models.IntegerField(choices=SEVERITIES, null=True, blank=True)
    resolution = models.IntegerField(choices=RESOLUTIONS, null=True, blank=True)
    ticket_type = models.IntegerField(choices=TYPES, null=True, blank=True)
    component = models.IntegerField(choices=COMPONENTS, null=True,\
            blank=True)

    def can_grant_achievement(self, stats):
        """Simple achievement logic. Should be extended to something 
        more complicated with checking ticket ids in some stats."""
        if self.ticket_count and len(stats['ticket_count']) < self.ticket_count:
            return False
        ticket_count = self.ticket_count if self.ticket_count else 1
        if self.attachment_count and\
                len(stats['attachment_count']) < self.attachment_count:
            return False
        if self.comment_count and\
                len(stats['comment_count']) < self.comment_count:
            return False
        if self.severity and (self.severity not in stats['severity'] or len(stats['severity'][self.severity]) < ticket_count):
            return False
        if self.resolution and (self.resolution not in stats['resolution'] or len(stats['resolution'][self.resolution]) < ticket_count):
            return False
        if self.ticket_type and (self.ticket_type not in stats['type'] or len(stats['type'][self.ticket_type]) < ticket_count):
            return False
        if self.component and (self.component not in stats['component'] or len(stats['component'][self.component]) < ticket_count):
            return False
        return True

    def __unicode__(self):
        return self.name

class Sprinter(models.Model):
    """Sprint participant profile. Stores all necessary data to identify the 
    user in Trac and Github."""

    user = models.OneToOneField(User)
    trac_login = models.CharField('Trac login', max_length=255,\
            null=True, blank=True)
    trac_email = models.EmailField('Trac e-mail', blank=True, null=True)
    github_login = models.CharField('Github login', max_length=255,\
            null=True, blank=True)
    achievements = models.ManyToManyField(Achievement)

    def __unicode__(self):
        return unicode(self.user)

