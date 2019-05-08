from django.http import HttpResponse, HttpRequest
from django.contrib import messages

from django.shortcuts import render, redirect

from .mediawiki_utils import find_article, find_articles_list
from .forms import CreateQuizForm, CreateQuestionForm, ChooseArticleForm
from .models import Player, Quiz


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


def choose_question_type(request: HttpRequest) -> HttpResponse:
    return render(request, 'question_type_chooser.html', context={'form': CreateQuestionForm(), 'generated': False})


#################################################################
# QUESTIONS TYPE BY TITLE
#################################################################

def create_question_type_title(request: HttpRequest) -> HttpResponse:
    """Render the create question page"""
    if request.method == 'POST':
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            key_word = form.save(commit=False)
            return redirect('quizzes:choose_best_article', key_word=key_word.answer)
        else:
            return HttpResponse("WHAT ARE YOU DOING?")
    return render(request, 'question_generator_title.html', context={'form': CreateQuestionForm(), 'generated': False})


def choose_best_article(request: HttpRequest, key_word) -> HttpResponse:
    """Render the page to choose concrete article"""
    data_list = find_articles_list(key_word)
    if request.method == 'POST':
        form = ChooseArticleForm(data_list, request.POST)
        if form.is_valid():
            pageid = form.cleaned_data['Choose article']
            found_article = find_article(pageid)
            context = {
                'article': found_article[0],
                'title': found_article[1]
            }
            return render(request, 'show_generated_question.html', context=context)
        else:
            return HttpResponse("WHAT ARE YOU DOING?")
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
    # TODO I-8
    return render(request, 'question_list.html')
