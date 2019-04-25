from django.urls import path

from . import views

app_name = 'quizzes'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('games/', views.choose_quiz_to_play, name='games'),
    path('games/<int:quiz_id>/', views.start_quiz, name='play_game'),
    path('my_quizzes/', views.list_player_quizzes, name='my_quizzes'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('log_in/', views.log_in, name='log_in'),
]