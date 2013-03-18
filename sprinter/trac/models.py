from django.db import models


class Ticket(models.Model):
    kind = models.CharField('trac type', max_length=250, blank=True)
    component = models.CharField(max_length=250, blank=True)
    resolution = models.CharField(max_length=250, blank=True)
    status = models.CharField(max_length=250, blank=True)
    severity = models.CharField(max_length=250, blank=True)


class Change(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='changes')
    timestamp = models.DateTimeField()
    field = models.CharField(max_length=250, blank=True)
    author = models.CharField(max_length=250, blank=True)
    old_value = models.CharField(max_length=250, blank=True)
    new_value = models.CharField(max_length=250, blank=True)


