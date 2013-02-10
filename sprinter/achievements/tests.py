from datetime import datetime

from django.test import TestCase
from django.contrib.auth.models import User

from sprinter.achievements.models import Sprinter, Achievement
from sprinter.achievements.proxies import TicketChangesImporter
from sprinter.achievements.processor import process_changes

from sprinter.achievements.test_data import RECENT_CHANGES, RECENT_TICKETS
from sprinter.achievements.trac_types import *

class TracClient(object):

    def get_recent_changes(self, start_date):
        return list(RECENT_CHANGES)

    def get_ticket_changelog(self, ticket):
        return list(RECENT_TICKETS[ticket]['change'])

    def get_ticket(self, ticket):
        return list(RECENT_TICKETS[ticket]['ticket'])

class AchievementsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('testuser', 'testuser@django.org', 'pass')
        self.sprinter = Sprinter.objects.create(
                trac_login='testuser', 
                trac_email='testuser@django.org',
                user=self.user,
        ) 
        self.logins = [sprinter.trac_login for sprinter in Sprinter.objects.all()]
        self.start_date = datetime(2013, 2, 1, 10, 0, 0, 0) 
        self.proxy = TicketChangesImporter(user='', password='',\
            logins=self.logins, start_date=self.start_date,\
            trac_client=TracClient())
    
    def _check_achievements(self, expects_count):
        self.assertEqual(0, self.sprinter.achievements.count())
        changes = self.proxy.fetch()
        process_changes(changes)
        self.assertEqual(expects_count, self.sprinter.achievements.count())

    def test_ticket_count(self):
        achievement = Achievement.objects.create(name='Ticket count',\
                description='Some description.', ticket_count=1)

        self._check_achievements(expects_count=1)
    
    def test_multiple_ticket_count(self):
        achievement = Achievement.objects.create(name='Ticket count',\
                description='Some description.', ticket_count=1)
        achievement = Achievement.objects.create(name='Ticket multiple',\
                description='Some description.', ticket_count=2)

        self._check_achievements(expects_count=2)

    def test_attachment_count(self):
        achievement = Achievement.objects.create(name='Patch count',\
                description='Some description.', attachment_count=1)

        self._check_achievements(expects_count=1)

    def test_multiple_attachment_count(self):
        achievement = Achievement.objects.create(name='Patch multiple',\
                description='Some description.', attachment_count=2)
        
        self._check_achievements(expects_count=0)
   
    def test_comment_count(self):
        achievement = Achievement.objects.create(name='Comment count',\
                description='Some description.', comment_count=3)

        self._check_achievements(expects_count=1)
  
    # Note: achievements with ticket type, resolution, severity, component 
    # check if the user did anything with ticket which is now with a given 
    # property. So we can check if the user did anything (i.e. comment) on 
    # a Bug ticket, but we do not check if the user changed tikcet type from
    # something else to Bug. 
    def test_ticket_type(self):
        achievement = Achievement.objects.create(name='Bug achievement',\
                description='Some description.', ticket_type=TP_BUG)
        
        other_achievement = Achievement.objects.create(name='New feature achievement',\
                description='Some description.', ticket_type=TP_FEATURE)
        self._check_achievements(expects_count=2)

    def test_severity(self):
        achievement = Achievement.objects.create(name='Realease blocker',\
                description='Some description.', severity=SV_BLOCKER)

        self._check_achievements(expects_count=1)

    def test_resolution(self):
        achievement = Achievement.objects.create(name='Wontfix',\
                description='Some description.', resolution=RS_WONTFIX)

        self._check_achievements(expects_count=1)

    def test_component(self):
        achievement = Achievement.objects.create(name='Urls change',\
                description='Some description.', component=CM_URLS)

        self._check_achievements(expects_count=1)
