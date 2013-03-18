from django.contrib.auth.models import User
from django.test import TestCase
from expecter import expect
from sprinter.userprofile.models import Sprinter


class SprinterManagerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='alice')

    def test_get_by_trac_author_login(self):
        sprinter = Sprinter.objects.create(user=self.user, trac_login='Alice')
        found = Sprinter.objects.get_by_trac_author('alice')
        expect(found) == sprinter

    def test_get_by_trac_author_email(self):
        email = 'Alice@Example.com'
        sprinter = Sprinter.objects.create(user=self.user, trac_email=email)
        found = Sprinter.objects.get_by_trac_author(email.lower())
        expect(found) == sprinter
