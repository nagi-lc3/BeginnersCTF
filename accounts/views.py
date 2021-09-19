from BeginnersCTF.accounts.forms import UsernameChangeForm
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib import messages


class MyPageView(TemplateView):
    template_name = 'accounts/my_page.html'


my_page = MyPageView.as_view()


class UsernameChangeView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        form = UsernameChangeForm()
        context["form"] = form
        return render(request, 'accounts/change_username.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = UsernameChangeForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            user_obj = User.objects.get(username=request.user.username)
            user_obj.username = username
            user_obj.save()
            messages.info(request, "usernameを変更しました。")

            return redirect('profiles:profile')
        else:
            context["form"] = form

            return render(request, 'accounts/change_username.html', context)
