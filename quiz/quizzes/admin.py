from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Player, Question, Quiz

admin.site.register(Player, UserAdmin)
admin.site.register(Question)
admin.site.register(Quiz)
