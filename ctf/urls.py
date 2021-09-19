from django.urls import path

from . import views

app_name = 'ctf'
urlpatterns = [
    path('', views.index, name="index"),
    path('information/', views.information, name="information"),
    path('ranking/', views.ranking, name="ranking"),
    path('problem_list/', views.problem_list, name="problem_list"),
    path('board/', views.board, name="board"),
    path('my_page/', views.my_page, name="my_page"),
]
