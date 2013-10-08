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
from django.conf import settings

from models import *
from forms import AnswerForm, QUESTION_FORMS

@login_required()
def index(request):
    return redirect('/question-list')
    #return TemplateResponse(request, 'index.html', locals())

@login_required()
def question_list(request):
    title = u'Вопросы для голосования'

    active_questions = Question.objects.exclude(user_replies__user=request.user).distinct('id')
    not_active_questions = Question.objects.filter(user_replies__user=request.user).distinct('id')

    return TemplateResponse(request, 'question_list.html', locals())

@login_required()
def question(request, id=None):
    if UserReply.objects.filter(user=request.user, question_id=id).exists():
        return redirect('voting.views.question_list')

    question = Question.objects.get(id=id)
    answers = question.answers.order_by('title').all()

    title = question.title

    return TemplateResponse(request, 'question.html', locals())

@login_required()
@transaction.commit_on_success
def answer(request, id=None):
    if request.method != 'POST':
        return redirect('voting.views.question_list')

    if UserReply.objects.filter(user=request.user, question_id=id).exists():
        return redirect('voting.views.question_list')

    question = Question.objects.get(id=id)

    form = QUESTION_FORMS[question.type_id](request.POST, question_id=id)

    key = request.COOKIES.get('key', None)

    if form.is_valid():
        ur_key = hashlib.sha1(str(datetime.datetime.now()) + str(request.user.id) + str(random.random())).hexdigest()
        UserReply.objects.create(key=ur_key, user=request.user, question_id=id)

        if not key:
            key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(6))

        reply = Reply.objects.create(
            key=hashlib.sha1(str(datetime.datetime.now()) + str(id) + key).hexdigest(),
            question_id=id,
            id_key=key
        )

        if question.type_id == QUESTION_SA:
            ReplyData.objects.create(
                key=hashlib.sha1(str(datetime.datetime.now()) + key).hexdigest(),
                reply=reply,
                answer_id=form.cleaned_data['answer']
            )
        elif question.type_id == QUESTION_MA:
            for answer_id in form.cleaned_data['answer']:
                ReplyData.objects.create(
                    key=hashlib.sha1(str(datetime.datetime.now()) + key).hexdigest(),
                    reply=reply,
                    answer_id=answer_id
                )

        success = True
    else:
        success = False

    response  = TemplateResponse(request, 'answer.html', locals())

    if key:
        response.set_cookie('key', key, expires=datetime.datetime.now() + datetime.timedelta(days=3),
            httponly=True, secure=settings.SESSION_COOKIE_SECURE)

    return response

@login_required()
def voters(request):
    title = u'Список проголосовавших'
    voters = User.objects.filter(user_replies__isnull=False).distinct().order_by('first_name', 'last_name')
    not_voting = User.objects.filter(user_replies__isnull=True).distinct().order_by('first_name', 'last_name')

    members = User.objects.count()

    presence = float(len(voters))/members * 100

    return TemplateResponse(request, 'voters.html', locals())

@login_required()
def replies(request, id=None):
    title = u'Итоги голосования'

    questions = Question.objects.all()

    question = Question.objects.get(id=id)

    answers = Answer.objects.filter(question_id=id).order_by('title').annotate(replies=Count('reply_data'))

    ordered_answers = Answer.objects.filter(question_id=id).annotate(replies=Count('reply_data')).order_by('-replies')

    replies = Reply.objects.filter(question_id=id).prefetch_related('reply_data').order_by('key')

    return TemplateResponse(request, 'replies.html', locals())
