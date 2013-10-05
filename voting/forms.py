#-*- coding: utf-8 -*-

from django import forms
from models import *

class AnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question_id = kwargs.pop('question_id')

        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['answer'].choices = [(answer.id, answer.title)
            for answer in Answer.objects.filter(question_id=question_id)]

class SingleAnswerForm(AnswerForm):
    answer = forms.ChoiceField(label=u'Варианты ответов',
        widget=forms.RadioSelect, required=False)

class MultipleAnswerForm(AnswerForm):
    answer = forms.MultipleChoiceField(label=u'Варианты ответов',
        widget=forms.CheckboxSelectMultiple(), required=False)

QUESTION_FORMS = {
    QUESTION_SA: SingleAnswerForm,
    QUESTION_MA: MultipleAnswerForm,
}
