from django.views.generic import TemplateView


class MyPageView(TemplateView):
    template_name = 'accounts/my_page.html'


my_page = MyPageView.as_view()


class LoginView(TemplateView):
    template_name = 'accounts/login.html'


login = LoginView.as_view()
