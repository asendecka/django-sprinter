from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = '<user> <password>'
    help = 'Pass trac user and password to recalculate achievements.'

    def handle(self, user, password, *args, **options):
        pass
