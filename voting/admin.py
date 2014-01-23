# -*- coding: utf-8 -*-

from voting.models import QuestionType, Question, Answer
from django.contrib import admin


class QuestionTypeAdmin(admin.ModelAdmin):
    model = QuestionType

admin.site.register(QuestionType, QuestionTypeAdmin)


class AnswerInline(admin.TabularInline):
    model = Answer
    fk_name = 'question'
    readonly_fields = ('height', 'width')


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)
