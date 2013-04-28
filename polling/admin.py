# -*- coding: utf-8 -*-

from polling.models import Question, Answer
from django.contrib import admin

class AnswerInline(admin.TabularInline):
    model = Answer
    fk_name = 'question'
    readonly_fields = ('height', 'width')

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)