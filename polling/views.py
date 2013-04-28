# -*- coding: utf-8 -*-

import random
import string
import hashlib
import datetime

from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.template.response import TemplateResponse
from django.db import transaction
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db.models import Count

from models import *
from forms import AnswerForm

def index(request):
    return TemplateResponse(request, 'index.html', locals())

@login_required()
def question_list(request):
    title = u'Вопросы для голосования'

    active_questions = Question.objects.exclude(user_replies__user=request.user).distinct('id')
    not_active_questions = Question.objects.filter(user_replies__user=request.user).distinct('id')

    return TemplateResponse(request, 'question_list.html', locals())

@login_required()
def question(request, id=None):
    if UserReply.objects.filter(user=request.user, question_id=id).exists():
        return redirect('polling.views.question_list')

    question = Question.objects.get(id=id)
    answers = question.answers.order_by('title').all()

    title = question.title

    return TemplateResponse(request, 'question.html', locals())

@login_required()
@transaction.commit_on_success
def answer(request, id=None):
    if request.method != 'POST':
        return redirect('polling.views.question_list')

    if UserReply.objects.filter(user=request.user, question_id=id).exists():
        return redirect('polling.views.question_list')

    form = AnswerForm(request.POST, question_id=id)

    if form.is_valid() and len(form.cleaned_data['answers']) <= 7:
        UserReply.objects.create(user=request.user, question_id=id)

        key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(6))
        reply = Reply.objects.create(key=key, question_id=id)

        for answer_id in form.cleaned_data['answers']:
            rd_key = hashlib.sha1(str(datetime.datetime.now()) + key).hexdigest()
            ReplyData.objects.create(
                key=rd_key,
                reply=reply,
                answer_id=answer_id
            )

        success = True
    else:
        success = False

    return TemplateResponse(request, 'answer.html', locals())

@login_required()
def voters(request):
    title = u'Список проголосовавших'
    voters = User.objects.filter(user_replies__isnull=False).order_by('first_name', 'last_name')

    members = User.objects.count()

    presence = float(len(voters))/members * 100

    return TemplateResponse(request, 'voters.html', locals())

@login_required()
def replies(request):
    title = u'Итоги голосования за кандидатов в совет Наблюдателей Петербурга'
    answers = Answer.objects.order_by('title').annotate(replies=Count('reply_data'))

    ordered_answers = Answer.objects.annotate(replies=Count('reply_data')).order_by('-replies')

    replies = Reply.objects.prefetch_related('reply_data').order_by('key')

    return TemplateResponse(request, 'replies.html', locals())
