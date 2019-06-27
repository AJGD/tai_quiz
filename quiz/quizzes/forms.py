"""Forms"""
from django import forms
from django.forms.widgets import TextInput

from .models import Question, Quiz, Player

categories = (
    ('ACTORS', 'ACTORS'), ('AFRICA', 'AFRICA'), ('AMERICA', 'AMERICA'), ('ANATOMY', 'ANATOMY'),
    ('ANIMALS', 'ANIMALS'),
    ('ART', 'ART'), ('ASIA', 'ASIA'), ('AUSTRALIA', 'AUSTRALIA'), ('AUTOMOTIVE', 'AUTOMOTIVE'),
    ('AVIATION', 'AVIATION'),
    ('BASEBALL', 'BASEBALL'), ('BASKETBALL', 'BASKETBALL'), ('BIOLOGY', 'BIOLOGY'),
    ('BIRD', 'BIRD'),
    ('CHEMISTRY', 'CHEMISTRY'), ('CHINA', 'CHINA'), ('CHRISTMAS', 'CHRISTMAS'),
    ('COMPUTER', 'COMPUTER'),
    ('COUNTRIES', 'COUNTRIES'),
    ('DISNEY', 'DISNEY'), ('DOG', 'DOG'),
    ('EARTH', 'EARTH'), ('EASY', 'EASY'), ('ENGLAND', 'ENGLAND'), ('EUROPE', 'EUROPE'),
    ('FAMOUS PEOPLE', 'FAMOUS PEOPLE'), ('FOOD AND DRINK', 'FOOD AND DRINK'),
    ('FOOTBALL', 'FOOTBALL'),
    ('FRANCE', 'FRANCE'),
    ('GAMES', 'GAMES'), ('GENERAL KNOWLEDGE', 'GENERAL KNOWLEDGE'), ('GEOGRAPHY', 'GEOGRAPHY'),
    ('GERMANY', 'GERMANY'),
    ('GOLF', 'GOLF'),
    ('HARRY POTTER', 'HARRY POTTER'), ('HISTORY', 'HISTORY'), ('HOCKEY', 'HOCKEY'),
    ('ITALY', 'ITALY'),
    ('JAPAN', 'JAPAN'),
    ('KIDS', 'KIDS'),
    ('LANGUAGE', 'LANGUAGE'), ('LITERATURE', 'LITERATURE'),
    ('MILITARY', 'MILITARY'), ('MONEY', 'MONEY'), ('MOON', 'MOON'), ('MOVIE', 'MOVIE'),
    ('MUSIC', 'MUSIC'),
    ('NEWS', 'NEWS'),
    ('OCEAN', 'OCEAN'), ('OLYMPICS', 'OLYMPICS'),
    ('PHYSICS', 'PHYSICS'), ('PLACES', 'PLACES'), ('PLANET', 'PLANET'), ('POLAND', 'POLAND'),
    ('POLITICAL', 'POLITICAL'), ('PORTUGAL', 'PORTUGAL'), ('PSYCHOLOGY', 'PSYCHOLOGY'),
    ('QUOTES', 'QUOTES'),
    ('RELIGIONS', 'RELIGIONS'),
    ('SAINTS', 'SAINTS'), ('SCIENCE', 'SCIENCE'), ('SPACE', 'SPACE'), ('SPAIN', 'SPAIN'),
    ('SPORTS', 'SPORTS'),
    ('STRANGER THINGS', 'STRANGER THINGS'), ('SUPER BOWL', 'SUPER BOWL'),
    ('TRAVEL', 'TRAVEL'), ('TV', 'TV'),
    ('UK', 'UK'), ('USA', 'USA'),
    ('VIDEO GAMES', 'VIDEO GAMES'),
    ('WORLD', 'WORLD'),
    ('OTHER', 'OTHER')
)

general_categories = categories + (('ALL', 'ALL_CATEGORIES'),)


class CreateQuizForm(forms.ModelForm):
    """ form to create quiz"""
    name = forms.CharField(max_length=50,
                           help_text='This name will represent your quiz on the site.')
    category = forms.TypedChoiceField(choices=categories)
    topic = forms.CharField(max_length=50, help_text='Choose the exact topic within the category.')
    description = forms.CharField(max_length=50, required=False,
                                  help_text='Describe your quiz in a few words. Not required.')

    class Meta:
        model = Quiz
        fields = ['name', 'category', 'topic', 'description']


class CreateQuestionForm(forms.ModelForm):
    """ form to create question"""
    answer = forms.CharField(max_length=200)

    class Meta:
        model = Question
        fields = ['answer']


class ChooseArticleForm(forms.Form):
    def __init__(self, articles, *args, **kwargs):
        super(ChooseArticleForm, self).__init__(*args, **kwargs)
        self.fields['Choose article'] = forms.ChoiceField(choices=articles,
                                                          widget=forms.RadioSelect)


class ChooseWordToHide(forms.Form):
    word = forms.CharField(max_length=200)


class EnterAnswerGuess(forms.Form):
    def __init__(self, *args, **kwargs):
        super(EnterAnswerGuess, self).__init__(*args, **kwargs)
        self.fields['Answer'] = forms.CharField(max_length=200)


class FilterQuizForm(forms.ModelForm):
    """ form to filter quiz"""
    name = forms.CharField(max_length=50, required=False)
    author = forms.ModelChoiceField(queryset=Player.objects.all(),  # type: ignore
                                    to_field_name='id',
                                    required=False)
    category = forms.TypedChoiceField(choices=general_categories, required=False, initial="ALL")
    topic = forms.CharField(max_length=50, required=False)

    def __init__(self, *args, **kwargs):
        super(FilterQuizForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'id': field
            })

    class Meta:
        model = Quiz
        fields = ['name', 'author', 'category', 'topic']
