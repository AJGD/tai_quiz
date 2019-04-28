from django.shortcuts import render, redirect
import requests
from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
import requests

from .models import Player, Quiz
from .forms import CreateQuizForm, CreateQuestionForm
from django.shortcuts import render, redirect

from .forms import CreateQuizForm, CreateQuestionForm
from .models import Player, Quiz


def index(_request: HttpRequest) -> HttpResponse:
    """Render the main page"""
    context: dict = {}
    return render(_request, 'index.html', context)


def sign_up(request: HttpRequest) -> HttpResponse:
    """Render the sign up page"""
    return render(request, 'still_working.html')


def log_in(request: HttpRequest) -> HttpResponse:
    """Render the log in page"""
    return render(request, 'still_working.html')


def create_quiz(request: HttpRequest) -> HttpResponse:
    """Render the create quiz page"""
    resp = requests.get("http://en.wikipedia.org/w/api.php?action=query&prop=info&format=json&titles=Hello")
    print(resp.status_code)  # 200
    print(resp.json())
    if request.method == 'POST':
        form = CreateQuizForm(request.POST)
        if form.is_valid():
            added_quiz = form.save(commit=False)
            # mock_author = Player(username="w3d", email="kleo@example.com")
            # mock_author.save()
            if request.user.is_authenticated:
                added_quiz.author = Player.objects.get(pk=request.user.id)
                added_quiz.save()
                messages.success(request, 'Quiz successfully added!')
                return redirect('quizzes:quiz', quiz_id=added_quiz.id)
            else:
                messages.error(request, 'unable to add quiz when user is not logged in')
                return redirect('quizzes:index')
        else:
            return HttpResponse("WHAT ARE YOU DOING?")
    else:
        form = CreateQuizForm()
    context = {
        'form': form
    }
    return render(request, 'quiz_generator.html', context=context)


def create_question(request: HttpRequest) -> HttpResponse:
    """Render the create question page"""
    if request.method == 'POST':
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            key_word = form.save(commit=False)
            # mock_author = Player(username="Kleofas", email="kleo@example.com")
            # mock_author.save()
            # added_quiz.author = Player.objects.get(username="Kleofas")
            # added_quiz.save()
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
            return render(request, 'question_generator.html', context=context)
        else:
            return HttpResponse("WHAT ARE YOU DOING?")
    return render(request, 'question_generator.html', context={'form': CreateQuestionForm(), 'generated': False})


def list_player_quizzes(request: HttpRequest) -> HttpResponse:
    """Render the players own created quizzes page"""
    user = Player.objects.get(username="Kleofas")
    context = {
        'quizzes': Quiz.objects.filter(author=user)
    }
    return render(request, 'user_quizzes.html', context)


def choose_quiz_to_play(request: HttpRequest) -> HttpResponse:
    """Render the all quizzes created by all users page"""
    return render(request, 'all_quizzes.html', context={'id': 1})


def start_quiz(request, quiz_id):
    """Render the single quiz page"""
    if request.user.is_authenticated and (Quiz.objects.get(pk=quiz_id).author.id == request.user.id):
        return render(request, 'quiz_edit_page.html', context={'id': quiz_id})
    return render(request, 'quiz_start_page.html', context={'id': quiz_id})
