from .models import Problem
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField


class ProblemDetailForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ('answer',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['answer'].widget.attrs = {'placeholder': '答え'}

    def clean_answer(self):
        answer = self.cleaned_data['answer']
        if len(answer) < 5:
            raise forms.ValidationError('%(min_length)s文字以上で入力してください', code='invalid', params={'min_length': 5})
        return answer


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
