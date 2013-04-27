import factory
from datetime import datetime
from django.utils import timezone
from sprinter.trac.models import Ticket, Change


class TicketFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Ticket

    kind = 'Bug'
    component = 'Forms'
    resolution = ''
    status = 'new'
    severity = 'Normal'


class ChangeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Change

    ticket = factory.SubFactory(TicketFactory)
    timestamp = datetime(2013, 1, 13, 20, 45, tzinfo=timezone.utc)
    field = 'comment'
    author = 'alice'
    old_value = ''
    new_value = 'Comment'
