from django.contrib import admin
from sprinter.github.models import PullRequest


class PullRequestAdmin(admin.ModelAdmin):
    list_display = ('number', 'login', 'created_at')

admin.site.register(PullRequest, PullRequestAdmin)
