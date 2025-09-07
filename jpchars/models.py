from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    hiragana_level = models.IntegerField(default=100)
    katakana_level = models.IntegerField(default=100)

class Exercise(models.Model):
    type = models.CharField(max_length=255)
    level = models.IntegerField()
    representation = models.CharField(max_length=255)
    hint = models.CharField(max_length=255, default="")

    def serialize(self):
        return {
            "type": self.type,
            "level": self.level,
            "representation": self.representation,
            "hint": self.hint
        }
    

class Task(models.Model):
    type = models.CharField(max_length=255)
    min_level = models.IntegerField()
    japanese = models.CharField(max_length=255)
    romaji = models.CharField(max_length=255)
    priority = models.BooleanField(default=False)

    def serialize(self):
        return {
            "type": self.type,
            "min_level": self.min_level,
            "japanese": self.japanese,
            "romaji": self.romaji,
            "priority": self.priority
        }