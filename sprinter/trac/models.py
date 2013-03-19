from django.db import models


class Ticket(models.Model):
    kind = models.CharField('trac type', max_length=250, blank=True)
    component = models.CharField(max_length=250, blank=True)
    resolution = models.CharField(max_length=250, blank=True)
    status = models.CharField(max_length=250, blank=True)
    severity = models.CharField(max_length=250, blank=True)

    def snapshot_at(self, timestamp):
        attrs = {
            'kind': self.kind,
            'component': self.component,
            'resolution': self.resolution,
            'status': self.status,
            'severity': self.severity
        }
        for change in self.changes.order_by('-timestamp'):
            if change.timestamp < timestamp:
                break
            field = change.field
            if field == 'type':
                field = 'kind'
            if field in attrs:
                attrs[field] = change.old_value
        return TimeFrozenTicket(id=self.pk, **attrs)


class Change(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='changes')
    timestamp = models.DateTimeField()
    field = models.CharField(max_length=250, blank=True)
    author = models.CharField(max_length=250, blank=True)
    old_value = models.CharField(max_length=250, blank=True)
    new_value = models.CharField(max_length=250, blank=True)

    def ticket_snapshot(self):
        return self.ticket.snapshot_at(self.timestamp)


class TimeFrozenTicket(object):
    def __init__(self, id, kind, component, resolution, status, severity):
        self.id = id
        self.kind = kind
        self.component = component
        self.resolution = resolution
        self.status = status
        self.severity = severity

    @property
    def attrs(self):
        names = ('kind', 'component', 'resolution', 'status', 'severity')
        return {name: getattr(self, name) for name in names}
