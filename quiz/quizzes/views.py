from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect

from .forms import CreateQuizForm, CreateQuestionForm, ChooseArticleForm, ChooseWordToHide
from .mediawiki_utils import find_article, find_articles_list
from .models import Player, Quiz, Question


def index(_request: HttpRequest) -> HttpResponse:
    """Render the main page"""
    context: dict = {}
    return render(_request, 'index.html', context)


def create_quiz(request: HttpRequest) -> HttpResponse:
    """Render the create quiz page"""
    if request.method == 'POST':
        form = CreateQuizForm(request.POST)
        if form.is_valid():
            added_quiz = form.save(commit=False)
            if request.user.is_authenticated:
                added_quiz.author = Player.objects.get(pk=request.user.id)
                added_quiz.save()
                messages.success(request, 'Quiz successfully added!')
                return redirect('quizzes:quiz', quiz_id=added_quiz.id)
            else:
                return redirect('quizzes:index')
        else:
            return HttpResponse("WHAT ARE YOU DOING?")
    else:
        form = CreateQuizForm()
    context = {
        'form': form
    }
    return render(request, 'quiz_generator.html', context=context)


def choose_question_type(request: HttpRequest, article_id, question_id) -> HttpResponse:
    question = Question.objects.get(pk=question_id)
    if question.quiz.author != request.user.id:
        render(request, 'default_error.html')
    found_article = find_article(article_id)
    return render(request, 'question_type_chooser.html',
                  context={'form': CreateQuestionForm(), 'generated': False, 'article': found_article[0],
                           'title': found_article[1], 'article_id': article_id, 'question_id': question_id})


#################################################################
# QUESTIONS TYPE BY TITLE
#################################################################

def create_question_title(request: HttpRequest, article_id, question_id) -> HttpResponse:
    """Render the page to choose concrete article"""
    question = Question.objects.get(pk=question_id)
    if question.quiz.author != request.user.id:
        render(request, 'default_error.html')
    found_article = find_article(article_id)
    if question.question_text == '':
        question.question_text = found_article[0]
    if question.answer == '':
        question.answer = found_article[1]
    if question.source_url == '':
        question.source_url = found_article[2]
    if request.method == 'POST':
        form = ChooseWordToHide(request.POST)
        if form.is_valid():
            word = form.cleaned_data['word']
            question.question_text = question.question_text.replace(word, "####")
            question.type = 'Title'
            question.article_id = article_id
            question.save()
            redirect('quizzes:create_question_title', article_id=article_id, question_id=question_id)
        else:
            return render(request, 'default_error.html')
    context = {
        'article_id': article_id,
        'article': question.question_text,
        'title': question.answer,
        'chooser': ChooseWordToHide(),
    }
    return render(request, 'create_question_title.html', context=context)


def create_question(request: HttpRequest, quiz_id) -> HttpResponse:
    """Render the create question page"""
    if Quiz.objects.get(pk=quiz_id).author != request.user.id:
        render(request, 'default_error.html')
    if request.method == 'POST':
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            key_word = form.save(commit=False)
            return redirect('quizzes:choose_best_article', key_word=key_word.answer, quiz_id=quiz_id)
        else:
            return render(request, 'default_error.html')
    return render(request, 'question_generator_title.html', context={'form': CreateQuestionForm(), 'generated': False})


def choose_best_article(request: HttpRequest, quiz_id, key_word) -> HttpResponse:
    """Render the page to choose concrete article"""
    if Quiz.objects.get(pk=quiz_id).author != request.user.id:
        render(request, 'default_error.html')
    data_list = find_articles_list(key_word)
    if request.method == 'POST':
        form = ChooseArticleForm(data_list, request.POST)
        if form.is_valid():
            pageid = form.cleaned_data['Choose article']
            question = Question.objects.create(author_id=request.user.id, quiz_id=quiz_id, article_id=pageid)
            return redirect('quizzes:choose_question_type', article_id=pageid, question_id=question.id)
        else:
            return render(request, 'default_error.html')
    context = {
        'chooser': ChooseArticleForm(data_list)
    }
    return render(request, 'choose_article.html', context=context)


#################################################################

def create_question_type_statistics(request: HttpRequest) -> HttpResponse:
    """Render the create question page type statistics"""
    return render(request, 'still_working.html')


def list_player_quizzes(request: HttpRequest) -> HttpResponse:
    """Render the players own created quizzes page"""
    context = {}
    if request.user.is_authenticated:
        user = Player.objects.get(id=request.user.id)
        context = {
            'quizzes': Quiz.objects.filter(author=user)
        }
    return render(request, 'user_quizzes.html', context)


def choose_quiz_to_play(request: HttpRequest) -> HttpResponse:
    """Render the all quizzes created by all users page"""
    context = {
        'quizzes': Quiz.objects.all()
    }
    return render(request, 'all_quizzes.html', context=context)


def start_quiz(request, quiz_id):
    """Render the single quiz page"""
    if request.user.is_authenticated and (Quiz.objects.get(pk=quiz_id).author.id == request.user.id):
        return render(request, 'quiz_edit_page.html', context={'id': quiz_id})
    return render(request, 'quiz_start_page.html', context={'id': quiz_id})


def list_questions(request: HttpRequest, quiz_id) -> HttpResponse:
    quiz = Quiz.objects.get(id=quiz_id)
    context = {
        'questions': Question.objects.filter(quiz=quiz),
        'quiz': quiz
    }
    return render(request, 'question_list.html', context)
