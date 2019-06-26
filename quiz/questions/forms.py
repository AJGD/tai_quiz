"""Forms"""
from django import forms

from quizzes.models import Question


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
