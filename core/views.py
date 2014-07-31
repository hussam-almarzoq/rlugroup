# -*- coding: utf-8  -*-
from django import forms
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render
from django.core.urlresolvers import reverse

from post_office import mail

class ContactForm(forms.Form):
    name = forms.CharField(label=u"الاسم", max_length=70)
    email = forms.EmailField(label=u"البريد")
    subject = forms.CharField(label=u"الموضوع", max_length=127)
    message = forms.CharField(label=u"الرسالة", max_length=1000,
                              widget=forms.Textarea())

class SponsorForm(forms.Form):
    name = forms.CharField(label=u"الاسم", max_length=70)
    email = forms.EmailField(label=u"البريد")
    message = forms.CharField(label=u"مجال الدعم", max_length=1000,
                              widget=forms.Textarea())

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            now = timezone.now()
            mail.send(settings.CONTACT_EMAIL_RECIPIENTS,
                      template='contact_email',
                      context={'name': name,
                               'email': email, 'subject': subject, 'message':
                               message, 'now': now, 'intro':
                               settings.CONTACT_SUBJECT_INTRO},
                      headers={'Reply-to': email},)
            return HttpResponseRedirect(reverse('thanks'))
    elif request.method == 'GET':
        form = ContactForm()

    context = {'form': form}
    return render(request, 'contact.html', context)

def sponsor(request):
    if request.method == 'POST':
        form = SponsorForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            now = timezone.now()
            mail.send(settings.CONTACT_EMAIL_RECIPIENTS,
                      template='sponsor_email',
                      context={'name': name,
                               'email': email, 'message':
                               message, 'now': now},
                      headers={'Reply-to': email},)
            return HttpResponseRedirect(reverse('thanks'))
    elif request.method == 'GET':
        form = SponsorForm()

    context = {'form': form}
    return render(request, 'sponsor.html', context)
