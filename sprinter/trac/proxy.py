from xmlrpclib import ServerProxy


class Client(object):
    TRAC_URL = 'code.djangoproject.com/login/rpc'

    def __init__(self, user, password):
        self.user = user
        self.password = password
        url = 'https://%s:%s@%s' % (self.user, self.password, self.TRAC_URL)
        self.proxy = ServerProxy(url)

    def get_recent_changes(self, since):
        return self.proxy.ticket.getRecentChanges(since)

    def get_ticket_changelog(self, ticket_id):
        return self.proxy.ticket.changeLog(ticket_id)

    def get_ticket(self, ticket_id):
        return self.proxy.ticket.get(ticket_id)
