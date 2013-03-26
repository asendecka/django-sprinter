from datetime import datetime, timedelta
from xmlrpclib import DateTime
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import utc, make_aware
from expecter import expect
from sprinter.trac.importer import Importer
from sprinter.trac.models import Ticket
from sprinter.userprofile.models import SprinterChange, Sprinter


class ImporterTest(TestCase):
    def setUp(self):
        self.since = make_aware(datetime(2013, 1, 1, 13, 46), utc)
        self.proxy = FakeProxy(self.since)
        self.importer = Importer(self.proxy)

    def test_changed_tickets_get_created(self):
        self.importer.sync(self.since)
        expect(Ticket.objects.count()) == 2

    def test_created_tickets_get_attributes(self):
        self.importer.sync(self.since)
        ticket = Ticket.objects.all()[0]
        expect(ticket.component) == u'Forms'
        expect(ticket.severity) == u'Normal'
        expect(ticket.status) == u'new'
        expect(ticket.kind) == u'New feature'
        expect(ticket.resolution) == u''

    def test_tickets_get_changes(self):
        self.importer.sync(self.since)
        ticket = Ticket.objects.all()[0]
        expect(len(ticket.changes.all())) == 2

    def test_ticket_change_get_attributes(self):
        self.importer.sync(self.since)
        ticket = Ticket.objects.all()[0]
        change = ticket.changes.latest('timestamp')
        expect(change.author) == u'bob'
        expect(change.field) == u'status'
        expect(change.old_value) == u'new'
        expect(change.new_value) == u'assigned'

    def test_sync_is_idempotent(self):
        self.importer.sync(self.since)
        self.importer.sync(self.since)
        expect(Ticket.objects.count()) == 2
        ticket = Ticket.objects.all()[0]
        expect(ticket.changes.count()) == 2

    def test_no_sprinter_no_change(self):
        self.importer.sync(self.since)
        expect(SprinterChange.objects.count()) == 0

    def test_adds_sprinter_changes(self):
        user = User.objects.create(username='alice')
        sprinter = Sprinter.objects.create(user=user, trac_login='alice')
        self.importer.sync(self.since - timedelta(hours=1))
        expect(SprinterChange.objects.count()) == 2
        sprinter_change = sprinter.changes.latest('pk')
        expect(sprinter_change.field) == u'comment'
        expect(sprinter_change.kind) == u'New feature'
        expect(sprinter_change.status) == u'new'
        expect(sprinter_change.severity) == u'Normal'
        expect(sprinter_change.resolution) == u''
        expect(sprinter_change.ticket_id) == 12345


class FakeProxy(object):
    def __init__(self, dt=None):
        self.dt = dt or datetime(2010, 1, 1, 13, 45)

    def get_recent_changes(self, since):
        assert isinstance(since, datetime)
        return [1234, 12345]

    def get_ticket_changelog(self, ticket_id):
        assert isinstance(ticket_id, int)
        dt = DateTime(self.dt)
        return [
            [dt, 'alice', 'comment', '28', '', 1],
            [dt, 'bob', 'status', 'new', 'assigned', 1],
        ]

    def get_ticket(self, ticket_id):
        assert isinstance(ticket_id, int)
        dt = DateTime(self.dt)
        attributes = {
            'component': 'Forms',
            'severity': 'Normal',
            'status': 'new',
            'type': 'New feature',
            'resolution': '',
        }
        return [ticket_id, dt, dt, attributes]
