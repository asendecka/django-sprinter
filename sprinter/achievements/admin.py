from django.contrib import admin
from sprinter.achievements.models import Achievement


class AchievementAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'secret', 'ticket_count', 'attachment_count',
        'comment_count', 'pull_request_count', 'severity', 'resolution',
        'kind', 'component'
    )
    list_filter = ('component', 'kind', 'severity',)

admin.site.register(Achievement, AchievementAdmin)
