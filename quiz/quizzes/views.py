from django.shortcuts import render

from django.http import HttpResponse, HttpRequest


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


def create(request: HttpRequest) -> HttpResponse:
    """Render the create quiz page"""
    return render(request, 'still_working.html')


def list_player_quizzes(request: HttpRequest) -> HttpResponse:
    """Render the players own created quizzes page"""
    return render(request, 'still_working.html')


def choose_quiz_to_play(request: HttpRequest) -> HttpResponse:
    """Render the all quizzes created by all users page"""
    return render(request, 'all_quizzes.html', context={'id': 1})


def start_quiz(request, quiz_id):
    """Render the single quiz page"""
    return render(request, 'quiz_start_page.html', context={'id': quiz_id})