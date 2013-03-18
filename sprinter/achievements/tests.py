from datetime import datetime

from django.test import TestCase
from django.contrib.auth.models import User

from sprinter.achievements.models import Sprinter, Achievement
from sprinter.achievements.proxies import TicketChangesImporter, \
        GithubImporter
from sprinter.achievements.processor import process_changes

from sprinter.achievements.test_data import RECENT_CHANGES, RECENT_TICKETS, \
        PULL_REQUESTS
from sprinter.achievements.trac_types import *

class TracClient(object):

    def get_recent_changes(self, start_date):
        return list(RECENT_CHANGES)

    def get_ticket_changelog(self, ticket):
        return list(RECENT_TICKETS[ticket]['change'])

    def get_ticket(self, ticket):
        return list(RECENT_TICKETS[ticket]['ticket'])

class GithubClient(object):

    def get_pull_requests_page(self, page_no=None):
        return PULL_REQUESTS

    def get_recent_pull_requests(self, start_date, page_no=None):
        return PULL_REQUESTS


class AchievementsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('testuser', 'testuser@django.org', 'pass')
        self.sprinter = Sprinter.objects.create(
                trac_login='testuser', 
                trac_email='testuser@django.org',
                user=self.user,
                github_login='sprinter',
        ) 
        self.logins = [sprinter.trac_login for sprinter in Sprinter.objects.all()]
        self.github_logins = [sprinter.github_login for sprinter in Sprinter.objects.all()]
        self.start_date = datetime(2013, 2, 1, 10, 0, 0, 0) 
        self.proxy = TicketChangesImporter(user='', password='',\
            logins=self.logins, start_date=self.start_date,\
            trac_client=TracClient())
        self.proxy = TicketChangesImporter(user='', password='',\
            logins=self.logins, start_date=self.start_date,\
            trac_client=TracClient())
        
        self.logins = [sprinter.trac_login for sprinter in Sprinter.objects.all()]
        self.github_proxy = GithubImporter(logins=self.github_logins, \
                start_date=self.start_date, github_client=GithubClient())
    
    def _check_achievements(self, expects_count):
        self.assertEqual(0, self.sprinter.achievements.count())
        changes = self.proxy.fetch()
        process_changes(changes, [])
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

    def test_complex_achievements(self):
        achievement = Achievement.objects.create(name='Complex achievement 1',\
                description='Some description.', comment_count=3,\
                ticket_count=1, severity=SV_NORMAL, ticket_type=TP_BUG,\
                resolution=RS_WORKS)

        other_achievement = Achievement.objects.create(name='Complex 2',\
                description='Some description.', comment_count=1,\
                attachment_count=1, severity=SV_BLOCKER)
        
        another_achievement = Achievement.objects.create(name='Complex 3',\
                description='Some description.', comment_count=2,\
                attachment_count=1, severity=SV_NORMAL, resolution=RS_WORKS,\
                component=CM_URLS, ticket_type=TP_BUG)

        self._check_achievements(expects_count=2)

    def test_pull_request(self):
        achievement = Achievement.objects.create(name='Github',\
                description='Some description.', pull_request_count=1)
        
        achievement = Achievement.objects.create(name='Github Multi',\
                description='Some description.', pull_request_count=2)

        changes = self.github_proxy.fetch()
        process_changes({}, changes)
        self.assertEqual(1, self.sprinter.achievements.count())
    
    def test_pull_request_empty_login(self):
        achievement = Achievement.objects.create(name='Github',\
                description='Some description.', pull_request_count=1)
        
        achievement = Achievement.objects.create(name='Github Multi',\
                description='Some description.', pull_request_count=2)
        
        self.assertEqual(0, self.sprinter.achievements.count())
        changes = self.github_proxy.fetch()
        process_changes({}, changes)
        self.assertEqual(0, self.sprinter.achievements.count())
