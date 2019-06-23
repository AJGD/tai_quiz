"""Quizzes views"""
from django import forms
from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect

from .forms import CreateQuizForm, CreateQuestionForm, ChooseArticleForm, ChooseWordToHide, \
    EnterTitleGuess, FilterQuizForm
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
            if request.user.is_authenticated:  # type: ignore
                added_quiz.author = Player.objects.get(pk=request.user.id)  # type: ignore
                added_quiz.save()
                messages.success(request, 'Quiz successfully added!')  # type: ignore
                return redirect('quizzes:quiz', quiz_id=added_quiz.id)
            return redirect('quizzes:index')
        return HttpResponse("WHAT ARE YOU DOING?")
    return render(request, 'quiz_generator.html', context={'form': CreateQuizForm()})


def choose_question_type(request: HttpRequest, article_id, question_id) -> HttpResponse:
    """Render the choose question type page"""
    question = Question.objects.get(pk=question_id)  # type: ignore
    if question.quiz.author != request.user.id:  # type: ignore
        render(request, 'default_error.html')
    found_article = find_article(article_id)
    return render(request, 'question_type_chooser.html',
                  context={'form': CreateQuestionForm(), 'generated': False,
                           'article': found_article[0],
                           'title': found_article[1], 'article_id': article_id,
                           'question_id': question_id})


#################################################################
# QUESTIONS TYPE BY TITLE
#################################################################

def create_question_title(request: HttpRequest, article_id, question_id) -> HttpResponse:
    """Render the page to choose concrete article"""
    question = Question.objects.get(pk=question_id)  # type: ignore
    if question.quiz.author != request.user.id:  # type: ignore
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
            question.question_text = question.question_text.replace(word, len(word) * "_ ")
            question.type = 'Title'
            question.article_id = article_id
            question.save()
            redirect('quizzes:create_question_title', article_id=article_id,
                     question_id=question_id)
        else:
            return render(request, 'default_error.html')
    context = {
        'article_id': article_id,
        'article': question.question_text,
        'title': question.answer,
        'chooser': ChooseWordToHide(),
        'quiz_id': question.quiz.id,
        'source_url': question.source_url
    }
    return render(request, 'create_question_title.html', context=context)


def create_question(request: HttpRequest, quiz_id) -> HttpResponse:
    """Render the create question page"""
    if Quiz.objects.get(pk=quiz_id).author != request.user.id:  # type: ignore
        render(request, 'default_error.html')
    if request.method == 'POST':
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            key_word = form.save(commit=False)
            return redirect('quizzes:choose_best_article',
                            key_word=key_word.answer, quiz_id=quiz_id)
        return render(request, 'default_error.html')
    return render(request, 'question_generator_title.html',
                  context={'form': CreateQuestionForm(), 'generated': False})


def choose_best_article(request: HttpRequest, quiz_id, key_word) -> HttpResponse:
    """Render the page to choose concrete article"""
    if Quiz.objects.get(pk=quiz_id).author != request.user.id:  # type: ignore
        render(request, 'default_error.html')
    data_list = find_articles_list(key_word)
    if request.method == 'POST':
        form = ChooseArticleForm(data_list, request.POST)
        if form.is_valid():
            pageid = form.cleaned_data['Choose article']
            question = Question.objects.create(  # type: ignore
                author_id=request.user.id, quiz_id=quiz_id, article_id=pageid)  # type: ignore
            return redirect('quizzes:choose_question_type',
                            article_id=pageid, question_id=question.id)
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
    context = {'form': FilterQuizForm(), 'own': True}
    quizzes = Quiz.objects.all()  # type: ignore
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
    context['quizzes'] = quizzes
    return render(request, 'user_quizzes.html', context)


def choose_quiz_to_play(request):
    """Render the all quizzes created by all users page exclude this logged in"""
    context = {'form': FilterQuizForm()}
    quizzes = Quiz.objects.all()  # type: ignore
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
        context['quizzes'] = quizzes.exclude(author=request.user)  # type: ignore
    else:
        context['quizzes'] = quizzes
    return render(request, 'all_quizzes.html', context=context)


def open_quiz(request, quiz_id):
    """Render the single quiz page"""
    quiz = Quiz.objects.get(pk=quiz_id)  # type: ignore
    if request.user.is_authenticated and (quiz.author.id == request.user.id):
        return render(request, 'quiz_edit_page.html', context={'quiz': quiz})
    return render(request, 'quiz_start_page.html',
                  context={'quiz': quiz, 'any_questions': bool(Question.objects.filter(quiz=quiz))})


def list_questions(request: HttpRequest, quiz_id) -> HttpResponse:
    """Render the page of list of all questions"""
    quiz = Quiz.objects.get(id=quiz_id)  # type: ignore
    context = {
        'questions': Question.objects.filter(quiz=quiz),  # type: ignore
        'quiz': quiz
    }
    return render(request, 'question_list.html', context)


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


def delete_question(request: HttpRequest, quiz_id, question_id) -> HttpResponse:
    """Delete the question specified by question_id."""
    author_id = Quiz.objects.get(id=quiz_id).author.id  # type: ignore
    if request.user.is_authenticated and (author_id == request.user.id):  # type: ignore
        Question.objects.filter(id=question_id).delete()  # type: ignore
        messages.success(request, 'Question deleted successfully.')  # type: ignore
        return redirect('quizzes:questions', quiz_id=quiz_id)
    return render(request, 'no_permission_error.html')


def delete_quiz(request: HttpRequest, quiz_id) -> HttpResponse:
    """Delete the quiz specified by quiz_id."""
    author_id = Quiz.objects.get(id=quiz_id).author.id  # type: ignore
    if request.user.is_authenticated and (author_id == request.user.id):  # type: ignore
        Quiz.objects.filter(id=quiz_id).delete()  # type: ignore
        messages.success(request, 'Quiz deleted successfully.')  # type: ignore
        return redirect('quizzes:my_quizzes')
    return render(request, 'no_permission_error.html')
