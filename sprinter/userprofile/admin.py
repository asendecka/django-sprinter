from django.contrib import admin
from sprinter.userprofile.models import Sprinter


class AchievementInline(admin.StackedInline):
    model = Sprinter.achievements.through
    verbose_name = 'Achievement'
    verbose_name_plural = 'Achievements'
    extra = 0


class SprinterAdmin(admin.ModelAdmin):
    list_display = ('user', 'trac_login', 'trac_email', 'github_login')
    inlines = (AchievementInline,)
    exclude = ('achievements',)
    readonly_fields = ('user',)

admin.site.register(Sprinter, SprinterAdmin)
