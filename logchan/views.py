from django.shortcuts import render
from django.http import HttpResponse

from .models import Post

def index(request):
    return HttpResponse("This is the smallest imageboard ever made")


def db(request):

    post = Post()
    post.save()

    posts = Post.objects.all()

    return render(request, 'db.html', {'posts': posts})

