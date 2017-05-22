from django.shortcuts import render
from django.http import HttpResponse

from .models import Board, Thread, Post

def index(request):
    boards = Board.objects.all()
    return render(request, 'index.html', {'boards': boards})

def board(request, board_name):
    board = Board.objects.get(name=board_name)
    threads = Thread.objects.filter(board=board_name)
    return render(request, 'catalog.html', {'board': board, 'threads':threads})

def thread(request, board_name, thread_id):
    board = Board.objects.get(name=board_name)
    thread = Thread.objects.get(board=board_name, id=thread_id)
    posts = Post.objects.filter(thread=thread_id)
    return render(request, 'thread.html', {'board': board, 'thread':thread, 'posts':posts})
