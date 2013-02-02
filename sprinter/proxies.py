from xmlrpclib import ServerProxy

class TracProxy(object):
    url = 'https://djangosprinter:djangosprinter13@code.djangoproject.com/login/rpc'
    
    def fetch(self, start_date=None, logins=[]):
        p = ServerProxy(self.url)
        changed_tickets = p.ticket.getRecentChanges(start_date)
        
        changes = {}
        for login in logins:
            changes[login] = []
        return changes
        for ticket in changed_tickets:
            change_log = p.ticket.changeLog(ticket)
            if change_log:
                (change_time, author, field, old, new, permanent) = change_log.pop()
                while change_time > start_date and change_log: 
                    if change_time > start_date and author in logins:
                        changes[author].append({
                            #'ticket': ticket,
                            #'time': change_time, 
                            #'author': author, 
                            #'old': old, 
                            #'new': new,
                            'field': field,
                        })
                    (change_time, author, field, old, new, permanent) = change_log.pop()

        return changes
