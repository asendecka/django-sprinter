from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from sprinter.achievements.models import process_achievements
from sprinter.trac.importer import Importer as TracImporter
from sprinter.github.importer import Importer as GithubImporter
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
            since = now - timedelta(days=3)
        ImportRun.objects.create(timestamp=now)

        changed_sprinters = set()
        trac_importer = TracImporter()
        changed_sprinters.update(trac_importer.sync(since))

        github_importer = GithubImporter()
        changed_sprinters.update(github_importer.sync(since))
        process_achievements(changed_sprinters)
