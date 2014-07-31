from django.conf.urls import patterns, url
from events import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^create/$', views.create_event, name='create_event'),
    url(r'^(?P<event_id>\d+)/$', views.show_event, name='show_event'),
    url(r'^(?P<event_id>\d+)/edit/$', views.edit_event, name='edit_event'),
    url(r'^(?P<event_id>\d+)/attend/$', views.attend_event, name='attend'),
    url(r'^(?P<event_id>\d+)/attend/(?P<attendee_slug>[\d\w]{6})/$', views.show_attendee, name='show_attendee'),
    url(r'^(?P<event_id>\d+)/attend/(?P<attendee_slug>[\d\w]{6})/control/$', views.control_attendee, name='control_attendee'),
)
