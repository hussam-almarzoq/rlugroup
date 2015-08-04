This is a collection Django-based apps that run the website of Riyadh
Linux User Group (RLUG).  This website, in Arabic, is used for
managing events and registering attendees.  In addition, contacts and
sponsoring offers are received through the website.

# Dependencies and Settings

The RLUG website was tested using Django 1.6.5 and Python 2.7.5.
Additionally, it utilized the following freely-licensed Django apps:

* `django-post_office`
* `django-datetime-widget`
* `django-bootstrap3`

RLUG-required variables in `settings.py` (other than the variables
required by DJANGO itself and the dependencies mentioned above):

* `DEFAULT_FROM_EMAIL` = 'info@riyadhlug.org'  # The email address used for everything other than event notifications (currently: only contact emails.)
* `CONTACT_EMAIL_RECIPIENTS` = _['EMAIL_ADDRESS']- # A list of addresses that need to receive the incoming contact emails.
* `CONTACT_SUBJECT_INTRO` = '[RLUGroup] ' # The prefix used in the contact message subjects
* `EVENT_FROM_EMAIL` = _EMAIL_ADDRESS_ # The email address used for sending event notifications (currently: only contact emails.)

RLUG-required URLS in the project's `url.py` are:

    # [...]
    from django.views.generic import TemplateView
    # [...]
    urlpatterns = patterns('',
                       url(r'^$', 'core.views.home', name='home'),
                       url(r'^events/', include('events.urls', namespace='events')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^contact/$', 'core.views.contact', name='contact'),
                       url(r'^charter/$', TemplateView.as_view(template_name='charter.html'), name='charter'),
                       url(r'^sponsor/$', 'core.views.sponsor', name='sponsor'),
                       url(r'^speak/$', 'core.views.speak', name='speak'),
                       url(r'^contact/thanks/$', TemplateView.as_view(template_name='thanks.html'), name='thanks'),
                       url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    )

Additionally, we have a daily scheduled script that automatically
sends reminders two days in advance of events, `send_reminders.py`.
The cronjob we use is:

    0 0 * * * send_reminders.py  >> send_reminders.log 2>&1

# Licensing

Copyright (C) 2014 Osama Khalid.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Affero General Public License for more details.

Additionally, the templates are licensed under both the AGPLv3+ and
Creative Commons Attribution-ShareAlike 4.0 International.  You can
choose whatever best suits your purposes.
