from django.db import models


class PullRequest(models.Model):
    number = models.IntegerField(unique=True)
    login = models.CharField(max_length=250)
    created_at = models.DateTimeField()
