#-*- coding: utf-8 -*-

from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from forms import ChangePasswordForm
from forms import LoginForm

#@failed_login_rate()
@user_passes_test(lambda user: not user.is_authenticated(), '/account/logout')
def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login_data = login_form.cleaned_data
            user = auth.authenticate(username = login_data['username'],
                password = login_data['password'])
            if user is not None and user.is_active:
                auth.login(request, user)
                if login_data['next']:
                    return redirect(login_data['next'])
                else:
                    return redirect('/')

        error_message = u'Пожалуйста, введите верные имя пользователя ' \
            u'и пароль. Помните, оба поля чувствительны к регистру.'
    else:
        login_form = LoginForm(request.GET)

    title = 'Вход в систему'
    page_title = title

    return TemplateResponse(request, 'login.html', locals())

@login_required
def logout(request):
    auth.logout(request)

    return redirect('account.views.login')

@login_required
def change_password(request):
    if request.method == 'POST':
        change_password_form = ChangePasswordForm(request.POST)
        if change_password_form.is_valid():
            password_data = change_password_form.cleaned_data
            if request.user.check_password(password_data['old_password']):
                request.user.set_password(password_data['password1'])
                request.user.save()
            else:
                errors = u'Введённый старый пароль неверен'
    else:
        change_password_form = ChangePasswordForm()

    title = u'Изменение пароля %s' % request.user.get_full_name()
    page_title = title

    return TemplateResponse(request, 'change_password.html', locals())
