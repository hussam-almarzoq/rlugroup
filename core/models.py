# -*- coding: utf-8  -*-
from django.db import models

class FeaturedMedia(models.Model):
    event_name = models.CharField(max_length=60,
                                  verbose_name=u"اسم اسم النشاط",
                                  help_text=u"مثلا: يوم الأمان الرقمي")
    header = models.CharField(max_length=60, verbose_name=u"العنوان",
                              help_text=u"مثلا: منذر طه يتحدث عن الهندسة الاجتماعية")
    description = models.CharField(max_length=140, verbose_name=u"",
                                   help_text=u"مثلا: المهندس طه منذر يتحدث في نشاط مجموعة...")
    embed_code = models.TextField(u'كود التضمين', help_text=u"أضف class=\"embed-responsive-item\"")
