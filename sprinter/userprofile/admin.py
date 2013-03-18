from django.contrib import admin
from sprinter.userprofile.models import Sprinter


class SprinterAdmin(admin.ModelAdmin):
    list_display = ('user', 'trac_login', 'trac_email', 'github_login')

admin.site.register(Sprinter, SprinterAdmin)
