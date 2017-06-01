from __future__ import unicode_literals
from django.db import models
from django.conf import settings

# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Thread(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    def __str__(self):
        return self.subject

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    user_name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.message

