#-*- coding: utf-8 -*-

from django import forms
from models import *


class AnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question_id = kwargs.pop('question_id')
        self.question_id = question_id

        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['answer'].choices = [(answer.id, answer.title)
                                         for answer in Answer.objects
                                         .filter(question_id=question_id)]


class SingleAnswerForm(AnswerForm):
    answer = forms.ChoiceField(label=u'Варианты ответов',
                               widget=forms.RadioSelect, required=False)


class MultipleAnswerForm(AnswerForm):
    answer = forms.MultipleChoiceField(label=u'Варианты ответов',
                                       widget=forms.CheckboxSelectMultiple(),
                                       required=False)

    def clean(self):
        cleaned_data = super(MultipleAnswerForm, self).clean()

        question = Question.objects.get(id=self.question_id)
        if question.type_id == QUESTION_MA:
            if question.max_replies_number:
                max_replies_number = question.max_replies_number
            else:
                max_replies_number = question.answers.count()

            if len(cleaned_data.get('answer')) > max_replies_number:
                raise forms.ValidationError('Invalid replies number')

        return cleaned_data

QUESTION_FORMS = {
    QUESTION_SA: SingleAnswerForm,
    QUESTION_MA: MultipleAnswerForm,
}
