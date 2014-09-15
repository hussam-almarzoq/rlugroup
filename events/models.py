# -*- coding: utf-8  -*-
from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"الاسم")
    submitter = models.ForeignKey(User, null=True,
                                  on_delete=models.SET_NULL,
                                  verbose_name=u"المرسل")
    location = models.CharField(max_length=50, verbose_name=u"المكان", blank=True, help_text=u"اسم القاعة مثلا.")
    location_description = models.TextField(verbose_name=u"تفاصيل المكان", help_text=u'الوصف مثلا', blank=True)
    long_position   = models.DecimalField (max_digits=10, decimal_places=5, verbose_name=u"خط الطول")
    lat_position   = models.DecimalField (max_digits=10, decimal_places=5, verbose_name=u"خط العرض")
    short_description = models.TextField(u'الوصف القصير', help_text=u"سيستخدم في الصفحة الرئيسية للأنشطة (يمكن استخدام HTML")
    description = models.TextField(u'الوصف', help_text=u"الوصف الكامل (يمكن استخدام HTML)")
    starting_date = models.DateTimeField(u'تاريخ ووقت بدء الحدث')
    ending_date =  models.DateTimeField(u'تاريخ ووقت انتهاء')
    announcement_date =  models.DateField(u'تاريخ الإعلان', help_text=u"متى تريد أن يظهر هذا النشاط للزوار؟")
    max_attendees = models.PositiveSmallIntegerField(verbose_name=u"العدد الأقصى للحضور", help_text=u"كم عدد التذاكر التي سيسمح بحجزها؟")
    submission_date = models.DateTimeField(u'تاريخ الإرسال',
                                           auto_now_add=True)
    available_to_choices = (
        ('A', u'الجميع'),
        ('F', u'النساء'),
        ('M', u'الرجال'),
        )
    available_to = models.CharField(max_length=1,
                                    verbose_name=u"متاح لـ",
                                    choices=available_to_choices)
    edit_date = models.DateTimeField(u'تاريخ التعديل', auto_now=True)

    def __unicode__(self):
        return self.name
    
class Attendee(models.Model):
    event = models.ForeignKey(Event, null=True,
                              on_delete=models.SET_NULL,
                              verbose_name=u"الحدث")
    name = models.CharField(max_length=100, verbose_name=u"الاسم")
    email = models.EmailField(u'البريد')
    gender_choices = (
        ('M', u'ذكر'),
        ('F', u'أنثى'),
        )
    gender = models.CharField(max_length=1, verbose_name=u"الجنس", choices=gender_choices)
    add_to_mailing_list = models.BooleanField(verbose_name=u"هل تريد أن تضاف إلى القائمة البريدية؟",
                                              default=True)
    referral_choices = (
        ('T', u'قرأت عنه في تويتر'), # Twitter
        ('F', u'قرأت عنه في فيسبوك'),  # Facebook
        ('P', u'شاهدت إعلانا معلقا'), # Poster
        ('M', u'أخبرني عنه صديق'), # Word-of-mouth
        ('W', u'موقع المجموعة'), # Our website
        )
    referral = models.CharField(max_length=1, verbose_name=u"كيف عرفت عن الحدث؟", choices=referral_choices)
    slug = models.CharField(max_length=6, verbose_name=u"رابط")
    submission_date = models.DateTimeField(u'تاريخ الإرسال',
                                           auto_now_add=True)
    edit_date = models.DateTimeField(u'تاريخ التعديل', auto_now=True)
    is_counted_choices = (
        (False, 'ملغى'),
        (True, 'محسوب'),
        )
    is_counted = models.BooleanField(verbose_name=u"محسوب",
                                     default=True,
                                     choices=is_counted_choices)

    def get_gender(self):
        gender_dict = dict(self.gender_choices)
        return gender_dict[self.gender]

    def get_referral(self):
        referral_dict = dict(self.referral_choices)
        return referral_dict[self.referral]

    def __unicode__(self):
        return u"%s: %s" % (self.event.name, self.slug)

class Organizer(models.Model):
    event = models.ForeignKey(Event, null=True,
                              on_delete=models.SET_NULL,
                              verbose_name=u"الحدث")
    name = models.CharField(max_length=100, verbose_name=u"الاسم")
    email = models.EmailField(u'البريد')
    gender_choices = (
        ('M', u'ذكر'),
        ('F', u'أنثى'),
        )
    gender = models.CharField(max_length=1, choices=gender_choices,
                              verbose_name=u"الجنس")
    add_to_mailing_list = models.BooleanField(verbose_name=u"هل تريد أن تضاف إلى القائمة البريدية؟",
                                              default=True)
    submission_date = models.DateTimeField(u'تاريخ الإرسال',
                                           auto_now_add=True)
    edit_date = models.DateTimeField(u'تاريخ التعديل', auto_now=True)
    status_choices = (
        (None, 'لم يراجع بعد'),
        (False, 'مرفوض'),
        (True, 'مقبول'),
        )
    status = models.NullBooleanField(verbose_name=u"الحالة",
                                     default=None,
                                     choices=status_choices)
