from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class Player(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField()
    date_joined = models.DateTimeField("date joined", default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Question(models.Model):
    question_text = models.CharField(max_length=4196, null=False)
    source_url = models.URLField()
    answer = models.CharField(max_length=1000, null=False)
    author = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='author')
    published_date = models.DateTimeField("date published", default=timezone.now)

    def __str__(self):
        return self.question_text
