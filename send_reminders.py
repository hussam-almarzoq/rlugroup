# -*- coding: utf-8  -*-
import datetime
import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rlugroup.settings")

from django.conf import settings
from django.core.urlresolvers import reverse
from events.models import Attendee, Event
from post_office import mail

now = datetime.datetime.now()
two_days_latter = datetime.datetime.today().date() + datetime.timedelta(2)

for event in Event.objects.filter(starting_date__gte=now):
    print event.starting_date.date() == two_days_latter, event.starting_date.date(), two_days_latter
    if event.starting_date.date() == two_days_latter:
        print u"It will be two days until {0}. Scanning its attendees.".format(event.name).encode('utf-8')
        for attendee in event.attendee_set.filter(is_counted=True):
            print u"Adding a reminder to {0} for {1}".format(attendee.email, event.name).encode('utf-8')
            attendee_url = reverse('events:show_attendee',
                                   args=(event.pk, attendee.slug))
            mail.send([attendee.email], settings.EVENT_FROM_EMAIL,
                      template='remind_attendee',
                      context={'event': event,'attendee': attendee,
                               'attendee_url': attendee_url})
