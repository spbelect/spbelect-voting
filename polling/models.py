# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

#from django.conf import settings

class Question(models.Model):
    title = models.TextField(verbose_name=u'заголовок')
    text = models.TextField(verbose_name=u'текст')

    class Meta:
        ordering = ['id']
        verbose_name = u'вопрос'
        verbose_name_plural = u'вопросы'

class Answer(models.Model):
    question = models.ForeignKey(Question, db_column='question_id',
        verbose_name=u'вопрос', related_name='answers')
    photo = models.ImageField(upload_to='photo', height_field='height', width_field='width', verbose_name=u'фото', null=True, blank=True)
    title = models.TextField(verbose_name=u'заголовок')
    text = models.TextField(verbose_name=u'текст')
    height = models.SmallIntegerField(verbose_name=u'высота', null=True, blank=True)
    width = models.SmallIntegerField(verbose_name=u'ширина', null=True, blank=True)

    def __unicode__(self):
        return self.title[0:32]

    class Meta:
        ordering = ['id']
        verbose_name = u'ответ'
        verbose_name_plural = u'ответы'

class UserReply(models.Model):
    user = models.ForeignKey(User, related_name='user_replies', db_column='user_id')
    question = models.ForeignKey(Question, related_name='user_replies', db_column='question_id')

    class Meta:
        db_table = 'polling_user_reply'

class Reply(models.Model):
    key = models.TextField(primary_key=True)
    question = models.ForeignKey(Question, db_column='question_id')

class ReplyData(models.Model):
    key = models.TextField(primary_key=True)
    reply = models.ForeignKey(Reply, db_column='reply_key')
    answer = models.ForeignKey(Answer, db_column='answer_id', null=True)

    class Meta:
        db_table = 'polling_reply_data'
