"""Questions urls"""
from django.urls import path

from . import views

app_name = 'questions'
urlpatterns = [
    path('create_question_title/<int:question_id>/<str:article_id>', views.create_question_title,
         name='create_question_title'),
    path('quizzes/<int:quiz_id>/create_question/', views.create_question, name='create_question'),
    path('create_question_stat/', views.create_question_type_statistics,
         name='create_question_type_stat'),
    path('choose_question_type/<int:question_id>/<str:article_id>', views.choose_question_type,
         name='choose_question_type'),
    path('quizzes/<int:quiz_id>/questions', views.list_questions, name='questions'),
    path('quizzes/<int:quiz_id>/questions/<int:question_id>/delete',
         views.delete_question, name='delete_question'),
    path('quizzes/<int:quiz_id>/choose_best/<str:key_word>/', views.choose_best_article,
         name='choose_best_article'),
]
