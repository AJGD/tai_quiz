"""Views for the 'questions' app"""
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from quizzes.models import Question, Quiz

from .forms import ChooseWordToHide, CreateQuestionForm, ChooseArticleForm
from .forms import EnterMonthAndYearForm
from .mediawiki_utils import find_article, get_article_and_views, find_articles_list


def create_question(request: HttpRequest, quiz_id) -> HttpResponse:
    """Render the create question page"""
    if Quiz.objects.get(pk=quiz_id).author != request.user.id:  # type: ignore
        render(request, 'default_error.html')
    if request.method == 'POST':
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            key_word = form.save(commit=False)
            return redirect('questions:choose_best_article',
                            key_word=key_word.answer, quiz_id=quiz_id)
        return render(request, 'default_error.html')
    return render(request, 'question_generator_title.html',
                  context={'form': CreateQuestionForm(), 'generated': False})


def create_question_title(request: HttpRequest, article_id, question_id) -> HttpResponse:
    """Render the page to choose concrete article"""
    question = Question.objects.get(pk=question_id)  # type: ignore
    if question.quiz.author != request.user.id:  # type: ignore
        render(request, 'default_error.html')
    initialize_question(article_id, question)
    if request.method == 'POST':
        form = ChooseWordToHide(request.POST)
        if form.is_valid():
            replace_word(form, question)
            question.type = 'Title'
            question.article_id = article_id
            question.save()
            redirect('questions:create_question_title', article_id=article_id,
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


def replace_word(form, question):
    word = form.cleaned_data['word']
    question.question_text = question.question_text.replace(word, len(word) * " _")


def initialize_question(article_id, question):
    """helper function for filling the title-type question"""
    found_article = find_article(article_id)
    if question.question_text == '':
        question.question_text = 'What is the title of this article? "' \
                                 + found_article[0] + '"'
    if question.answer == '':
        question.answer = found_article[1]
    if question.source_url == '':
        question.source_url = found_article[2]


def create_question_type_statistics(request: HttpRequest, article_id, question_id) -> HttpResponse:
    """Render the create question page type statistics"""
    question = Question.objects.get(pk=question_id)  # type: ignore
    if question.quiz.author != request.user.id:  # type: ignore
        render(request, 'default_error.html')
    if request.method == 'POST':
        form = EnterMonthAndYearForm(request.POST)
        if form.is_valid():
            found_date = form.cleaned_data['date']
            found_article = get_article_and_views(article_id,
                                                  year=found_date.year, month=found_date.month)
            fill_stat_type_question(article_id, found_article, found_date, question)
            question.save()
            redirect('questions:create_question_type_stat',
                     article_id=article_id, question_id=question_id)
        else:
            print(form.errors)
            return render(request, 'default_error.html')
    context = {
        'article_id': article_id,
        'article': question.question_text,
        'title': find_article(article_id)[1],
        'form': EnterMonthAndYearForm(),
        'quiz': question.quiz,
    }
    return render(request, 'create_question_statistics.html', context=context)


def fill_stat_type_question(article_id, found_article, found_date, question):
    """Given an article, a date and some already gathered data, fill the details
    of a statistics-type question"""
    if question.source_url == '':
        question.source_url = found_article[2]
    question.question_text = \
        'How many times was the article "' \
        + found_article[0] + '" viewed in the month of ' \
        + str(found_date.year) + "-" + str(found_date.month) + "?"
    question.type = 'Statistic'
    question.article_id = article_id
    question.answer = found_article[1]


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


def list_questions(request: HttpRequest, quiz_id) -> HttpResponse:
    """Render the page of list of all questions"""
    quiz = Quiz.objects.get(id=quiz_id)  # type: ignore
    questions = Question.objects.filter(quiz=quiz).order_by('id')  # type: ignore
    page = request.GET.get('page', 1)
    paginator = Paginator(questions, 10)
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)  # type: ignore
    context = {
        'questions': questions,  # type: ignore
        'quiz': quiz
    }
    return render(request, 'question_list.html', context)


def delete_question(request: HttpRequest, quiz_id, question_id) -> HttpResponse:
    """Delete the question specified by question_id."""
    author_id = Quiz.objects.get(id=quiz_id).author.id  # type: ignore
    if request.user.is_authenticated and (author_id == request.user.id):  # type: ignore
        Question.objects.filter(id=question_id).delete()  # type: ignore
        messages.success(request, 'Question deleted successfully.')  # type: ignore
        return redirect('questions:questions', quiz_id=quiz_id)
    return render(request, 'no_permission_error.html')


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
            return redirect('questions:choose_question_type',
                            article_id=pageid, question_id=question.id)
        return render(request, 'default_error.html')
    context = {
        'chooser': ChooseArticleForm(data_list)
    }
    return render(request, 'choose_article.html', context=context)
