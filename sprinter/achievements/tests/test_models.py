from django.test import TestCase
from expecter import expect
from sprinter.achievements.models import Achievement, Processor
from sprinter.userprofile.models import SprinterChange


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

    attributes = ['component', 'severity', 'resolution', 'kind']

    def test_is_relevant_single_ok(self):
        for attribute in self.attributes:
            change = SprinterChange(**{attribute: 'ok'})
            achievement = Achievement(**{attribute: 'ok'})
            expect(achievement.is_relevant(change)) == True

    def test_is_relevant_single_fail(self):
        for attribute in self.attributes:
            change = SprinterChange(**{attribute: 'ok'})
            achievement = Achievement(**{attribute: 'not ok'})
            expect(achievement.is_relevant(change)) == False

    def test_is_relevant_component_not_specified(self):
        achievement = Achievement()
        for attribute in self.attributes:
            change = SprinterChange(**{attribute: 'ok'})
            expect(achievement.is_relevant(change)) == True

    def test_is_relevant_many_ok(self):
        kwargs = {attr: attr for attr in self.attributes}
        change = SprinterChange(**kwargs)
        kwargs.pop('component')
        achievement = Achievement(**kwargs)
        expect(achievement.is_relevant(change)) == True

    def test_is_relevant_many_fail(self):
        kwargs = {attr: attr for attr in self.attributes}
        achievement = Achievement(**kwargs)
        kwargs.pop('component')
        change = SprinterChange(**kwargs)
        expect(achievement.is_relevant(change)) == False

    def test_relevant_changes(self):
        ok = SprinterChange(pk=1, component='Forms')
        not_ok = SprinterChange(pk=2, component='ORM')
        achievement = Achievement(component='Forms')
        changes = [ok, not_ok]
        filtered = achievement.relevant_changes(changes)
        expect(filtered) == [ok]


class ProcessorTest(TestCase):
    def test_earns_only_unlockable_achievements(self):
        ok = FakeAchievement()
        not_ok = FakeAchievement(can_unlock=False)
        achievements = [ok, not_ok]
        sprinter_changes = [SprinterChange()]
        processor = Processor(achievements)
        earned = processor.earned_achievements(sprinter_changes)
        expect(earned) == [ok]

    def test_grant(self):
        ok = FakeAchievement(can_unlock=True)
        not_ok = FakeAchievement(can_unlock=False)
        processor = Processor([ok, not_ok])
        sprinter = FakeSprinter()
        sprinters_and_changes = [(sprinter, [])]
        processor.grant(sprinters_and_changes)
        expect(sprinter.achievements) == [ok]


class FakeAchievement(object):
    def __init__(self, can_unlock=True, relevant=()):
        self._can_unlock = can_unlock
        self._relevant = set(relevant)

    def can_unlock(self, sprinter_changes):
        return self._can_unlock


class FakeSprinter(object):
    def __init__(self):
        self.achievements = []
