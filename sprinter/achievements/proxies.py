from xmlrpclib import ServerProxy
from copy import copy
from pyhole import PyHole
from datetime import datetime
from dateutil import parser, tz

from django.utils.simplejson import loads

def init_changes(logins):
    changes = {}
    for login in logins:
        changes[login] = []
    return changes

class GithubClient(object):
    GITHUB_URL = 'https://api.github.com/repos/django/django'

    def __init__(self):
        self.proxy = PyHole(self.GITHUB_URL)

    def get_pull_requests_page(self, page_no=None):
        return self.proxy(page=page_no).pulls.get()

    def get_recent_pull_requests(self, start_date, page_no=None):
        pull_requests = []
        page = loads(self.get_pull_requests_page(page_no=page_no))
        stop = False
        for element in page:
            print "element login", element['user']['login']
            from django.utils import timezone
            current_date = timezone.make_aware(parser.parse(element['created_at']),\
                    timezone.get_default_timezone())
            start_date = timezone.make_aware(start_date, timezone.get_default_timezone())
            if current_date.astimezone(tz.tzutc()) < start_date:
                stop = True
                break
            pull_requests.append(element)

        if not stop:
            page_no = page_no + 1 if page_no else 2
            pull_requests = pull_requests +\
                    self.get_recent_pull_requests(page_no=page_no)
        return pull_requests

class GithubImporter(object):
    
    def __init__(self, logins, start_date, github_client=None):
        self.github_client = github_client or GithubClient()
        self.logins = logins
        self.start_date = start_date
    
    def fetch(self):
        pull_requests = self.github_client.get_recent_pull_requests(\
                self.start_date) 

        changes = init_changes(self.logins) 

        for pull_request in pull_requests:
            if pull_request['user']['login'] in self.logins:
                changes[pull_request['user']['login']].append(\
                        pull_request['number'])

        return changes


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
        self.trac_client = trac_client or TracClient(user, password)
        self.logins = logins
        self.start_date = start_date

    def process_ticket_changelog(self, ticket_id, change_log, changes, ticket):
        updated_changes = copy(changes)
        for change_time, author, field, old, new, permanent in reversed(change_log):
            if change_time < self.start_date:
                break

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
        return updated_changes

    def fetch(self):
        recent_changes = self.trac_client.get_recent_changes(self.start_date) 
        changes = init_changes(self.logins) 

        for ticket_id in recent_changes:
            change_log = self.trac_client.get_ticket_changelog(ticket_id)
            ticket = self.trac_client.get_ticket(ticket_id)
            if change_log:
                changes = self.process_ticket_changelog(ticket_id, change_log,\
                        changes, ticket)

        return changes
