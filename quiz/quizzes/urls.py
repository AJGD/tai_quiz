"""Quizzes urls"""
from django.urls import path

from . import views

app_name = 'quizzes'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_quiz, name='create'),
    path('quizzes/', views.choose_quiz_to_play, name='quizzes'),
    path('quizzes/<int:quiz_id>/', views.open_quiz, name='quiz'),
    path('quizzes/<int:quiz_id>/delete', views.delete_quiz, name='delete_quiz'),
    path('quizzes/<int:quiz_id>/solve', views.solve_quiz, name='solve_quiz'),
    path('my_quizzes/', views.list_player_quizzes, name='my_quizzes'),
]
