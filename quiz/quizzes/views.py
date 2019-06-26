"""Quizzes views"""
from django import forms
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect

from .forms import CreateQuizForm, EnterTitleGuess, FilterQuizForm
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
            if request.user.is_authenticated:  # type: ignore
                added_quiz.author = Player.objects.get(pk=request.user.id)  # type: ignore
                added_quiz.save()
                messages.success(request, 'Quiz successfully added!')  # type: ignore
                return redirect('quizzes:quiz', quiz_id=added_quiz.id)
            return redirect('quizzes:index')
        return HttpResponse("WHAT ARE YOU DOING?")
    return render(request, 'quiz_generator.html', context={'form': CreateQuizForm()})


def list_player_quizzes(request: HttpRequest) -> HttpResponse:
    """Render the players own created quizzes page"""
    context = {'form': FilterQuizForm(), 'own': True}
    quizzes = Quiz.objects.all().order_by('id')  # type: ignore
    if request.method == 'POST':
        form = FilterQuizForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['author']:
                quizzes = quizzes.filter(author=form.cleaned_data['author'])
            if form.cleaned_data['category'] and form.cleaned_data['category'] != "ALL":
                quizzes = quizzes.filter(category=form.cleaned_data['category'])
            if form.cleaned_data['topic']:
                quizzes = quizzes.filter(topic=form.cleaned_data['topic'])
    if request.user.is_authenticated:  # type: ignore
        user = Player.objects.get(id=request.user.id)  # type: ignore
        quizzes = quizzes.filter(author=user)  # type: ignore
    page = request.GET.get('page', 1)
    paginator = Paginator(quizzes, 10)
    try:
        quizzes = paginator.page(page)
    except PageNotAnInteger:
        quizzes = paginator.page(1)
    except EmptyPage:
        quizzes = paginator.page(paginator.num_pages)  # type: ignore
    context['quizzes'] = quizzes
    return render(request, 'user_quizzes.html', context)


def choose_quiz_to_play(request):
    """Render the all quizzes created by all users page exclude this logged in"""
    context = {'form': FilterQuizForm()}
    quizzes = Quiz.objects.all().order_by('id')  # type: ignore
    if request.method == 'POST':
        form = FilterQuizForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['name']:
                quizzes = quizzes.filter(name__icontains=form.cleaned_data['name'])
            if form.cleaned_data['author']:
                quizzes = quizzes.filter(author=form.cleaned_data['author'])
            if form.cleaned_data['category'] and form.cleaned_data['category'] != "ALL":
                quizzes = quizzes.filter(category=form.cleaned_data['category'])
            if form.cleaned_data['topic']:
                quizzes = quizzes.filter(topic__icontains=form.cleaned_data['topic'])
    if request.user.is_authenticated:
        quizzes = quizzes.exclude(author=request.user)  # type: ignore
    else:
        quizzes = quizzes
    page = request.GET.get('page', 1)
    paginator = Paginator(quizzes, 10)
    try:
        quizzes = paginator.page(page)
    except PageNotAnInteger:
        quizzes = paginator.page(1)
    except EmptyPage:
        quizzes = paginator.page(paginator.num_pages)
    context['quizzes'] = quizzes
    return render(request, 'all_quizzes.html', context=context)


def open_quiz(request, quiz_id):
    """Render the single quiz page"""
    quiz = Quiz.objects.get(pk=quiz_id)  # type: ignore
    if request.user.is_authenticated and (quiz.author.id == request.user.id):
        return render(request, 'quiz_edit_page.html', context={'quiz': quiz})
    return render(request, 'quiz_start_page.html',
                  context={'quiz': quiz, 'any_questions': bool(Question.objects.filter(quiz=quiz))})


def solve_quiz(request: HttpRequest, quiz_id) -> HttpResponse:
    """Render the page for solving the quiz"""
    enter_title_guess_form_set = forms.formset_factory(EnterTitleGuess, extra=0)  # type: ignore
    questions = Question.objects.filter(quiz=quiz_id)  # type: ignore
    if request.method == "POST":
        score = 0
        questions_number = 0
        formset = enter_title_guess_form_set(request.POST,
                                             initial=[{'question': question}
                                                      for question in questions])
        if formset.is_valid():
            for form in formset:
                questions_number += 1
                cleaned_data = form.cleaned_data
                if form.initial.get('question').answer == cleaned_data.get('Title'):
                    score += 1
            return render(request, 'quiz_results.html',
                          context={'result': 100 * (score / questions_number)})
    formset = enter_title_guess_form_set(initial=[{'question': question} for question in questions])
    return render(request, 'solve_quiz.html', context={'formset': formset})


def delete_quiz(request: HttpRequest, quiz_id) -> HttpResponse:
    """Delete the quiz specified by quiz_id."""
    author_id = Quiz.objects.get(id=quiz_id).author.id  # type: ignore
    if request.user.is_authenticated and (author_id == request.user.id):  # type: ignore
        Quiz.objects.filter(id=quiz_id).delete()  # type: ignore
        messages.success(request, 'Quiz deleted successfully.')  # type: ignore
        return redirect('quizzes:my_quizzes')
    return render(request, 'no_permission_error.html')
