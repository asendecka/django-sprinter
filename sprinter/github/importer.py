from collections import defaultdict
from sprinter.github.models import PullRequest
from sprinter.github.proxy import parse_datetime
from sprinter.userprofile.models import Sprinter, SprinterPull


class Importer(object):
    def __init__(self, client):
        self.client = client

    def sync(self, since):
        created_pull_requests = defaultdict(list)
        for pull_data in self.client.get_recent_pull_requests(since):
            number = pull_data['number']
            login = pull_data['user']['login']
            created_at = parse_datetime(pull_data['created_at'])
            pr, created = PullRequest.objects.get_or_create(
                number=number, defaults={
                    'login': login,
                    'created_at': created_at
                }
            )
            if created:
                created_pull_requests[login].append(pr)

        for login, pull_requests in created_pull_requests.iteritems():
            try:
                sprinter = Sprinter.objects.get(github_login=login)
                pulls = [SprinterPull(pull_request=pr) for pr in pull_requests]
                sprinter.pulls.add(*pulls)
            except Sprinter.DoesNotExist:
                pass


