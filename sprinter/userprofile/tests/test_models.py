# encoding: utf-8
from django.contrib.auth.models import User
from django.test import TestCase
from expecter import expect
from sprinter.userprofile.models import Sprinter, SprinterChange, per_sprinter
from sprinter.userprofile.tests.factories import SprinterFactory, \
    SprinterChangeFactory, SprinterPullFactory


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

    def test_get_by_trac_author_full(self):
        author = u'Alice Zażółć Gęślą Jaźń <alice@example.com>'
        email = u'alice@example.com'
        sprinter = Sprinter.objects.create(user=self.user, trac_email=email)
        found = Sprinter.objects.get_by_trac_author(author)
        expect(found) == sprinter


class PerSprinterTest(TestCase):
    def test_per_sprinter(self):
        alice = SprinterFactory.create()
        change = SprinterChangeFactory.create(sprinter=alice)
        pull = SprinterPullFactory.create(sprinter=alice)
        generator = per_sprinter([alice])
        sprinter, sprinter_changes, sprinter_pulls = list(generator)[0]
        expect(sprinter) == alice
        expect(list(sprinter_changes)) == [change]
        expect(list(sprinter_pulls)) == [pull]
