from django.contrib import admin
from sprinter.achievements.models import Achievement, Sprinter

class AchievementAdmin(admin.ModelAdmin):
    pass

class SprinterAdmin(admin.ModelAdmin):
    pass

admin.site.register(Achievement, AchievementAdmin)
admin.site.register(Sprinter, SprinterAdmin)
