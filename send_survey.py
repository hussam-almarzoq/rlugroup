# -*- coding: utf-8  -*-
import datetime
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

from django.conf import settings
from events.models import Attendee, Event
from post_office import mail


queued_addresses = [] # To aviod sending an email twice.

event_pk = int(sys.argv[1])
survey_url = sys.argv[2]

event = Event.objects.get(pk=event_pk)

print u"Surveing {0} attendees with: {1}".format(event.name, survey_url).encode('utf-8')

for attendee in event.attendee_set.filter(is_counted=True):
    if attendee.email in queued_addresses:
        continue
    else:
        queued_addresses.append(attendee.email)

    print u"Queuing the survey to {0}".format(attendee.email).encode('utf-8')
    mail.send([attendee.email], settings.EVENT_FROM_EMAIL,
              template='event_survey',
              context={'event': event,'attendee': attendee,
                       'survey_url': survey_url})
