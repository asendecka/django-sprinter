from django.contrib import admin
from sprinter.github.models import PullRequest


class PullRequestAdmin(admin.ModelAdmin):
    pass

admin.site.register(PullRequest, PullRequestAdmin)
