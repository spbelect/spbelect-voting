#-*- coding: utf-8 -*-

from django import forms
from models import *

class AnswerForm(forms.Form):
    answers = forms.MultipleChoiceField(label=u'Варианты ответов',
        widget=forms.CheckboxSelectMultiple(), required=False)

    def __init__(self, *args, **kwargs):
        question_id = kwargs.pop('question_id')

        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['answers'].choices = [(answer.id, answer.title)
            for answer in Answer.objects.filter(question_id=question_id)]