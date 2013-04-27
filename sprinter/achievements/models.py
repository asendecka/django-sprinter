from django.db import models
import sprinter.trac.const as trac
from sprinter.userprofile.models import SprinterChange


class Achievement(models.Model):
    """Achievement with fields that specify the set of rules to gain it. 
    For now all rule fields works with AND (user has to satisfy all non-null 
    rules to receive an achievement).
    """

    name = models.CharField('Achievement title', max_length=255)
    description = models.TextField('Description')
    picture = models.ImageField(upload_to='achievements', null=True)
    secret = models.BooleanField('Is secret achievement', default=False)

    ticket_count = models.IntegerField(default=1)
    attachment_count = models.IntegerField(null=True, blank=True)
    comment_count = models.IntegerField(null=True, blank=True)
    pull_request_count = models.IntegerField(null=True, blank=True)

    severity = models.CharField(
        max_length=250, choices=trac.SEVERITIES_CHOICES, blank=True)
    resolution = models.CharField(
        max_length=250, choices=trac.RESOLUTIONS_CHOICES, blank=True)
    kind = models.CharField(
        max_length=250, choices=trac.TYPES_CHOICES, blank=True)
    component = models.CharField(
        max_length=250, choices=trac.COMPONENTS_CHOICES, blank=True)

    def can_unlock(self, sprinter_changes):
        return self.ticket_count_ok(sprinter_changes) and \
            self.comment_count_ok(sprinter_changes) and \
            self.attachment_count_ok(sprinter_changes)

    def ticket_count_ok(self, sprinter_changes):
        tickets = {change.ticket_id for change in sprinter_changes}
        ticket_count = len(tickets)
        if self.ticket_count > ticket_count:
            return False
        return True

    def comment_count_ok(self, sprinter_changes):
        if not self.comment_count:
            return True
        comment_tickets = {
            change.ticket_id for change in sprinter_changes
            if change.field == 'comment'
        }
        comment_count = len(comment_tickets)
        return self.comment_count <= comment_count

    def attachment_count_ok(self, sprinter_changes):
        if not self.attachment_count:
            return True
        attachment_tickets = {
            change.ticket_id for change in sprinter_changes
            if change.field == 'attachment'
        }
        attachment_count = len(attachment_tickets)
        return self.attachment_count <= attachment_count

    def relevant_changes(self, sprinter_changes):
        return [sc for sc in sprinter_changes if self.is_relevant(sc)]

    def is_relevant(self, sprinter_change):
        attributes = ['component', 'severity', 'resolution', 'kind']
        for attr in attributes:
            value = getattr(self, attr)
            if value and value != getattr(sprinter_change, attr):
                return False
        return True

    def __unicode__(self):
        return self.name


class Processor(object):
    def __init__(self, achievements):
        self.achievements = achievements

    def earned_achievements(self, sprinter_changes):
        return [achievement for achievement in self.achievements
                if achievement.can_unlock(sprinter_changes)]

    def grant(self, sprinters_and_changes):
        for sprinter, sprinter_changes in sprinters_and_changes:
            earned = self.earned_achievements(sprinter_changes)
            sprinter.achievements = earned


def process_achievements(sprinters):
    achievements = Achievement.objects.all()
    sprinters_and_changes = SprinterChange.objects.per_sprinter(sprinters)
    processor = Processor(achievements)
    processor.grant(sprinters_and_changes)




