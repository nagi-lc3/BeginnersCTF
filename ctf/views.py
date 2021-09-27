import datetime
import logging

import django_tables2
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy, reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django_tables2 import tables, RequestConfig

from .forms import ProblemDetailForm, InquiryForm, MyPageForm, AccountDeleteForm
from .models import Information, Problem, UserProblem
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

User = get_user_model()

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
            % (escape(value),))


class RankingTable(tables.Table):
    """ユーザテーブルのランキング表示"""

    icon = ImageColumn('アイコン')

    class Meta:
        model = User
        fields = ('ranking', 'icon', 'username', 'score')


class RankingView(LoginRequiredMixin, View):
    """ランキングページ"""

    def get(self, request, *args, **kwargs):
        queryset = User.objects.order_by('ranking')
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
        queryset = User.objects.get(id=request.user.id)
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
            user = User.objects.get(username=request.user.username)
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
                user = User.objects.get(username=request.user.username)
                user.icon = icon
                user.save()

                # メッセージ
                messages.info(request, "ユーザー情報を変更しました。")
                return redirect('ctf:my_page')
            else:
                context["form"] = form
                return render(request, 'ctf/my_page.html', context)


my_page = MyPageView.as_view()


class StatusView(LoginRequiredMixin, View):
    """ステータスページ"""

    model = User
    template_name = 'ctf/status.html'

    def get(self, request, *args, **kwargs):
        user_pk = get_object_or_404(User, pk=self.kwargs['pk'])

        # ALL
        all_count = User.objects.all().prefetch_related('userproblem').filter(
            userproblem__custom_user_id=self.request.user.id
        ).count()

        solved_all_count = User.objects.all().prefetch_related('userproblem').filter(
            userproblem__custom_user_id=self.request.user.id,
            userproblem__problem_correct_answer=True
        ).count()

        try:
            all_per = round((solved_all_count / all_count) * 100)
        except ZeroDivisionError:
            all_per = 0

        # Crypto
        crypto_count = User.objects.all().prefetch_related('userproblem').select_related(
            'problem').filter(
            userproblem__custom_user_id=self.request.user.id,
            problem__genre='crypto'
        ).count()

        solved_crypto_count = get_user_model().objects.all().prefetch_related('userproblem').select_related(
            'problem').filter(
            userproblem__custom_user_id=self.request.user.id,
            userproblem__problem_correct_answer=True,
            problem__genre='crypto'
        ).count()

        try:
            crypto_per = round((solved_crypto_count / crypto_count) * 100)
        except ZeroDivisionError:
            crypto_per = 0

        # Forensics
        forensics_count = User.objects.all().prefetch_related('userproblem').select_related(
            'problem').filter(
            userproblem__custom_user_id=self.request.user.id,
            problem__genre='forensics'
        ).count()

        solved_forensics_count = get_user_model().objects.all().prefetch_related('userproblem').select_related(
            'problem').filter(
            userproblem__custom_user_id=self.request.user.id,
            userproblem__problem_correct_answer=True,
            problem__genre='forensics'
        ).count()

        try:
            forensics_per = round((solved_forensics_count / forensics_count) * 100)
        except ZeroDivisionError:
            forensics_per = 0

        # Reversing
        reversing_count = User.objects.all().prefetch_related('userproblem').select_related(
            'problem').filter(
            userproblem__custom_user_id=self.request.user.id,
            problem__genre='reversing'
        ).count()

        solved_reversing_count = get_user_model().objects.all().prefetch_related('userproblem').select_related(
            'problem').filter(
            userproblem__custom_user_id=self.request.user.id,
            userproblem__problem_correct_answer=True,
            problem__genre='reversing'
        ).count()

        try:
            reversing_per = round((solved_reversing_count / reversing_count) * 100)
        except ZeroDivisionError:
            reversing_per = 0

        # Pwnable
        pwnable_count = User.objects.all().prefetch_related('userproblem').select_related(
            'problem').filter(
            userproblem__custom_user_id=self.request.user.id,
            problem__genre='pwnable'
        ).count()

        solved_pwnable_count = get_user_model().objects.all().prefetch_related('userproblem').select_related(
            'problem').filter(
            userproblem__custom_user_id=self.request.user.id,
            userproblem__problem_correct_answer=True,
            problem__genre='pwnable'
        ).count()

        try:
            pwnable_per = round((solved_pwnable_count / pwnable_count) * 100)
        except ZeroDivisionError:
            pwnable_per = 0

        # Web
        web_count = User.objects.all().prefetch_related('userproblem').select_related(
            'problem').filter(
            userproblem__custom_user_id=self.request.user.id,
            problem__genre='web'
        ).count()

        solved_web_count = get_user_model().objects.all().prefetch_related('userproblem').select_related(
            'problem').filter(
            userproblem__custom_user_id=self.request.user.id,
            userproblem__problem_correct_answer=True,
            problem__genre='web'
        ).count()

        try:
            web_per = round((solved_web_count / web_count) * 100)
        except ZeroDivisionError:
            web_per = 0

        # Network
        network_count = User.objects.all().prefetch_related('userproblem').select_related(
            'problem').filter(
            userproblem__custom_user_id=self.request.user.id,
            problem__genre='network'
        ).count()

        solved_network_count = get_user_model().objects.all().prefetch_related('userproblem').select_related(
            'problem').filter(
            userproblem__custom_user_id=self.request.user.id,
            userproblem__problem_correct_answer=True,
            problem__genre='network'
        ).count()

        try:
            network_per = round((solved_network_count / network_count) * 100)
        except ZeroDivisionError:
            network_per = 0

        # Misc
        misc_count = User.objects.all().prefetch_related('userproblem').select_related(
            'problem').filter(
            userproblem__custom_user_id=self.request.user.id,
            problem__genre='misc'
        ).count()

        solved_misc_count = get_user_model().objects.all().prefetch_related('userproblem').select_related(
            'problem').filter(
            userproblem__custom_user_id=self.request.user.id,
            userproblem__problem_correct_answer=True,
            problem__genre='misc'
        ).count()

        try:
            misc_per = round((solved_misc_count / misc_count) * 100)
        except ZeroDivisionError:
            misc_per = 0

        # レベル0
        level0_count = User.objects.all().prefetch_related('userproblem').select_related(
            'problem').filter(
            userproblem__custom_user_id=self.request.user.id,
            problem__level='0'
        ).count()

        solved_level0_count = get_user_model().objects.all().prefetch_related('userproblem').select_related(
            'problem').filter(
            userproblem__custom_user_id=self.request.user.id,
            userproblem__problem_correct_answer=True,
            problem__level='0'
        ).count()

        try:
            level0_per = round((solved_level0_count / level0_count) * 100)
        except ZeroDivisionError:
            level0_per = 0

        # レベル1
        level1_count = User.objects.all().prefetch_related('userproblem').select_related(
            'problem').filter(
            userproblem__custom_user_id=self.request.user.id,
            problem__level='1'
        ).count()

        solved_level1_count = get_user_model().objects.all().prefetch_related('userproblem').select_related(
            'problem').filter(
            userproblem__custom_user_id=self.request.user.id,
            userproblem__problem_correct_answer=True,
            problem__level='1'
        ).count()

        try:
            level1_per = round((solved_level1_count / level1_count) * 100)
        except ZeroDivisionError:
            level1_per = 0

        # レベル2
        level2_count = User.objects.all().prefetch_related('userproblem').select_related(
            'problem').filter(
            userproblem__custom_user_id=self.request.user.id,
            problem__level='2'
        ).count()

        solved_level2_count = get_user_model().objects.all().prefetch_related('userproblem').select_related(
            'problem').filter(
            userproblem__custom_user_id=self.request.user.id,
            userproblem__problem_correct_answer=True,
            problem__level='2'
        ).count()

        try:
            level2_per = round((solved_level2_count / level2_count) * 100)
        except ZeroDivisionError:
            level2_per = 0

        # レベル3
        level3_count = User.objects.all().prefetch_related('userproblem').select_related(
            'problem').filter(
            userproblem__custom_user_id=self.request.user.id,
            problem__level='3'
        ).count()

        solved_level3_count = get_user_model().objects.all().prefetch_related('userproblem').select_related(
            'problem').filter(
            userproblem__custom_user_id=self.request.user.id,
            userproblem__problem_correct_answer=True,
            problem__level='3'
        ).count()

        try:
            level3_per = round((solved_level3_count / level3_count) * 100)
        except ZeroDivisionError:
            level3_per = 0

        # レベル4
        level4_count = User.objects.all().prefetch_related('userproblem').select_related(
            'problem').filter(
            userproblem__custom_user_id=self.request.user.id,
            problem__level='4'
        ).count()

        solved_level4_count = get_user_model().objects.all().prefetch_related('userproblem').select_related(
            'problem').filter(
            userproblem__custom_user_id=self.request.user.id,
            userproblem__problem_correct_answer=True,
            problem__level='4'
        ).count()

        try:
            level4_per = round((solved_level4_count / level4_count) * 100)
        except ZeroDivisionError:
            level4_per = 0

        # レベル5
        level5_count = User.objects.all().prefetch_related('userproblem').select_related(
            'problem').filter(
            userproblem__custom_user_id=self.request.user.id,
            problem__level='5'
        ).count()

        solved_level5_count = get_user_model().objects.all().prefetch_related('userproblem').select_related(
            'problem').filter(
            userproblem__custom_user_id=self.request.user.id,
            userproblem__problem_correct_answer=True,
            problem__level='5'
        ).count()

        try:
            level5_per = round((solved_level5_count / level5_count) * 100)
        except ZeroDivisionError:
            level5_per = 0

        context = {
            'user': user_pk,

            'all_count': all_count,
            'solved_all_count': solved_all_count,
            'all_per': all_per,

            'crypto_count': crypto_count,
            'solved_crypto_count': solved_crypto_count,
            'crypto_per': crypto_per,

            'forensics_count': forensics_count,
            'solved_forensics_count': solved_forensics_count,
            'forensics_per': forensics_per,

            'reversing_count': reversing_count,
            'solved_reversing_count': solved_reversing_count,
            'reversing_per': reversing_per,

            'pwnable_count': pwnable_count,
            'solved_pwnable_count': solved_pwnable_count,
            'pwnable_per': pwnable_per,

            'web_count': web_count,
            'solved_web_count': solved_web_count,
            'web_per': web_per,

            'network_count': network_count,
            'solved_network_count': solved_network_count,
            'network_per': network_per,

            'misc_count': misc_count,
            'solved_misc_count': solved_misc_count,
            'misc_per': misc_per,

            'level0_count': level0_count,
            'solved_level0_count': solved_level0_count,
            'level0_per': level0_per,

            'level1_count': level1_count,
            'solved_level1_count': solved_level1_count,
            'level1_per': level1_per,

            'level2_count': level2_count,
            'solved_level2_count': solved_level2_count,
            'level2_per': level2_per,

            'level3_count': level3_count,
            'solved_level3_count': solved_level3_count,
            'level3_per': level3_per,

            'level4_count': level4_count,
            'solved_level4_count': solved_level4_count,
            'level4_per': level4_per,

            'level5_count': level5_count,
            'solved_level5_count': solved_level5_count,
            'level5_per': level5_per,
        }

        # ステータスぺージへ
        return TemplateResponse(request, 'ctf/status.html', context)


status = StatusView.as_view()


class AccountDeleteView(LoginRequiredMixin, View):
    """アカウント削除ページ"""

    model = User
    template_name = 'ctf/account_delete.html'

    def get(self, request, *args, **kwargs):
        context = {
            'form': AccountDeleteForm(),
        }
        return TemplateResponse(request, 'ctf/account_delete.html', context)

    def post(self, request, *args, **kwargs):
        form = AccountDeleteForm(request.POST)
        email = request.POST.get('email')

        if form.is_valid():
            user = User.objects.get(id=self.request.user.id)

            if email == user.email:
                user.delete()

                # ロギング
                logger.info("User(id={}) has deleted the account.".format(self.request.user.id))

                # フラッシュメッセージを画面に表示
                messages.success(request, "アカウント（{}）を削除しました。ご利用ありがとうございました。".format(self.request.user.email))

                return HttpResponseRedirect(reverse('account_login'))
            else:
                # フラッシュメッセージを画面に表示
                messages.error(request, "メールアドレスが一致しません。")

                # 問題詳細画面を再表示
                return TemplateResponse(request, 'ctf/account_delete.html', {'form': form})

        if not form.is_valid():
            return TemplateResponse(request, 'ctf/account_delete.html', {'form': form})


account_delete = AccountDeleteView.as_view()


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
                    user = User.objects.get(id=self.request.user.id)
                    user.score += problem.score
                    user.score_updated_at = datetime.datetime.now()
                    user.save()

                    # custom_userモデルのランキングを更新
                    update_custom_user = []
                    # 点数と点数更新日時でソートしてカラムを全て取り出して配列で回す
                    id_list = User.objects.values_list('id', flat=True).order_by('-score',
                                                                                 'score_updated_at')
                    # rank = インデックス, user_id = アイテム
                    for rank, user_id in enumerate(id_list):
                        custom_user = User(id=user_id, ranking=rank + 1)
                        update_custom_user.append(custom_user)
                    User.objects.bulk_update(update_custom_user, fields=['ranking'])

                # ロギング
                logger.info(
                    "User(id={0}) answered Problem(id={1}) correctly.".format(self.request.user.id, self.kwargs['pk']))

                # フラッシュメッセージを画面に表示
                messages.success(request, "問題「{}」に正解しました。".format(problem.name))

                # 問題一覧画面にリダイレクト
                return HttpResponseRedirect(reverse('ctf:problem_list'))

            else:
                # フラッシュメッセージを画面に表示
                messages.error(request, "解答が違います。")
                # 問題詳細画面を再表示
                return TemplateResponse(request, 'ctf/problem_detail.html', {'form': form, 'problem': problem_pk})

        if not form.is_valid():
            # バリデーションNGの場合は問題詳細画面を再表示
            return TemplateResponse(request, 'ctf/problem_detail.html', {'form': form, 'problem': problem_pk})


problem_detail = ProblemDetailView.as_view()
