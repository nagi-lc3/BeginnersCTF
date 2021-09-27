from django.core.mail import EmailMessage
from django.forms import ImageField

from .models import Problem, Inquiry
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class ProblemDetailForm(forms.ModelForm):
    """問題詳細フォーム"""

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
    """お問い合わせフォーム"""

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
            field.widget.attrs['class'] = 'form-control'

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


class MyPageForm(forms.ModelForm):
    """マイページフォーム"""
    username = forms.CharField(label='ユーザ名', max_length=30)

    class Meta:
        model = User
        fields = ('icon', 'username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = "form-control"


class AccountDeleteForm(forms.ModelForm):
    """アカウント削除フォーム"""

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs = {'placeholder': 'メールアドレス', }
        for field in self.fields.values():
            field.widget.attrs['class'] = "form-control"
