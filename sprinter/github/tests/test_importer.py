from datetime import datetime
from django.test import TestCase
from django.utils.timezone import make_aware, utc
from expecter import expect
from sprinter.github.importer import Importer
from sprinter.github.models import PullRequest
from sprinter.userprofile.models import SprinterPull
from sprinter.userprofile.tests.factories import SprinterFactory


class ImporterTest(TestCase):
    def setUp(self):
        self.since = make_aware(datetime(2013, 1, 1, 13, 46), utc)
        self.proxy = FakeClient()
        self.importer = Importer(self.proxy)

    def test_pull_requests_get_created(self):
        self.importer.sync(self.since)
        expect(PullRequest.objects.count()) == 2

    def test_sync_is_idempotent(self):
        self.importer.sync(self.since)
        self.importer.sync(self.since)
        expect(PullRequest.objects.count()) == 2

    def test_adds_sprinter_pulls(self):
        SprinterFactory.create(github_login='oinopion')
        self.importer.sync(self.since)
        expect(SprinterPull.objects.count()) == 1


class FakeClient(object):
    def get_recent_pull_requests(self, since):
        return [
            {
                'number': 1,
                'user': {'login': 'octocat'},
                'created_at': '2012-05-13T14:55:45Z',
            },
            {
                'number': 2,
                'user': {'login': 'oinopion'},
                'created_at': '2012-05-12T11:45:45Z',
            },
        ]
