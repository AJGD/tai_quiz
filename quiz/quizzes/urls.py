from django.urls import path

from . import views

app_name = 'quizzes'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_quiz, name='create'),
    path('create_question_title/', views.create_question_type_title, name='create_question_type_title'),
    path('create_question_stat/', views.create_question_type_statistics, name='create_question_type_stat'),
    path('choose_question_type/', views.choose_question_type, name='choose_question_type'),
    path('quizzes/', views.choose_quiz_to_play, name='quizzes'),
    path('quizzes/<int:quiz_id>/', views.start_quiz, name='quiz'),
    path('questions/<int:quiz_id>/', views.list_questions, name='questions'),
    path('my_quizzes/', views.list_player_quizzes, name='my_quizzes'),
]