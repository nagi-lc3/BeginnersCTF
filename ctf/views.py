from .forms import UsernameChangeForm
from .models import Information, Problem, UserProblem
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView, ListView
from django.shortcuts import render, redirect
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

    # クエリ数が多くなるかも
    def get_queryset(self):
        for i in range(Problem.objects.count()):
            result, created = UserProblem.objects.get_or_create(custom_user_id=self.request.user.id,
                                                                problem_id=i + 1)

    # def get_queryset(self):
    #     add_user_problem = []
    #     for i in range(Problem.objects.count()):
    #         user_problem = UserProblem(custom_user_id=self.request.user.id, problem_id=i + 1)
    #         add_user_problem.append(user_problem)
    #     # ignore_conflicts=Trueで重複回避
    #     UserProblem.objects.bulk_create(add_user_problem, ignore_conflicts=True)

        return UserProblem.objects.all().select_related('problem').filter(
            custom_user_id=self.request.user.id, ).order_by('problem_id__level')


# def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     context['problem_list'] = Problem.objects.all()
#     return context


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
