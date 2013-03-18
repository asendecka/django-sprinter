from django.db import models

from social_auth.signals import socialauth_registered

from sprinter.achievements.trac_types import *
from sprinter.userprofile.models import new_users_handler


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

        if self.severity != None:
            valid_tickets = self.get_valid_tickets(stats['severity'],\
                    self.severity, valid_tickets, ticket_count)
            if not valid_tickets:
                return False
        
        if self.resolution != None:
            valid_tickets = self.get_valid_tickets(stats['resolution'],\
                    self.resolution, valid_tickets, ticket_count)
            if not valid_tickets:
                return False

        if self.ticket_type != None:
            valid_tickets = self.get_valid_tickets(stats['type'],\
                    self.ticket_type, valid_tickets, ticket_count)
            if not valid_tickets:
                return False

        if self.component != None:
            valid_tickets = self.get_valid_tickets(stats['component'],\
                    self.component, valid_tickets, ticket_count)
            if not valid_tickets:
                return False
        
        if self.pull_request_count and 'pull_requests' in stats:
            if not stats['pull_requests'] or len(stats['pull_requests']) < self.pull_request_count:
                return False

        return True

    def get_valid_tickets(self, stats_list, attr_name, valid_tickets, ticket_count):
        if valid_tickets and attr_name in stats_list:
            valid_tickets = narrow_results(stats_list[attr_name],\
                valid_tickets) 
        elif attr_name in stats_list:
            valid_tickets = stats_list[attr_name]
        else:
            valid_tickets = []
        if len(valid_tickets) < ticket_count:
            return []
        return valid_tickets

    def get_severity(self):
        if self.severity == None:
            return None
        return dict(SEVERITIES)[self.severity]
    
    def get_component(self):
        if self.component == None:
            return None
        return dict(COMPONENTS)[self.component]
    
    def get_ticket_type(self):
        if self.ticket_type == None:
            return None
        return dict(TYPES)[self.ticket_type]
    
    def get_resolution(self):
        if self.resolution == None:
            return None
        return dict(RESOLUTIONS)[self.resolution]

    def __unicode__(self):
        return self.name




