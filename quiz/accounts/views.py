"""Accounts views"""
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from quizzes.models import Player


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields["password2"].help_text = None

    class Meta(UserCreationForm.Meta):  # type: ignore
        model = Player
        fields = UserCreationForm.Meta.fields  # type: ignore


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def show_privacy_policy(request: HttpRequest) -> HttpResponse:
    return render(request, 'privacy_policy.html')
