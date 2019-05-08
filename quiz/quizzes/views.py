from django.http import HttpResponse, HttpRequest
from django.contrib import messages
import requests

from django.shortcuts import render, redirect

from .forms import CreateQuizForm, CreateQuestionForm
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


def create_question_type_title(request: HttpRequest) -> HttpResponse:
    """Render the create question page"""
    if request.method == 'POST':
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            key_word = form.save(commit=False)
            baseurl = 'http://en.wikipedia.org/w/api.php'
            my_atts = {}
            my_atts['action'] = 'query'  # action=query
            my_atts['list'] = 'search'
            my_atts['format'] = 'json'  # format=json
            my_atts['srsearch'] = key_word.answer
            resp = requests.get(baseurl, params=my_atts)
            data = resp.json()
            messages.success(request, 'Question successfully founded!')
            context = {
                'form': CreateQuestionForm(),
                'question': data,
                'generated': True
            }
            return render(request, 'question_generator_title.html', context=context)
        else:
            return HttpResponse("WHAT ARE YOU DOING?")
    return render(request, 'question_generator_title.html', context={'form': CreateQuestionForm(), 'generated': False})


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
