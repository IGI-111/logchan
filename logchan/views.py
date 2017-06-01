from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from .models import Board, Thread, Post

def index(request):
    boards = Board.objects.all()
    return render(request, 'index.html', {'boards': boards})

def board(request, board_name):
    boards = Board.objects.all()
    board = Board.objects.get(name=board_name)
    threads = Thread.objects.filter(board=board_name)
    return render(request, 'catalog.html', {
        'boards': boards,
        'board': board,
        'threads':threads
        })

def thread(request, board_name, thread_id):
    boards = Board.objects.all()
    board = Board.objects.get(name=board_name)
    thread = Thread.objects.get(board=board_name, id=thread_id)
    posts = Post.objects.filter(thread=thread_id)
    return render(request, 'thread.html', {
        'boards': boards,
        'board': board,
        'thread':thread,
        'posts':posts
        })

class Login(TemplateView):
    def get(self, request, **kwargs):
        boards = Board.objects.all()
        return render(request, 'login.html', {'boards': boards})
    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect('/')
        boards = Board.objects.all()
        return render(request, 'login.html', {'boards': boards, 'errors' : 'The username or password you entered is incorrect.'})

class Logout(TemplateView):
    def get(self, request, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')

