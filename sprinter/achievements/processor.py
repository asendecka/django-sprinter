from sprinter.achievements.models import Sprinter, Achievement
from sprinter.achievements.trac_types import *

# index in ticket list with dictionary of ticket attributes
TICKET_ATTRIBUTES = 3 

# list of attribute names
STAT_FIELDS = ['type', 'component', 'resolution', 'severity', ]


def process_changes(changes):
    """Takes all changes done by sprinters and recalculate sprinters'
    statistics"""
    
    for author, tickets in changes.items():
        if '@' in author:
            sprinter = Sprinter.objects.filter(trac_email=author)
        else:
            sprinter = Sprinter.objects.filter(trac_login=author)
        if sprinter:
            sprinter = sprinter[0]
            grant_achievements(sprinter, tickets)

def get_updated_stat(stats, stat_field, ticket, attributes):
    if attributes[stat_field] in stats[stat_field]:
        return stats[stat_field][attributes[stat_field]] + [ticket['ticket_id']]
    else:
        return [ticket['ticket_id']]

def grant_achievements(sprinter, tickets):
    achievements = Achievement.objects.all()
    stats = generate_stats(tickets)
    for achievement in achievements:
        if achievement.can_grant_achievement(stats):
            sprinter.achievements.add(achievement)

def generate_stats(tickets):
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
            stats['attachment_count'].append(ticket['ticket_id'])

        # changes in tickets with given severity/component/resolution/type
        for stat_field in STAT_FIELDS:
            stats[stat_field][attributes[stat_field]] =\
                    get_updated_stat(stats, stat_field, ticket, attributes)
    return stats
