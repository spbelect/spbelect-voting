# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

#from django.conf import settings

QUESTION_SA = 1 #with single answer
QUESTION_MA = 2 #with multiplie answer

class QuestionType(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=u'ID')
    name = models.TextField(verbose_name=u'название')
    info = models.TextField(null=True, blank=True, verbose_name=u'комментарий')

    def __unicode__(self):
        return u'%s (%d)' % (self.name, self.id)

    def questions_number(self):
        return self.questions.filter(type=self).count()

    questions_number.short_description = u'количество вопросов'

    class Meta:
        ordering = ['id']
        db_table = 'voting_question_type'
        verbose_name = u'тип вопроса'
        verbose_name_plural = u'типы вопросов'

class Question(models.Model):
    type = models.ForeignKey(QuestionType, db_column='type_id',
        verbose_name=u'тип', related_name='questions',
        default=QUESTION_SA)
    title = models.TextField(verbose_name=u'заголовок')
    text = models.TextField(verbose_name=u'текст')
    max_replies_number = models.SmallIntegerField(verbose_name=u'максимальное количество ответов', null=True, blank=True)

    def __unicode__(self):
        return u'%s (%d)' % (self.title, self.id)

    class Meta:
        ordering = ['id']
        verbose_name = u'вопрос'
        verbose_name_plural = u'вопросы'

class Answer(models.Model):
    question = models.ForeignKey(Question, db_column='question_id',
        verbose_name=u'вопрос', related_name='answers')
    photo = models.ImageField(upload_to='photo', height_field='height', width_field='width', verbose_name=u'фото', null=True, blank=True)
    title = models.TextField(verbose_name=u'заголовок')
    text = models.TextField(verbose_name=u'текст', null=True, blank=True)
    height = models.SmallIntegerField(verbose_name=u'высота', null=True, blank=True)
    width = models.SmallIntegerField(verbose_name=u'ширина', null=True, blank=True)

    def __unicode__(self):
        return u'%s (%d)' % (self.title[0:32], self.id)

    class Meta:
        ordering = ['id']
        verbose_name = u'ответ'
        verbose_name_plural = u'ответы'

class UserReply(models.Model):
    key = models.TextField(primary_key=True)
    user = models.ForeignKey(User, related_name='user_replies', db_column='user_id')
    question = models.ForeignKey(Question, related_name='user_replies', db_column='question_id')

    class Meta:
        db_table = 'voting_user_reply'

class Reply(models.Model):
    key = models.TextField(primary_key=True)
    question = models.ForeignKey(Question, db_column='question_id')
    id_key = models.TextField()

class ReplyData(models.Model):
    key = models.TextField(primary_key=True)
    reply = models.ForeignKey(Reply, related_name='reply_data', db_column='reply_key')
    answer = models.ForeignKey(Answer, related_name='reply_data', db_column='answer_id', null=True)

    class Meta:
        db_table = 'voting_reply_data'
