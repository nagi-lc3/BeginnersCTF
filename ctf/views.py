from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'ctf/index.html'


index = IndexView.as_view()


class InformationView(TemplateView):
    template_name = 'ctf/information.html'


information = InformationView.as_view()


class RankingView(TemplateView):
    template_name = 'ctf/ranking.html'


ranking = RankingView.as_view()


class ProblemListView(TemplateView):
    template_name = 'ctf/problem_list.html'


problem_list = ProblemListView.as_view()


class BoardView(TemplateView):
    template_name = 'ctf/board.html'


board = BoardView.as_view()
