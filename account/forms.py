#-*- coding: utf-8 -*-

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label=u'Логин')
    password = forms.CharField(label=u'Пароль',
                               widget=forms.PasswordInput)
    next = forms.CharField(required=False, widget=forms.HiddenInput)


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label=u'Старый пароль',
                                   widget=forms.PasswordInput)
    password1 = forms.CharField(label=u'Новый пароль', min_length=6,
                                max_length=32, widget=forms.PasswordInput)
    password2 = forms.CharField(label=u'Повтор пароля', min_length=6,
                                max_length=32, widget=forms.PasswordInput)

    def clean_password1(self):
        import re
        if not re.match('^[A-Za-z0-9_-]+$', self.cleaned_data['password1']):
            raise forms.ValidationError(u'Неверные символы в пароле.')

        return self.cleaned_data['password1']

    def clean(self):
        if self.cleaned_data.get('password1') != \
           self.cleaned_data.get('password2'):
            raise forms.ValidationError(u'Введённые пароли не совпадают.')

        return self.cleaned_data
