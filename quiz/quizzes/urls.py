from django.urls import path

from . import views

app_name = 'quizzes'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_quiz, name='create'),
    path('create_question/', views.create_question, name='create_question'),
    path('quizzes/', views.choose_quiz_to_play, name='quizzes'),
    path('quizzes/<int:quiz_id>/', views.start_quiz, name='quiz'),
    path('my_quizzes/', views.list_player_quizzes, name='my_quizzes'),
]