from hashlib import md5

from django.db import models
from django.contrib.auth.models import User

from social_auth.signals import socialauth_registered

from sprinter.achievements.trac_types import *

def narrow_results(current, valid):
    """Narrow results from stats to ticket ids previously taken into account."""
    return [f for f in current if f in valid]

class Achievement(models.Model):
    """Achievement with fields that specify the set of rules to gain it. 
    For now all rule fields works with AND (user has to satisfy all non-null 
    rules to receive an achievement)."""

    name = models.CharField('Achievement title', max_length=255)
    description = models.CharField('Description', max_length=2000)
    picture = models.ImageField(upload_to='achievements', null=True)
    secret = models.BooleanField('Is secret achievement', default=False)

    ticket_count = models.IntegerField(null=True, blank=True)
    attachment_count = models.IntegerField(null=True, blank=True)
    comment_count = models.IntegerField(null=True, blank=True)

    # current status of the ticket (no matter if user changed it to the given state or not)
    severity = models.IntegerField(choices=SEVERITIES, null=True, blank=True)
    resolution = models.IntegerField(choices=RESOLUTIONS, null=True, blank=True)
    ticket_type = models.IntegerField(choices=TYPES, null=True, blank=True)
    component = models.IntegerField(choices=COMPONENTS, null=True,\
            blank=True)

    pull_request_count = models.IntegerField(null=True, blank=True)

    def can_grant_achievement(self, stats):
        """Simple achievement logic. Should be extended to something 
        more complicated with checking ticket ids in some stats."""
        valid_tickets = None
        if self.ticket_count:
            valid_tickets = stats['ticket_count'] 
            if len(stats['ticket_count']) < self.ticket_count:
                return False

        ticket_count = self.ticket_count if self.ticket_count else 1

        if self.attachment_count:
            valid_tickets = narrow_results(stats['attachment_count'],\
                    valid_tickets) if valid_tickets else\
                    stats['attachment_count']
            if len(valid_tickets) < self.attachment_count:
                return False

        if self.comment_count:
            valid_tickets = narrow_results(stats['comment_count'],\
                    valid_tickets) if valid_tickets else\
                    stats['comment_count']
            if len(valid_tickets) < self.comment_count:
                return False

        if self.severity:
            valid_tickets = self.get_valid_tickets(stats['severity'],\
                    self.severity, valid_tickets, ticket_count)
            if not valid_tickets:
                return False

        if self.resolution:
            valid_tickets = self.get_valid_tickets(stats['resolution'],\
                    self.resolution, valid_tickets, ticket_count)
            if not valid_tickets:
                return False

        if self.ticket_type:
            valid_tickets = self.get_valid_tickets(stats['type'],\
                    self.ticket_type, valid_tickets, ticket_count)
            if not valid_tickets:
                return False

        if self.component:
            valid_tickets = self.get_valid_tickets(stats['component'],\
                    self.component, valid_tickets, ticket_count)
            if not valid_tickets:
                return False
        
        if self.pull_request_count and 'pull_requests' in stats and stats['pull_requests']:
            if len(stats['pull_requests']) < self.pull_request_count:
                return False

        return True

    def get_valid_tickets(self, stats_list, attr_name, valid_tickets, ticket_count):
        valid_tickets = narrow_results(stats_list[attr_name],\
                valid_tickets) if valid_tickets else\
                stats_list[attr_name]
        if attr_name not in stats_list or\
                len(valid_tickets) < ticket_count:
            return []
        return valid_tickets

    def get_severity(self):
        if not self.severity:
            return None
        return dict(SEVERITIES)[self.severity]
    
    def get_component(self):
        if not self.component:
            return None
        return dict(COMPONENTS)[self.component]
    
    def get_ticket_type(self):
        if not self.ticket_type:
            return None
        return dict(TYPES)[self.ticket_type]
    
    def get_resolution(self):
        if not self.resolution:
            return None
        return dict(RESOLUTIONS)[self.resolution]

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

    def get_email_hash(self):
        print self.user.email
        if self.user.email:
            return md5(self.user.email).hexdigest()
        if self.trac_email:
            return md5(self.trac_email).hexdigest()
        return ''

def new_users_handler(sender, user, response, details, **kwargs):
    # create Sprinter 
    sprinter = Sprinter.objects.create(user=user)


socialauth_registered.connect(new_users_handler, sender=None)
