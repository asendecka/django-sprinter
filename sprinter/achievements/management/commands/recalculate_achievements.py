from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from sprinter.achievements.models import process_achievements
from sprinter.trac.importer import Importer
from sprinter.trac.models import ImportRun


class Command(BaseCommand):
    args = '<user> <password>'
    help = 'Pass trac user and password to recalculate achievements.'

    def handle(self, *args, **options):
        now = timezone.now()
        try:
            last_import_run = ImportRun.objects.latest('timestamp')
            since = last_import_run.timestamp
        except ImportRun.DoesNotExist:
            since = now - timedelta(days=30)
        ImportRun.objects.create(timestamp=now)

        importer = Importer()
        changed_sprinters = importer.sync(since)
        process_achievements(changed_sprinters)

