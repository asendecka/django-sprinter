from datetime import datetime
from itertools import chain
import json
import re
from django.conf import settings
from django.utils import timezone
import requests

LINK_RE = re.compile(r'<(.*)>; rel="(.*)"')

ISO_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

PULL_REQUESTS_URL = 'https://api.github.com/repos/django/django/pulls'
PER_PAGE = 100


class Client(object):
    def __init__(self):
        self.app_id = settings.GITHUB_APP_ID
        self.secret = settings.GITHUB_API_SECRET

    def get_recent_pull_requests(self, since):
        open = self.get_recent_pull_requests_status(since, 'open')
        closed = self.get_recent_pull_requests_status(since, 'closed')
        return chain(open, closed)

    def get_recent_pull_requests_status(self, since, status):
        url = PULL_REQUESTS_URL
        page = 1
        has_more_pages = True
        while has_more_pages:
            params = {
                'per_page': PER_PAGE,
                'page': page,
                'status': status,
                'client_id': self.app_id,
                'client_secret': self.secret,
            }
            resp = requests.get(url, params=params)
            resp.raise_for_status()
            pulls = json.loads(resp.content)
            for pull in pulls:
                pull_date = parse_datetime(pull['created_at'])
                if pull_date <= since:
                    has_more_pages = False
                    break
                yield pull
            else:
                header = parse_link_header(resp.header['link'])
                if 'next' not in header:
                    has_more_pages = False


def parse_datetime(datetime_str):
    d = datetime.strptime(datetime_str, ISO_FORMAT)
    return timezone.make_aware(d, timezone.utc)


def parse_link_header(header_str):
    parts = header_str.split(',')
    result = {}
    for part in parts:
        match = LINK_RE.match(part)
        url, rel = match.groups()
        result[rel] = url
    return result
