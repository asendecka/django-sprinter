from django.db import models
import sprinter.trac.const as trac


class Achievement(models.Model):
    """Achievement with fields that specify the set of rules to gain it. 
    For now all rule fields works with AND (user has to satisfy all non-null 
    rules to receive an achievement).
    """

    name = models.CharField('Achievement title', max_length=255)
    description = models.CharField('Description', max_length=2000)
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

    def can_unlock(self, sprinter):
        sprinter_changes = self.get_changes(sprinter)
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

    def get_changes(self, sprinter):
        qs = sprinter.changes.all()
        for property_name in ['severity', 'resolution', 'kind', 'component']:
            property = getattr(self, property_name)
            if property:
                qs = qs.filter(**{property_name: property})
        return list(qs)

    def __unicode__(self):
        return self.name




