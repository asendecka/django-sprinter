from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

from sprinter.achievements.proxies import TicketChangesImporter, GithubImporter
from sprinter.achievements.models import Sprinter, Achievement
from sprinter.achievements.processor import process_changes

class Command(BaseCommand):
    args = '<user> <password>'
    help = 'Pass trac user and password to recalculate achievements.'

    def handle(self, user, password, *args, **options):
        logins = [sprinter.trac_login for sprinter in Sprinter.objects.all()]
        github_logins = [sprinter.github_login for sprinter in\
                Sprinter.objects.all()]
        start_date = datetime(2013, 2, 9, 10, 0, 0, 0) # TODO: customize date

        proxy = TicketChangesImporter(user=user, password=password,\
            logins=logins, start_date=start_date)
        changes = proxy.fetch()
        github_proxy = GithubImporter(logins=github_logins,\
                start_date=start_date)
        github_changes = proxy.fetch()
        process_changes(changes, github_changes)
        
