from datetime import datetime
from django.utils.timezone import utc, make_aware
from sprinter.trac.models import Ticket, Change


class Importer(object):
    def __init__(self, proxy):
        self.proxy = proxy

    def sync(self, since):
        ticket_ids = self.proxy.get_recent_changes(since)
        for ticket_id in ticket_ids:
            self.sync_ticket(ticket_id)

    def sync_ticket(self, ticket_id):
        ticket_data = self.proxy.get_ticket(ticket_id)
        id_, created, changed, attributes = ticket_data
        defaults = {
            'kind': attributes['type'],
            'component': attributes['component'],
            'resolution': attributes['resolution'],
            'severity': attributes['severity'],
            'status': attributes['status'],
        }
        ticket, was_created = Ticket.objects.get_or_create(
            pk=ticket_id, defaults=defaults)

        self.sync_ticket_changes(ticket)

    def sync_ticket_changes(self, ticket):
        ticket_changelog_data = self.proxy.get_ticket_changelog(ticket.pk)
        try:
            last_recorded_change = ticket.changes.latest('timestamp')
            last_recorded_timestamp = last_recorded_change.timestamp
        except Change.DoesNotExist:
            last_recorded_timestamp = make_aware(datetime(1970, 1, 1), utc)
        for data in ticket_changelog_data:
            time, author, field, old_value, new_value, permanent = data
            timestamp = datetime.strptime(time.value, "%Y%m%dT%H:%M:%S")
            timestamp = make_aware(timestamp, utc)

            if timestamp > last_recorded_timestamp:
                ticket.changes.create(
                    timestamp=timestamp, author=author, field=field,
                    old_value=old_value, new_value=new_value)


