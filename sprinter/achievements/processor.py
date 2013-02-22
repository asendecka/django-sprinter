from sprinter.achievements.models import Sprinter, Achievement
from sprinter.achievements.trac_types import *

# index in ticket list with dictionary of ticket attributes
TICKET_ATTRIBUTES = 3 

# list of attribute names
STAT_FIELDS = ['type', 'component', 'resolution', 'severity', ]

def create_attribute_dict(pairs):
    return dict([(name, val) for val, name in pairs])

ATTRIBUTE_DICTS = {
    'type': create_attribute_dict(TYPES),
    'component': create_attribute_dict(COMPONENTS),
    'resolution': create_attribute_dict(RESOLUTIONS),
    'severity': create_attribute_dict(SEVERITIES),
}

def get_attr_id(stat_field, attr_val):
    if stat_field not in ATTRIBUTE_DICTS or \
            attr_val not in ATTRIBUTE_DICTS[stat_field]:
        return None
    return ATTRIBUTE_DICTS[stat_field][attr_val]

def process_changes(changes, github_changes):
    """Takes all changes done by sprinters and recalculate sprinters'
    statistics"""
    
    for author, tickets in changes.items():
        if '@' in author:
            sprinter = Sprinter.objects.filter(trac_email=author)
        else:
            sprinter = Sprinter.objects.filter(trac_login=author)
        if sprinter:
            sprinter = sprinter[0]
            if sprinter.github_login in github_changes and sprinter.github_login:
                pull_requests = github_changes[sprinter.github_login]
            else:
                pull_requests = None
            grant_achievements(sprinter, tickets, pull_requests)

def get_updated_stat(stats, stat_field, ticket, attributes):
    if attributes[stat_field] in stats[stat_field]:
        return stats[stat_field][attributes[stat_field]] + [ticket['ticket_id']]
    else:
        return [ticket['ticket_id']]

def grant_achievements(sprinter, tickets, pull_requests):
    achievements = Achievement.objects.all()
    stats = generate_stats(tickets, pull_requests)
    for achievement in achievements:
        if achievement.can_grant_achievement(stats):
            sprinter.achievements.add(achievement)

def generate_stats(tickets, pull_requests):
    stats = {
        'ticket_count': set([]), 
        'attachment_count': set([]), 
        'comment_count': [], 
        'severity': {}, 
        'resolution': {}, 
        'type': {}, 
        'component': {},
    }
    
    for ticket in tickets:
        attributes = ticket['ticket'][TICKET_ATTRIBUTES]
       
        # tickets changed
        stats['ticket_count'].add(ticket['ticket_id'])

        # attachmnets added
        if attributes['has_patch'] and ticket['field'] == FD_ATTACHMENT: 
            stats['attachment_count'].add(ticket['ticket_id'])
        
        # comment count
        if ticket['field'] == FD_COMMENT: 
            stats['comment_count'].append(ticket['ticket_id'])

        # changes in tickets with given severity/component/resolution/type
        for stat_field in STAT_FIELDS:
            if stat_field in attributes:
                attr_id = get_attr_id(stat_field, attributes[stat_field])
                stats[stat_field][attr_id] =\
                        get_updated_stat(stats, stat_field, ticket, attributes)
    
    # calculate pull requests
    stats['pull_requests'] = pull_requests

    return stats

