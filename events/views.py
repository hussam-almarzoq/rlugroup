# -*- coding: utf-8  -*-
import datetime
import string
import random

from django import forms
from django.conf import settings
from django.utils import timezone
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required, login_required

from datetimewidget.widgets import DateTimeWidget
from post_office import mail
from events.models import Event, Attendee, Organizer


class EventForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        if 'ending_date' in cleaned_data and 'starting_date' \
           in cleaned_data:
            if cleaned_data['starting_date'] > cleaned_data['ending_date']:
                msg = u'تاريخ انتهاء الحدث بعد تاريخ بدئه!'
                # Add an error message to specific fields.
                self._errors["starting_date"] = self.error_class([msg])
                self._errors["ending_date"] = self.error_class([msg])
                # Remove invalid fields
                del cleaned_data["starting_date"]
                del cleaned_data["ending_date"]

        if 'starting_date' in cleaned_data and 'announcement_date' \
           in cleaned_data:
            if cleaned_data['announcement_date'] > cleaned_data['starting_date'].date():
                msg = u'تاريخ الإعلان عن الحدث بعد تاريخ بدئه!'
                # Add an error message to specific fields.
                self._errors["starting_date"] = self.error_class([msg])
                self._errors["announcement_date"] = self.error_class([msg])
                # Remove invalid fields
                del cleaned_data["starting_date"]
                del cleaned_data["announcement_date"]

        return cleaned_data

    class Meta:
        model = Event
        fields = ['name', 'location', 'location_description',
                  'long_position', 'lat_position',
                  'short_description', 'description', 'starting_date',
                  'ending_date', 'announcement_date', 'max_attendees', 'available_to']
        widgets = {
             'starting_date': DateTimeWidget(attrs={'id':"starting_date"}),
             'ending_date': DateTimeWidget(attrs={'id':"starting_date"})
         }

class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = ['name', 'email', 'gender', 'add_to_mailing_list',
                  'referral']

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organizer
        fields = ['name', 'email', 'gender', 'add_to_mailing_list']

def home(request):
    now = timezone.now()
    # Only show events that are on or past the announcement date.
    events = Event.objects.filter(announcement_date__lte=now).order_by('-starting_date')

    next_event_query = Event.objects.filter(announcement_date__lte=now, starting_date__gte=now).order_by('starting_date')

    if next_event_query:
        next_event = next_event_query[0]
    else:
        next_event = None

    paginator = Paginator(events, 25)
    page = request.GET.get('page')

    try:
        page_events = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_events = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_events = paginator.page(paginator.num_pages)

    context = {'page_events': page_events, 'next_event': next_event}

    return render(request, 'events/home.html', context)

@login_required
@permission_required('add_event', raise_exception=True)
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            after_url = reverse('events:show_event', args=(event.pk,))
            return HttpResponseRedirect(after_url)
    elif request.method == 'GET':
        now = timezone.now()
        event = Event(announcement_date=now)
        form = EventForm(instance=event)

    context = {'form': form}
    return render(request, 'events/create_event.html', context)

@login_required
@permission_required('change_event', raise_exception=True)
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            after_url = reverse('events:show_event', args=(event.pk,))
            return HttpResponseRedirect(after_url)
    elif request.method == 'GET':
        form = EventForm(instance=event)

    context = {'form': form, 'event': event, 'edit': True}
    return render(request, 'events/create_event.html', context)

def show_event(request, event_id):
    # If the user has the view_event permission, show events
    # regardless of their announcement date.
    now = timezone.now()
    if request.user.has_perm('events.view_event'):
        event = get_object_or_404(Event, pk=event_id)
    else:
        event = get_object_or_404(Event, pk=event_id,
                                  announcement_date__lte=now)

    if event.ending_date > now and event.max_attendees > event.attendee_set.count():
        attendable = 'yes'
    elif now > event.ending_date:
        attendable = 'over'
    elif event.attendee_set.count() >= event.max_attendees:
        attendable = 'book'

    event_url = reverse('events:show_event', args=(event.pk,))
    full_url = request.build_absolute_uri(event_url)

    context = {'event': event, 'attendable': attendable,
               'full_url': full_url}
    return render(request, 'events/show_event.html', context)

def attend_event(request, event_id):
    # Only allow attending events that are on or past the announcement
    # time.
    now = timezone.now()
    event = get_object_or_404(Event, pk=event_id)
    context = {'event': event}

    if now >= event.ending_date:
        context['error'] = 'done'
    elif event.announcement_date > now.date():
        context['error'] = 'unavailable'
    elif event.attendee_set.count() == event.max_attendees:
        context['error'] = 'booked'
    else:
        if request.method == 'POST':
            while True:
                random_slug = "".join([random.choice(string.digits+string.ascii_letters) for i in xrange(6)])
                try:
                    previous_attendee = Attendee.objects.get(slug=random_slug)
                except ObjectDoesNotExist:
                    break
            attendee = Attendee(event=event, slug=random_slug)
            form = AttendeeForm(request.POST, instance=attendee)
            if form.is_valid():
                new_attendee = form.save()
                after_url = reverse('events:show_attendee',
                                    args=(event.pk, random_slug))
                full_url = request.build_absolute_uri(after_url)
                mail.send([new_attendee.email], settings.EVENT_FROM_EMAIL,
                          template='add_attendee',
                          context={'event': event, 'attendee': new_attendee, 'full_url': full_url})
                return HttpResponseRedirect(after_url)     
                
            else:
                context['form'] = form
        elif request.method == 'GET':
            form = AttendeeForm()
            context['form'] = form

    return render(request, 'events/attend_event.html', context)

def show_attendee(request, event_id, attendee_slug):
    event = get_object_or_404(Event, pk=event_id)
    # Don't make it possible to manipulate urls by putting an
    # attendee slug under a different event. Just a needless, but
    # fancy hack. :p
    attendee = get_object_or_404(Attendee, event=event,
                                   slug=attendee_slug)
    now = timezone.now()

    # Don't show the edit button if we are already past the starting
    # date.
    if now > event.starting_date:
        editable = False
    else:
        editable = True
    context = {'attendee': attendee, 'editable': editable}

    return render(request, 'events/show_attendee.html', context)

def control_attendee(request, event_id, attendee_slug):
    # TODO: indicate on the page whether or not the activity is right.

    event = get_object_or_404(Event, pk=event_id)
    attendee = get_object_or_404(Attendee, event=event,
                                   slug=attendee_slug)
    now = timezone.now()
    context = {'attendee': attendee, 'event': event, 'edit': True}
    form = AttendeeForm(instance=attendee)
    if now > event.starting_date:
        context['error'] = 'done'
    else:
        if request.method == 'POST':
            # Cancellation form/button
            if 'action' in request.POST and request.POST['action'] == 'cancel':
                attendee.is_counted = False
                attendee.save()
                after_url = reverse('events:show_event',
                                    args=(event.pk,))
                event_full_url = request.build_absolute_uri(after_url)
                mail.send([attendee.email], settings.EVENT_FROM_EMAIL,
                          template='cancel_attendee',
                          context={'event': event, 'attendee': attendee, 'event_full_url': event_full_url})

                return HttpResponseRedirect(after_url)
            else: # Normal editing
                form = AttendeeForm(request.POST, instance=attendee)
                if form.is_valid():
                    form.save()
                    after_url = reverse('events:show_attendee',
                                    args=(event.pk, attendee.slug))
                    return HttpResponseRedirect(after_url)

    context['form'] = form
    return render(request, 'events/attend_event.html', context)
