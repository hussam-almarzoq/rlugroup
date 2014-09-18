# -*- coding: utf-8  -*-
from datetime import datetime
from django.contrib import admin

from events.models import Event, Attendee, Organizer
#from post_office.models import EmailTemplate


class AttendeeInline(admin.StackedInline):
    model = Attendee
    extra = 1

class TimeFilter(admin.SimpleListFilter):
    title = u"الوقت"
    parameter_name = 'time'
    def lookups(self, request, model_admin):
        return (
                ('p', u'نشاطات انقضت'), # past
                ('f', u'نشاطات مقبلة'), # future
            )
    def queryset(self, request, queryset):
        now = datetime.now()
        if self.value() == 'p':
            return queryset.filter(starting_date__lte=now)
        elif self.value() == 'f':
            return queryset.filter(starting_date__gte=now)

class AttendeeTimeFilter(admin.SimpleListFilter):
    title = u"الوقت"
    parameter_name = 'time'
    def lookups(self, request, model_admin):
        return (
                ('p', u'نشاطات انقضت'), # past
                ('f', u'نشاطات مقبلة'), # future
            )
    def queryset(self, request, queryset):
        now = datetime.now()
        if self.value() == 'p':
            return queryset.filter(event__starting_date__lte=now)
        elif self.value() == 'f':
            return queryset.filter(event__starting_date__gte=now)

class GenderFilter(admin.SimpleListFilter):
    title = u"الجنس"
    parameter_name = 'gender'

    def lookups(self, request, model_admin):
        return (
                ('m', u'رجال'),
                ('f', u'نساء'),
            )
    def queryset(self, request, queryset):
        if self.value() == 'm':
            return queryset.filter(gender='M')
        elif self.value() == 'f':
            return queryset.filter(gender='F')

class PublishedFilter(admin.SimpleListFilter):
    title = u"النشر"
    parameter_name = 'published'

    def lookups(self, request, model_admin):
        return (
                ('y', u'نشاطات منشورة'), # past
                ('n', u'نشاطات لم تنشر بعد'), # future
            )
    def queryset(self, request, queryset):
        now = datetime.now()
        if self.value() == 'y':
            return queryset.filter(announcement_date__lte=now)
        elif self.value() == 'n':
            return queryset.filter(announcement_date__gte=now)


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'submitter', 'starting_date', 'ending_date', 'announcement_date')
    list_filter = [TimeFilter, PublishedFilter]
    inlines = [AttendeeInline]

class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'event', 'gender', 'is_counted', 'submission_date')
    list_filter = [GenderFilter, AttendeeTimeFilter]

admin.site.register(Event, EventAdmin)
admin.site.register(Attendee, AttendeeAdmin)
