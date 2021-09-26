import datetime
import logging

import django_tables2
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy, reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django_tables2 import tables, RequestConfig

from .forms import ProblemDetailForm, InquiryForm, MyPageForm
from .models import Information, Problem, UserProblem
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    """indexページ"""

    template_name = 'ctf/index.html'


index = IndexView.as_view()


class InformationListView(ListView):
    """お知らせページ"""

    model = Information
    template_name = 'ctf/information.html'

    def get_queryset(self):
        return Information.objects.order_by('-created_at')


information = InformationListView.as_view()


class ImageColumn(django_tables2.Column):
    """アイコンのフォーマット"""

    def render(self, value):
        return mark_safe(
            '<img src="/media/%s" class="rounded-circle border me-1" width="40" height="40" alt="" loading="lazy" />'
            % escape(value))


class RankingTable(tables.Table):
    """ユーザテーブルのランキング表示"""

    icon = ImageColumn('アイコン')

    class Meta:
        model = get_user_model()
        fields = ('ranking', 'icon', 'username', 'score')


class RankingView(LoginRequiredMixin, View):
    """ランキングページ"""

    def get(self, request, *args, **kwargs):
        queryset = get_user_model().objects.order_by('ranking')
        # テーブルオブジェクトを作成
        table = RankingTable(queryset)
        RequestConfig(request).configure(table)
        table.paginate(page=request.GET.get('page', 1), per_page=100)
        context = {
            'table': table,
        }
        return TemplateResponse(request, 'ctf/ranking.html', context)


ranking = RankingView.as_view()


class ProblemListView(LoginRequiredMixin, ListView):
    """問題一覧ページ"""

    model = UserProblem
    template_name = 'ctf/problem_list.html'

    def get_queryset(self):
        return UserProblem.objects.all().select_related('problem').filter(
            custom_user_id=self.request.user.id, ).order_by('problem_id__level')


problem_list = ProblemListView.as_view()


class BoardView(LoginRequiredMixin, TemplateView):
    """掲示板ページ"""

    template_name = 'ctf/board.html'


board = BoardView.as_view()


class InquiryView(FormView):
    template_name = 'ctf/inquiry.html'
    form_class = InquiryForm
    success_url = reverse_lazy('ctf:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        # ロギング
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        # モデルに登録
        form.save()
        return super().form_valid(form)


inquiry = InquiryView.as_view()


class MyPageView(LoginRequiredMixin, View):
    """マイページ"""

    def get(self, request, *args, **kwargs):
        queryset = get_user_model().objects.get(id=request.user.id)
        initial_data = {
            'icon': queryset.icon,
            'username': queryset.username,
        }
        context = {}
        form = MyPageForm(initial=initial_data)
        context["form"] = form
        return render(request, 'ctf/my_page.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        # instanceでログイン中のユーザ情報をformsに返す
        form = MyPageForm(request.POST, request.FILES)

        if form.is_valid():
            icon = form.cleaned_data["icon"]
            username = form.cleaned_data["username"]

            # モデル変更
            user = get_user_model().objects.get(username=request.user.username)
            # ファイルを選択しない時はアイコンは変更しない
            if icon != 'icon/default.jpg':
                user.icon = icon
            user.username = username
            user.save()

            # メッセージ
            messages.info(request, "ユーザー情報を変更しました。")

            return redirect('ctf:my_page')

        else:
            # バリデーションチェックに引っかかった場合はアイコンのみ更新するか判断
            icon = form.cleaned_data["icon"]

            # ファイルを選択しない時はアイコンは変更しない
            if icon != 'icon/default.jpg':
                # モデル変更
                user = get_user_model().objects.get(username=request.user.username)
                user.icon = icon
                user.save()

                # メッセージ
                messages.info(request, "ユーザー情報を変更しました。")
                return redirect('ctf:my_page')
            else:
                context["form"] = form
                return render(request, 'ctf/my_page.html', context)


my_page = MyPageView.as_view()


class ProblemDetailView(LoginRequiredMixin, View):
    """問題詳細ページ"""

    model = Problem
    template_name = 'ctf/problem_detail.html'

    def get(self, request, *args, **kwargs):
        problem_pk = get_object_or_404(Problem, pk=self.kwargs['pk'])
        context = {
            'problem': problem_pk,
            'form': ProblemDetailForm(),
        }
        # 各問題詳細ぺージへ
        return TemplateResponse(request, 'ctf/problem_detail.html', context)

    def post(self, request, *args, **kwargs):
        form = ProblemDetailForm(request.POST)
        problem_pk = get_object_or_404(Problem, pk=self.kwargs['pk'])
        answer = request.POST.get('answer')

        if form.is_valid():
            problem = Problem.objects.get(id=self.kwargs['pk'])

            if answer == problem.answer:
                userproblem = UserProblem.objects.get(custom_user_id=self.request.user.id,
                                                      problem_id=self.kwargs['pk'])

                # はじめて問題に正解したときのみモデルを更新
                if not userproblem.problem_correct_answer:
                    # userProblemモデルを更新
                    userproblem.problem_correct_answer = True
                    userproblem.corrected_at = datetime.datetime.now()
                    userproblem.save()

                    # custom_userモデルのスコアを更新
                    user = get_user_model().objects.get(id=self.request.user.id)
                    user.score += problem.score
                    user.score_updated_at = datetime.datetime.now()
                    user.save()

                    # custom_userモデルのランキングを更新
                    update_custom_user = []
                    # 点数と点数更新日時でソートしてカラムを全て取り出して配列で回す
                    id_list = get_user_model().objects.values_list('id', flat=True).order_by('-score',
                                                                                             'score_updated_at')
                    # rank = インデックス, user_id = アイテム
                    for rank, user_id in enumerate(id_list):
                        custom_user = get_user_model()(id=user_id, ranking=rank + 1)
                        update_custom_user.append(custom_user)
                    get_user_model().objects.bulk_update(update_custom_user, fields=['ranking'])

                # ロギング
                logger.info(
                    "User(id={0}) answered Problem(id={1}) correctly.".format(self.request.user.id, self.kwargs['pk']))

                # フラッシュメッセージを画面に表示
                messages.success(request, "問題「{}」に正解しました。".format(problem.name))

                # 問題一覧画面にリダイレクト
                return HttpResponseRedirect(reverse('ctf:problem_list'))

            else:
                # フラッシュメッセージを画面に表示
                messages.error(request, "解答が違います。".format(problem.name))
                # 問題詳細画面を再表示
                return TemplateResponse(request, 'ctf/problem_detail.html', {'form': form, 'problem': problem_pk})

        if not form.is_valid():
            # バリデーションNGの場合は問題詳細画面を再表示
            return TemplateResponse(request, 'ctf/problem_detail.html', {'form': form, 'problem': problem_pk})


problem_detail = ProblemDetailView.as_view()
