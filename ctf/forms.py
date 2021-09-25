import re

from django.core.mail import EmailMessage

from .models import Problem, Inquiry
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField


class ProblemDetailForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ('answer',)
        labels = {
            'name': '名前',
            'email': 'メールアドレス',
            'subject': '件名',
            'contents': '内容',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['answer'].widget.attrs = {'placeholder': 'ctf{sample_answer}',
                                              'class': 'form-control'}


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ('name', 'email', 'subject', 'contents')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'placeholder': 'お名前を入力してください。', }
        self.fields['email'].widget.attrs = {'placeholder': 'メールアドレスを入力してください。'}
        self.fields['subject'].widget.attrs = {'placeholder': '件名を入力してください。'}
        self.fields['contents'].widget.attrs = {'placeholder': 'お問い合わせ内容を入力してください。',
                                                'rows': 10}
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control mb-3'

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        subject = self.cleaned_data['subject']
        contents = self.cleaned_data['contents']

        message = '送信者名: {0}\nメールアドレス: {1}\n内容:\n{2}'.format(name, email, contents)
        from_email = 'beginnersctf@gmail.com'
        to_list = [
            'yoshida.mitsuki1203@gmail.com'
        ]

        message = EmailMessage(subject=subject, body=message, from_email=from_email, to=to_list)
        message.send()


class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username',)
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = "form-control"
            field.widget.attrs['placeholder'] = "150 characters or fewer. Letters, digits and @/./+/-/_ only."
