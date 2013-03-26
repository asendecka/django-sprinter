from django.contrib.auth.models import User
from django.test import TestCase
from expecter import expect
from sprinter.achievements.models import Achievement
from sprinter.userprofile.models import SprinterChange, Sprinter


class AchievementTest(TestCase):
    def test_comment_number_ok_failed(self):
        changes = [SprinterChange(ticket_id=1, field='comment', ),
                   SprinterChange(ticket_id=1, field='comment', )]
        achievement = Achievement(comment_count=2)
        expect(achievement.comment_count_ok(changes)) == False

    def test_comment_number_ok_success(self):
        changes = [SprinterChange(ticket_id=1, field='comment', ),
                   SprinterChange(ticket_id=2, field='comment', )]
        achievement = Achievement(comment_count=2)
        expect(achievement.comment_count_ok(changes)) == True

    def test_comment_number_ok_not_set(self):
        achievement = Achievement()
        expect(achievement.comment_count_ok([])) == True

    def test_attachment_count_ok_failed(self):
        changes = [SprinterChange(ticket_id=1, field='attachment', ),
                   SprinterChange(ticket_id=1, field='attachment', )]
        achievement = Achievement(attachment_count=2)
        expect(achievement.attachment_count_ok(changes)) == False

    def test_attachment_count_ok_success(self):
        changes = [SprinterChange(ticket_id=1, field='attachment', ),
                   SprinterChange(ticket_id=2, field='attachment', )]
        achievement = Achievement(attachment_count=2)
        expect(achievement.attachment_count_ok(changes)) == True

    def test_attachment_count_ok_not_set(self):
        achievement = Achievement()
        expect(achievement.attachment_count_ok([])) == True

    def test_ticket_count_ok(self):
        changes = [SprinterChange(ticket_id=1),
                   SprinterChange(ticket_id=2)]
        achievement = Achievement(ticket_count=2)
        expect(achievement.ticket_count_ok(changes)) == True

    def test_ticket_count_ok_failed(self):
        changes = [SprinterChange(ticket_id=1),
                   SprinterChange(ticket_id=1)]
        achievement = Achievement(ticket_count=2)
        expect(achievement.ticket_count_ok(changes)) == False

    def check_achievement_property(self, property_name):
        user = User.objects.create()
        sprinter = Sprinter.objects.create(user=user)
        a = SprinterChange.objects.create(
            **{'sprinter': sprinter, property_name: 'a', 'ticket_id': 1})
        b = SprinterChange.objects.create(
            **{'sprinter': sprinter, property_name: 'b', 'ticket_id': 1})
        achievement = Achievement()
        setattr(achievement, property_name, 'a')
        changes = achievement.get_changes(sprinter)
        expect(changes).contains(a)
        expect(changes).does_not_contain(b)

    def test_get_changes_component(self):
        self.check_achievement_property('component')

    def test_get_changes_resolution(self):
        self.check_achievement_property('resolution')

    def test_get_changes_kind(self):
        self.check_achievement_property('kind')

    def test_get_changes_severity(self):
        self.check_achievement_property('severity')
