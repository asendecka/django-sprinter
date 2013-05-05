from django.contrib import admin
from sprinter.trac.models import Ticket, Change, ImportRun


class TicketAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'kind', 'severity', 'status', 'resolution')
    list_filter = ('kind', 'severity', 'status', 'resolution')
    search_fields = ('id',)
    ordering = ('-id',)


class ChangeAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = ('__unicode__', 'ticket', 'timestamp', 'author', 'field')
    list_filter = ('field',)
    raw_id_fields = ('ticket',)
    search_fields = ('ticket__id', 'author')


class ImportRunAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp')
    ordering = ('-timestamp',)


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Change, ChangeAdmin)
admin.site.register(ImportRun, ImportRunAdmin)
