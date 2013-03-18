from datetime import datetime, timedelta
from django.test import TestCase
from django.utils.timezone import make_aware, utc
from expecter import expect
from sprinter.trac.models import Ticket


class TimeFrozenTicketTest(TestCase):

    def setUp(self):
        self.timestamp = make_aware(datetime(2013, 1, 1), utc)

    def test_no_changes_snapshot(self):
        ticket = Ticket.objects.create(status='new')
        snapshot = ticket.snapshot_at(self.timestamp)
        expect(snapshot.status) == ticket.status

    def test_status_change(self):
        ticket = Ticket.objects.create(status='new')
        ticket.changes.create(
            timestamp=self.timestamp,
            field='status',
            author='alice',
            old_value='old',
            new_value='new',
        )
        snapshot = ticket.snapshot_at(self.timestamp - timedelta(hours=1))
        expect(snapshot.status) == 'old'

    def test_snapshot_between_two_changes(self):
        ticket = Ticket.objects.create(status='new')
        ticket.changes.create(
            timestamp=self.timestamp - timedelta(hours=3),
            field='status',
            author='alice',
            old_value='very-old',
            new_value='slightly-old',
        )
        ticket.changes.create(
            timestamp=self.timestamp,
            field='status',
            author='alice',
            old_value='slightly-old',
            new_value='new',
        )
        snapshot = ticket.snapshot_at(self.timestamp - timedelta(hours=1))
        expect(snapshot.status) == 'slightly-old'

