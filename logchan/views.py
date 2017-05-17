from django.shortcuts import render
from django.http import HttpResponse

from .models import Board, Thread

def index(request):
    boards = Board.objects.all()
    return render(request, 'index.html', {'boards': boards})

def board(request, board_name):
    board = Board.objects.get(name=board_name)
    threads = Thread.objects.filter(board=board_name)
    return render(request, 'catalog.html', {'board': board, 'threads':threads})

