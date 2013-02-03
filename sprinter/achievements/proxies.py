from xmlrpclib import ServerProxy
from copy import copy

class TracClient(object):
    TRAC_URL = 'code.djangoproject.com/login/rpc'

    def __init__(self, user, password):
        self.user = user
        self.password = password
        url = 'https://%s:%s@%s' % (self.user, self.password, self.TRAC_URL) 
        self.proxy = ServerProxy(url)

    def get_recent_changes(self, start_date):
        return self.proxy.ticket.getRecentChanges(start_date)

    def get_ticket_changelog(self, ticket):
        return self.proxy.ticket.changeLog(ticket)

    def get_ticket(self, ticket):
        return self.proxy.ticket.get(ticket)

class TicketChangesImporter(object):
    
    def __init__(self, user, password, logins, start_date, trac_client=None):
        self.trac_client = trac_client if trac_client else TracClient(user, password)
        self.logins = logins
        self.start_date = start_date

    def init_changes(self, logins):
        changes = {}
        for login in logins:
            changes[login] = []
        return changes

    def process_ticket_changelog(self, ticket_id, change_log, changes, ticket):
        updated_changes = copy(changes)
        (change_time, author, field, old, new, permanent) = change_log.pop()
        while change_time > self.start_date and change_log: 
            if author in self.logins:
                updated_changes[author].append({
                    'ticket_id': ticket_id,
                    'ticket': ticket,
                    'time': change_time, 
                    'author': author, 
                    'old': old, 
                    'new': new,
                    'field': field,
                })
            (change_time, author, field, old, new, permanent) = change_log.pop()
        return updated_changes

    def fetch(self):
        recent_changes = self.trac_client.get_recent_changes(self.start_date) 
        changes = self.init_changes(self.logins) 

        for ticket_id in recent_changes:
            change_log = self.trac_client.get_ticket_changelog(ticket_id)
            ticket = self.trac_client.get_ticket(ticket_id)
            if change_log:
                changes = self.process_ticket_changelog(ticket_id, change_log,\
                        changes, ticket)

        return changes
