from datetime import datetime
from django.utils.timezone import utc
import factory
from sprinter.github.models import PullRequest


class PullRequestFactory(factory.DjangoModelFactory):
    FACTORY_FOR = PullRequest

    @factory.sequence
    def number(self):
        return self

    login = 'octocat'
    created_at = datetime(2013, 3, 7, 10, 34, tzinfo=utc)
