"""Forms"""
from django import forms

from .models import Player, Question, Quiz

categories = (
    ('ACTORS', 'ACTORS'), ('AFRICA', 'AFRICA'), ('AMERICA', 'AMERICA'), ('ANATOMY', 'ANATOMY'), ('ANIMALS', 'ANIMALS'),
    ('ART', 'ART'), ('ASIA', 'ASIA'), ('AUSTRALIA', 'AUSTRALIA'), ('AUTOMOTIVE', 'AUTOMOTIVE'),
    ('AVIATION', 'AVIATION'),
    ('BASEBALL', 'BASEBALL'), ('BASKETBALL', 'BASKETBALL'), ('BIOLOGY', 'BIOLOGY'), ('BIRD', 'BIRD'),
    ('CHEMISTRY', 'CHEMISTRY'), ('CHINA', 'CHINA'), ('CHRISTMAS', 'CHRISTMAS'), ('COMPUTER', 'COMPUTER'),
    ('COUNTRIES', 'COUNTRIES'),
    ('DISNEY', 'DISNEY'), ('DOG', 'DOG'),
    ('EARTH', 'EARTH'), ('EASY', 'EASY'), ('ENGLAND', 'ENGLAND'), ('EUROPE', 'EUROPE'),
    ('FAMOUS PEOPLE', 'FAMOUS PEOPLE'), ('FOOD AND DRINK', 'FOOD AND DRINK'), ('FOOTBALL', 'FOOTBALL'),
    ('FRANCE', 'FRANCE'),
    ('GAMES', 'GAMES'), ('GENERAL KNOWLEDGE', 'GENERAL KNOWLEDGE'), ('GEOGRAPHY', 'GEOGRAPHY'), ('GERMANY', 'GERMANY'),
    ('GOLF', 'GOLF'),
    ('HARRY POTTER', 'HARRY POTTER'), ('HISTORY', 'HISTORY'), ('HOCKEY', 'HOCKEY'),
    ('ITALY', 'ITALY'),
    ('JAPAN', 'JAPAN'),
    ('KIDS', 'KIDS'),
    ('LANGUAGE', 'LANGUAGE'), ('LITERATURE', 'LITERATURE'),
    ('MILITARY', 'MILITARY'), ('MONEY', 'MONEY'), ('MOON', 'MOON'), ('MOVIE', 'MOVIE'), ('MUSIC', 'MUSIC'),
    ('NEWS', 'NEWS'),
    ('OCEAN', 'OCEAN'), ('OLYMPICS', 'OLYMPICS'),
    ('PHYSICS', 'PHYSICS'), ('PLACES', 'PLACES'), ('PLANET', 'PLANET'), ('POLAND', 'POLAND'),
    ('POLITICAL', 'POLITICAL'), ('PORTUGAL', 'PORTUGAL'), ('PSYCHOLOGY', 'PSYCHOLOGY'),
    ('QUOTES', 'QUOTES'),
    ('RELIGIONS', 'RELIGIONS'),
    ('SAINTS', 'SAINTS'), ('SCIENCE', 'SCIENCE'), ('SPACE', 'SPACE'), ('SPAIN', 'SPAIN'), ('SPORTS', 'SPORTS'),
    ('STRANGER THINGS', 'STRANGER THINGS'), ('SUPER BOWL', 'SUPER BOWL'),
    ('TRAVEL', 'TRAVEL'), ('TV', 'TV'),
    ('UK', 'UK'), ('USA', 'USA'),
    ('VIDEO GAMES', 'VIDEO GAMES'),
    ('WORLD', 'WORLD'),
    ('OTHER', 'OTHER')
)


class CreateQuizForm(forms.ModelForm):
    """ form to create quiz"""
    name = forms.CharField(max_length=50, help_text='This name will be seen')
    category = forms.TypedChoiceField(choices=categories)
    topic = forms.CharField(max_length=50, help_text='Precise category')
    description = forms.CharField(max_length=50, required=False, help_text='Not required')

    class Meta:
        model = Quiz
        fields = ['name', 'category', 'topic', 'description']


class CreateQuestionForm(forms.ModelForm):
    """ form to create question"""
    answer = forms.CharField(max_length=200, help_text='Search wikipedia article')

    class Meta:
        model = Question
        fields = ['answer']
