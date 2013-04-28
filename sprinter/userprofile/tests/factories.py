import factory
from django.contrib.auth.models import User
from sprinter.github.tests.factories import PullRequestFactory
from sprinter.trac.tests.factories import ChangeFactory
from sprinter.userprofile.models import Sprinter, SprinterChange, SprinterPull


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    @factory.sequence
    def username(self):
        return 'user-%s' % self


class SprinterFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Sprinter

    user = factory.SubFactory(UserFactory)

    @factory.lazy_attribute
    def trac_login(self):
        return self.user.username


class SprinterChangeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SprinterChange

    sprinter = factory.SubFactory(SprinterFactory)
    ticket_change = factory.SubFactory(ChangeFactory)

    @factory.lazy_attribute
    def ticket_id(self):
        return self.ticket_change.ticket_id


class SprinterPullFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SprinterPull

    sprinter = factory.SubFactory(SprinterFactory)

    pull_request = factory.SubFactory(PullRequestFactory)
