from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy, reverse

from .forms import UsernameChangeForm, ProblemDetailForm
from .models import Information, Problem, UserProblem
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


class IndexView(TemplateView):
    template_name = 'ctf/index.html'


index = IndexView.as_view()


class InformationListView(ListView):
    model = Information
    template_name = 'ctf/information.html'

    def get_queryset(self):
        return Information.objects.order_by('-created_at')


information = InformationListView.as_view()


class RankingView(LoginRequiredMixin, TemplateView):
    template_name = 'ctf/ranking.html'


ranking = RankingView.as_view()


class ProblemListView(LoginRequiredMixin, ListView):
    model = UserProblem
    template_name = 'ctf/problem_list.html'

    def get_queryset(self):
        return UserProblem.objects.all().select_related('problem').filter(
            custom_user_id=self.request.user.id, ).order_by('problem_id__level')


problem_list = ProblemListView.as_view()


class BoardView(LoginRequiredMixin, TemplateView):
    template_name = 'ctf/board.html'


board = BoardView.as_view()


class InquiryView(TemplateView):
    template_name = 'ctf/inquiry.html'


inquiry = InquiryView.as_view()


class MyPageView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        queryset = get_user_model().objects.get(id=request.user.id)
        initial_data = {
            'username': queryset.username
        }
        context = {}
        form = UsernameChangeForm(initial=initial_data)
        context["form"] = form
        return render(request, 'ctf/my_page.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        form = UsernameChangeForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            user_obj = get_user_model().objects.get(username=request.user.username)
            user_obj.username = username
            user_obj.save()
            messages.info(request, "ユーザー名を変更しました。")

            return redirect('ctf:my_page')
        else:
            context["form"] = form

            return render(request, 'ctf/my_page.html', context)


my_page = MyPageView.as_view()


class ProblemDetailView(LoginRequiredMixin, View):
    model = Problem
    template_name = 'ctf/problem_detail.html'

    def get(self, request, *args, **kwargs):
        problem = get_object_or_404(Problem, pk=self.kwargs['pk'])
        context = {
            'problem': problem,
            'form': ProblemDetailForm(),
        }
        # 各問題詳細ぺージへ
        return TemplateResponse(request, 'ctf/problem_detail.html', context)

    def post(self, request, *args, **kwargs):
        form = ProblemDetailForm(request.POST)
        problem = get_object_or_404(Problem, pk=self.kwargs['pk'])

        if form.is_valid():
            # answer = UserProblem.objects.get(custom_user_id=self.request.user.id, problem_id=self.kwargs['pk'])

            # フラッシュメッセージを画面に表示
            query_problem = Problem.objects.get(id=self.kwargs['pk'])
            messages.success(request, "問題「{}」に正解しました。".format(query_problem.name))

            # 問題一覧画面にリダイレクト
            return HttpResponseRedirect(reverse('ctf:problem_list'))

        if not form.is_valid():
            # バリデーションNGの場合は問題詳細画面のテンプレートを再表示
            return TemplateResponse(request, 'ctf/problem_detail.html', {'form': form, 'problem': problem})


problem_detail = ProblemDetailView.as_view()
