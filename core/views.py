# -*- coding: utf-8  -*-
import random

from django import forms
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render
from django.core.urlresolvers import reverse

from post_office import mail

from core.models import FeaturedMedia

category_choices = (
    ('distribution', u'توزيعات غنو/لينكس'),
    ('development', u'البرمجة والتطوير'),
    ('culture', u'الثقافة الحرة'),
    ('privacy', u'الأمان الرقمي والخصوصية'),
    ('society', u'مجتمع البرمجيات الحرة'),
    ('concepts', u'مفاهيم البرمجيات الحرة'),
    ('story', u'تجربة مع البرمجيات الحرة'),
    ('other', u'أخرى'),
)

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

class SpeakForm(forms.Form):
    name = forms.CharField(label=u"الاسم", max_length=70)
    email = forms.EmailField(label=u"البريد")
    category = forms.CharField(label=u"المجال",
                               max_length=15,
                               widget=forms.Select(choices=category_choices))
    message = forms.CharField(label=u"نبذة قصيرة عن الكلمة", max_length=1000,
                              widget=forms.Textarea())


def home(request):
    count = FeaturedMedia.objects.count()
    random_pk = random.randint(1, count)
    print random_pk
    featured_media = FeaturedMedia.objects.get(pk=random_pk)

    context = {'featured_media': featured_media}
    return render(request, 'home.html', context)

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

def speak(request):
    if request.method == 'POST':
        form = SpeakForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            category = form.cleaned_data['category']
            category_dict = dict(category_choices)
            full_category = category_dict[category]
            summery = form.cleaned_data['message']
            now = timezone.now()
            mail.send(settings.CONTACT_EMAIL_RECIPIENTS,
                      template='speak_email',
                      context={'name': name,
                               'email': email, 'summery':
                               summery, 'category': full_category,
                               'now': now},
                      headers={'Reply-to': email},)
            return HttpResponseRedirect(reverse('thanks'))
    elif request.method == 'GET':
        form = SpeakForm()

    context = {'form': form}
    return render(request, 'speak.html', context)
