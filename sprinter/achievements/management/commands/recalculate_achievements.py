from django.core.management.base import BaseCommand, CommandError
from sprinter.achievements.proxies import TicketChangesImporter
from sprinter.achievements.models import Sprinter

class RecalculateAchievements(BaseCommand):
    args = '<user> <password>'
    help = 'Pass trac user and password to recalculate achievements.'

    def handle(self, user, password, *args, **options):
        logins = [sprinter.trac_login for sprinter in Sprinter.objects.all()]
        start_date = datetime(2013, 2, 1, 10, 0, 0, 0) # TODO: customize date

        proxy = TicketChangesImporter(user=user, password=password,\
            logins=logins, start_date=start_date)
        changes = proxy.fetch()
        self.process_changes(changes)
        
    def process_changes(self, changes):
        """Takes all changes done by sprinters and recalculate sprinters'
        statistics"""
        pass   
