from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

from sprinter.achievements.proxies import TicketChangesImporter
from sprinter.achievements.models import Sprinter, Achievement
from sprinter.achievements.trac_types import *

# index in ticket list with dictionary of ticket attributes
TICKET_ATTRIBUTES = 3 

# list of attribute names
STAT_FIELDS = ['type', 'component', 'resolution', 'severity', ]

class Command(BaseCommand):
    args = '<user> <password>'
    help = 'Pass trac user and password to recalculate achievements.'

    def handle(self, user, password, *args, **options):
        logins = [sprinter.trac_login for sprinter in Sprinter.objects.all()]
        start_date = datetime(2013, 2, 1, 10, 0, 0, 0) # TODO: customize date

        proxy = TicketChangesImporter(user=user, password=password,\
            logins=logins, start_date=start_date)
        changes = proxy.fetch()
        self.process_changes(changes)
        
    def process_changes(self, changes):
        """Takes all changes done by sprinters and recalculate sprinters'
        statistics"""
        
        # ticket_count, attachment_count, comment_count, severity 
        # resolution, ticket_type, component
        for author, tickets in changes.items():
            if '@' in author:
                sprinter = Sprinter.objects.filter(trac_email=author)
            else:
                sprinter = Sprinter.objects.filter(trac_login=author)
            if sprinter:
                sprinter = sprinter[0]
                self.grant_achievements(sprinter, tickets)
    
    def get_updated_stat(self, stats, stat_field, ticket, attributes):
        return [ticket['ticket_id']]\
                if not (attributes[stat_field] in stats[stat_field]) else\
                stats[stat_field][attributes[stat_field]] + [ticket['ticket_id']]
    
    def grant_achievements(self, sprinter, tickets):
        achievements = Achievement.objects.all()
        stats = self.generate_stats(tickets)
        for achievement in achievements:
            if achievement.can_grant_achievement(stats):
                sprinter.achievements.add(achievement)

    def generate_stats(self, tickets):
        stats = {
            'ticket_count': [], 
            'attachment_count': [], 
            'comment_count': [], 
            'severity': {}, 
            'resolution': {}, 
            'type': {}, 
            'component': {},
        }

        for ticket in tickets:
            attributes = ticket['ticket'][TICKET_ATTRIBUTES]
           
            # tickets changed
            stats['ticket_count'].append(ticket['ticket_id'])

            # attachmnets added
            if attributes['has_patch'] and ticket['field'] == FD_ATTACHMENT: 
                stats['ticket_count'].append(ticket['ticket_id'])

            # changes in tickets with given severity/component/resolution/type
            for stat_field in STAT_FIELDS:
                stats[stat_field][attributes[stat_field]] =\
                        self.get_updated_stat(stats, stat_field, ticket, attributes)

        return stats
