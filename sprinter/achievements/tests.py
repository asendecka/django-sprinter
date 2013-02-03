from datetime import datetime

from django.test import TestCase
from django.contrib.auth.models import User

from sprinter.achievements.models import Sprinter, Achievement
from sprinter.achievements.proxies import TicketChangesImporter
from sprinter.achievements.processor import process_changes

from sprinter.achievements.test_data import RECENT_CHANGES, RECENT_TICKETS

class TracClient(object):

    def get_recent_changes(self, start_date):
        return list(RECENT_CHANGES)

    def get_ticket_changelog(self, ticket):
        return list(RECENT_TICKETS[ticket]['change'])

    def get_ticket(self, ticket):
        return list(RECENT_TICKETS[ticket]['ticket'])

class AchievementsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('testuser', 'testuser@django.org', 'pass')
        self.sprinter = Sprinter.objects.create(
                trac_login='testuser', 
                trac_email='testuser@django.org',
                user=self.user,
        ) 
        self.logins = [sprinter.trac_login for sprinter in Sprinter.objects.all()]
        self.start_date = datetime(2013, 2, 1, 10, 0, 0, 0) 

    def test_ticket_count(self):
        achievement = Achievement.objects.create(name='Ticket count',\
                description='Some description.', ticket_count=1)

        self.assertEqual(0, self.sprinter.achievements.count())
        proxy = TicketChangesImporter(user='', password='',\
            logins=self.logins, start_date=self.start_date,\
            trac_client=TracClient())
        changes = proxy.fetch()
        process_changes(changes)
        self.assertEqual(1, self.sprinter.achievements.count())

    def test_attachment_count(self):
        achievement = Achievement.objects.create(name='Ticket count',\
                description='Some description.', attachment_count=1)

        self.assertEqual(0, self.sprinter.achievements.count())
        proxy = TicketChangesImporter(user='', password='',\
            logins=self.logins, start_date=self.start_date,\
            trac_client=TracClient())
        changes = proxy.fetch()
        process_changes(changes)
        self.assertEqual(1, self.sprinter.achievements.count())
