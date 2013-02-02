from datetime import datetime
import os

from django.http import HttpResponse
from django.shortcuts import render_to_response

from sprinter.achievements.models import Sprinter
from sprinter.achievements.proxies import TicketChangesImporter

def board(request):
    start_date = datetime(2013, 2, 1, 10, 0, 0, 0)
    logins = [sprinter.trac_login for sprinter in Sprinter.objects.all()]
    user = os.environ['TRAC_USER']
    password = os.environ['TRAC_PASSWORD']
    proxy = TicketChangesImporter(user=user, password=password, logins=logins,\
            start_date=start_date)
    changes = proxy.fetch()

    return render_to_response('achievements/board.html', {'changes': changes})
