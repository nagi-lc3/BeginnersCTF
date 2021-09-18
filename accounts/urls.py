from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name="login"),
    path('my_page/', views.my_page, name="my_page"),
]
