from django.urls import path

from . import views

app_name = 'quizzes'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_quiz, name='create'),
    path('create_question_title/<int:question_id>/<str:article_id>', views.create_question_title, name='create_question_title'),
    path('quizzes/<int:quiz_id>/create_question/', views.create_question, name='create_question'),
    path('quizzes/<int:quiz_id>/choose_best/<str:key_word>/', views.choose_best_article, name='choose_best_article'),
    path('create_question_stat/', views.create_question_type_statistics, name='create_question_type_stat'),
    path('choose_question_type/<int:question_id>/<str:article_id>', views.choose_question_type, name='choose_question_type'),
    path('quizzes/', views.choose_quiz_to_play, name='quizzes'),
    path('quizzes/<int:quiz_id>/', views.open_quiz, name='quiz'),
    path('quizzes/<int:quiz_id>/solve', views.solve_quiz, name='solve_quiz'),
    path('quizzes/<int:quiz_id>/questions', views.list_questions, name='questions'),
    path('my_quizzes/', views.list_player_quizzes, name='my_quizzes'),
]