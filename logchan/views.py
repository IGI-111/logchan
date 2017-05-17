from django.shortcuts import render
from django.http import HttpResponse

from .models import Board

def index(request):
    return HttpResponse("This is the smallest imageboard ever made")


def db(request):

    board = Board()
    board.save()

    boards = Board.objects.all()

    return render(request, 'db.html', {'boards': boards})

