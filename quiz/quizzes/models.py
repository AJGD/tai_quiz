"""Quizzes models"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Player(AbstractUser):
    """User of app"""
    username: models.CharField = models.CharField(max_length=50, unique=True)
    email: models.EmailField = models.EmailField()
    date_joined: models.DateTimeField = models.DateTimeField("date joined", default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Quiz(models.Model):
    """Model of quiz"""
    name: models.CharField = models.CharField(max_length=100, null=False, default='')
    category: models.CharField = models.CharField(max_length=100, null=False, default='')
    topic: models.CharField = models.CharField(max_length=100, null=False, default='')
    description: models.CharField = models.CharField(max_length=100)
    author: models.ForeignKey = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name='quiz_author')

    def __str__(self):
        return self.topic


class Question(models.Model):
    """Model of question"""
    question_text: models.CharField = models.CharField(max_length=4196, null=False, default='')
    source_url: models.URLField = models.URLField()
    answer: models.CharField = models.CharField(max_length=1000, null=False, default='')
    author: models.ForeignKey = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name='question_author')
    published_date: models.DateTimeField = models.DateTimeField(
        "date published", default=timezone.now)
    quiz: models.ForeignKey = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    article_id: models.IntegerField = models.IntegerField(null=False)
    TYPES = (
        ('Title', 'Title'),
        ('Stats', 'Statistics')
    )

    type: models.CharField = models.CharField(
        max_length=2,
        choices=TYPES,
        default='Title',
    )

    def __str__(self):
        return self.question_text
